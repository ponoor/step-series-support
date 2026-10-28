#!/usr/bin/env python3
"""手作業の確認（段 3）の案内プログラム。CHECKLIST_config_tool_v220.md の、自動テストでは見られない所。

堀尾さんが端末で実行する。1 手順ずつ、「目的」「操作」「見る所」を出す。操作が終わったら Enter。
シリアル・OSC・ping・どのプログラムがポートを開いているかは、このプログラムが自分で確かめる。
目で見ないと分からないことだけを y / n で聞く（1 つの質問で 1 つのことだけ）。

    ~/.venvs/step-config-test/bin/python step-config/tests/guided.py                 # 最初から
    ~/.venvs/step-config-test/bin/python step-config/tests/guided.py --list           # 手順の一覧
    ~/.venvs/step-config-test/bin/python step-config/tests/guided.py --dry-run        # 案内の文を全部表示（ボードは要らない）
    ~/.venvs/step-config-test/bin/python step-config/tests/guided.py --check          # ボードを探して退避するだけ
    ~/.venvs/step-config-test/bin/python step-config/tests/guided.py --only unplug,safari
    ~/.venvs/step-config-test/bin/python step-config/tests/guided.py --resume out/guided_20261028_115035.json --only unplug,safari
    ~/.venvs/step-config-test/bin/python step-config/tests/guided.py --resume out/guided_20261028_115035.json --redo
                                                           # 前の結果で FAIL / 未完了の手順だけやり直す

結果は out/guided_<時刻>.json に、分かるたびに書く。--resume では同じファイルに書き足し、前の結果は
消さない（同じ項目をやり直すと、前の結果は "history" に移り、新しい結果が "results" に入る）。

始める前に 2 枚のボードを（G を送って）見つけ、設定を out/backup_*.json に退避し、基準
（out/golden_*.json）と同じか確かめる。設定を変える手順の終わりに、設定を元に戻す。

モーターが動くのは手順 brake（10.3）だけで、モーターがつながり電源が入っていると答えたときだけ。
その手順の間だけ、動かす OSC コマンドを許可の一覧に足す。

Chrome（や Safari）がシリアルポートを開いていると、このプログラムはそのポートを開けない。
ポートを使う前には必ず確かめ、開いていたら「Chrome で Disconnect を押す」と出して待つ。
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import time

import hw_protocol as hp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
TOOL = os.path.normpath(os.path.join(HERE, '..', 'index.html'))
TEMPLATES = os.path.normpath(os.path.join(HERE, '..', '..', 'configGenerator'))
TEMPLATE400 = os.path.join(TEMPLATES, 'configTemplate_step400.json')
DOWNLOADS = os.path.expanduser('~/Downloads')

# 段 2 の自動テストがカードに残したファイル。このプログラムが消すのは、この名前だけ。
LEFTOVERS = ['/config.txt', '/zzz.json', '/ABC.JSON', '/My Config.json',
             '/STEP400_test_with_a_long_file_name_0123456789.json',
             '/' + 'a' * 57 + '.json', '/test_offline.json']

STEPS = []        # (id, title, function), in order
CHROME_HINT = 'Chrome で、ツールの Disconnect を押す（効かなければ、ツールのタブを閉じる）'


def step(sid, title):
    def deco(fn):
        STEPS.append((sid, title, fn))
        return fn
    return deco


class Stop(Exception):
    pass


# ====================================================================== 案内の文
# すべての案内の文はここにある（--dry-run がこれを順に表示する）。{名前} は実行時の値で入る。
# P = 目的、D = 操作（番号つき。終わったら Enter）、Q = 見る所と質問（y / n）。
def P(text):
    return ('P', text)


def D(*ops):
    return ('D', list(ops))


def Q(look, question):
    return ('Q', look, question)


GUIDE = {
    'chrome': {
        'purpose': P('本物の Chrome で、ツールが STEP400 に接続でき、Disconnect → Connect を繰り返せ、'
                     'ダーク・ライトのどちらでもボタンの文字が読めることを確かめる。'),
        'open': D('Arduino のシリアルモニターなど、シリアルポートを使うプログラムを終了する。',
                  'これから Chrome が開く（このプログラムが開く）。開いたら、ツールが表示されているタブでそのまま作業する。'),
        'connect': D('ツールの Connect を押す。',
                     'ポートの選択の窓で、STEP400 のポートを選ぶ（上の一覧のポート名を見る。2 枚とも同じ名前なら、'
                     '選んだ後でこのプログラムがどちらか確かめる。迷うなら STEP800 の USB を抜く）。',
                     '「Config loaded from board」と出るまで待つ。'),
        'wrong_board': D('STEP800 を選んでしまった。ツールの Disconnect を押し、もう一度 Connect を押して、STEP400 のほうを選ぶ。'),
        'q_status': Q('画面上部の状態表示（ボタンの列の近く）', '状態表示は「Config loaded from board」になっているか。'),
        'q_info': Q('「Board Information」の欄', 'Product が STEP400、Firmware Version が 2.2.0、Axes が「4 (from board)」になっているか。'),
        'cycle': D('ツールの Disconnect を押し、続けて Connect を押す。これを 3 回行う'
                   '（Disconnect → Connect → Disconnect → Connect → Disconnect → Connect）。'
                   'ポートの選択の窓が出たら STEP400 を選ぶ。',
                   '3 回目の Connect で「Config loaded from board」が出たら、この手順は終わり（このプログラムが Connect の回数を数える。最長 90 秒）。'),
        'q_nobanner': Q('Disconnect を押した直後のツールの上部', 'Disconnect を押したとき、黄色い「Serial connection lost」の帯は出なかったか（3 回とも）。'),
        'q_reads': Q('Connect を押したあとの状態表示', 'Connect のたびに「Config loaded from board」と出たか（3 回とも）。'),
        'appearance': D('macOS の外観を {scheme} にする（システム設定 → 外観）。',
                        'Chrome でツールのタブを再読み込みし（⌘R）、Connect を押して接続する。'),
        'q_labels': Q('Connect / Disconnect / Reboot のボタン', '{scheme}: ボタンの文字は読めるか（マウスを乗せない状態で）。'),
        'q_hover': Q('同じボタンにマウスを乗せる', '{scheme}: ボタンにマウスを乗せたときも、文字は読めるか。'),
        'end': D('ツールの Disconnect を押す（次の手順のためにポートを空ける）。'),
    },
    'unplug': {
        'purpose': P('USB を抜いたとき、ツールが接続の喪失を知らせ、Reconnect で戻れること。保存の途中で抜いても、'
                     'ツールが固まらず、Connect に戻れること。Reboot → Connect が使えること。'
                     '（段 3 では、Reconnect が効かず、保存中に抜くとツールが戻らなかった。今回の直し方の確認。）'),
        'console': D('Chrome のツールのタブで、開発者ツールのコンソールを開く（⌥⌘J。Console タブ）。'
                     'うまくいかなかったとき、ここに出る「[serial]」で始まる行をあとで貼ってもらう。'
                     '「[board]」で始まる行はボードが送った文なので、貼らなくてよい。'),
        'connect': D('ツールの Connect を押し（STEP400）、「Config loaded from board」と出るまで待つ。'),
        'pull': D('STEP400 の USB ケーブルを抜く（Ethernet はそのまま）。'),
        'q_banner': Q('ツールの上部', '黄色い「Serial connection lost」の帯が出たか。'),
        'q_connectbtn': Q('ボタンの列', '左端のボタンの文字は「Connect」に戻っているか（「Disconnect」のままではないか）。'),
        'replug': D('USB ケーブルを挿し直し、3 秒待つ。', '黄色い帯の中の「Reconnect」を押す。'),
        'q_reconnect': Q('状態表示', 'ツールは「Config loaded from board」になり、Disconnect が押せる状態に戻ったか。'),
        'recover': D('Reconnect が効かなかった。ツールのタブを再読み込みする（⌘R）。', 'ボタンの列の左端が「Connect」になっていることを確かめる。'),
        'save_prep': D('ボタンの列の左端が「Connect」なら、Connect を押し、「Config loaded from board」を待つ（もう「Disconnect」ならそのまま）。',
                       '「Board Information」の Config Name を unplugtest に書き換える（まだ Save to SD は押さない）。',
                       '次の操作は 0.3 秒で終わる。USB ケーブルに手を添えておく。'),
        'save_pull': D('Save to SD を押し、すぐ（0.3 秒以内に）STEP400 の USB ケーブルを抜く。'
                       '間に合わなくてもよい（保存が終わってから抜けた場合は、あとの質問に n と答える）。'),
        'q_save_btn': Q('ボタンの列', '左端のボタンの文字は、数秒のうちに「Connect」に戻ったか（「Disconnect」のまま動かなくならなかったか）。'),
        'q_save_msg': Q('ツールの上部の赤い帯', '「The connection was lost during the save: the board may or may not have saved …」と出たか。'),
        'q_save_disc': Q('ボタンの列', '左端のボタンを押して反応を見る。ボタンが「Disconnect」のまま固まっていたとき、押して「Connect」に戻ったか'
                         '（最初から「Connect」だったときは s）。'),
        'save_back': D('USB ケーブルを挿し直す。3 秒待つ。',
                       '黄色い帯に Reconnect があれば Reconnect を、無ければ Connect を押して（ポートの選択の窓が出たら STEP400 を選ぶ）、「Config loaded from board」を待つ。',
                       '次に、ツールの Disconnect を押す（このプログラムがボードを読めるように）。'),
        'reboot': D('ツールの Connect を押し、「Config loaded from board」を待つ。',
                    'Reboot を押し、確認の窓で OK を押す。',
                    '「Board rebooted — click Connect to reconnect.」と出たら、Connect を押す（ポートの選択の窓が出たら STEP400 を選ぶ）。'),
        'q_reboot': Q('ツールの状態表示と上部', 'Reboot のあと、黄色い「lost」の帯も「Serial response timeout」のエラーも出ずに、Connect で設定が読めたか。'),
        'end': D('ツールの Disconnect を押す。'),
    },
    'ethernet': {
        'purpose': P('Ethernet ケーブルを抜き差ししたとき、ツールのステータスの Link が OFF / ON に変わることを確かめる。'),
        'start': D('ツールの Connect を押し、「Config loaded from board」を待つ。', 'Start Status を押す。'),
        'q_on': Q('「Real-time Status」の Board の欄', 'Link は ON（緑）か。'),
        'pull': D('STEP400 の Ethernet ケーブルを抜く。'),
        'q_off': Q('同じ欄', '1〜2 秒のうちに Link が OFF（赤）に変わったか。'),
        'plug': D('Ethernet ケーブルを挿し直す。'),
        'q_on2': Q('同じ欄', 'Link が ON（緑）に戻ったか。'),
        'end': D('Stop Status を押し、Disconnect を押す。'),
    },
    'safari': {
        'purpose': P('Web Serial のない Safari で、案内の帯が出て、Connect が使えず、Load JSON / Download JSON は使えることを確かめる。'),
        'open': D('Safari でツールを開く（このプログラムが開く）。',
                  'ファイルを読み込むとき用に、次のファイルを使う: {template}',
                  'ダウンロードされるファイルの場所は Safari の既定のダウンロード先（{downloads}）。'),
        'q_banner': Q('ツールの上部の黄色い帯', '帯に「Web Serial API is not available in this browser」と出ていて、Chrome か Edge を使うよう書いてあるか。'),
        'q_banner_ff': Q('同じ帯', '帯に、Firefox 151 以降は動くはずだが未確認、という意味の文があるか。'),
        'q_grey': Q('ボタンの列の Connect', 'Connect ボタンは灰色で、押せないか（押しても何も起きない）。'),
        'load': D('Load JSON を押し、上のファイル（configTemplate_step400.json）を選ぶ。'),
        'q_load': Q('各設定の表（モーターごとの 4 列の表）', 'Load JSON のあと、4 列の表に数値が入ったか（空の表のままではないか）。'),
        'download': D('Download JSON を押す。ファイル名の確認が出たら、そのまま OK / 保存を押す。'),
        'q_download': Q('{downloads} を Finder で開く', '新しい .json ファイルが保存されていたか（保存の直後の時刻のもの）。'),
    },
    'card': {
        'purpose': P('SD カードに残った試験用のファイルを調べ（3.7）、起動のときに読まれるファイルの順（4.8, 9.5, 9.6, 4.9）を'
                     '本物のボードで確かめる。カードは最初に全部退避し、最後の手順（card-restore）で元に戻す。'),
        'take': D('STEP400 の電源を切る（USB と Ethernet を抜く）。', 'STEP400 から microSD カードを取り出し、Mac に挿す。'),
        'take_again': D('STEP400 の電源を切り、microSD カードを取り出して Mac に挿す。'),
        'scene_a': '場面 a（4.8）: config.txt が無く、.json が何枚かあるとき、アルファベット順で最初の .json が読まれるか',
        'scene_b': '場面 b（9.5）: ダウンロードしたファイルを /test_offline.json として置いたとき',
        'scene_c': '場面 c（9.6）: ダウンロードしたファイルを config.txt として置いたとき',
        'scene_d': '場面 d（4.9）: 名前に空白のある「My Config.json」だけのとき',
        'put': D('カードを取り出す（このプログラムが取り出し済みにした）。STEP400 に挿し、電源を入れる（USB と Ethernet）。'),
        'done': '場面は終わり。最後の場面のカードがボードに入っている。次の手順 card-restore でカードを元に戻す。',
    },
    'card-errors': {
        'purpose': P('カードが無い・外れたとき、ボードとツールが正しく知らせることを確かめる（2.3, 5.1〜5.4, 13.7〜13.9）。'),
        'nocard': D('STEP400 の電源を切り、カードを抜いたまま（そのまま）、電源を入れる（USB と Ethernet）。'),
        'chrome_nocard': D('Chrome のツールで Connect を押し、「Config loaded from board」を待つ。', 'Start Status を押す。', 'Save to SD を押す。'),
        'q_nocard_read': Q('状態表示', '設定は読めた（「Config loaded from board」）か。'),
        'q_nocard_sd': Q('「Real-time Status」の Board の欄', 'SD が「ERR」（赤）、Config が「Not loaded」になっているか。'),
        'q_nocard_save': Q('ツールの上部の赤い帯', 'Save のあとに「Save failed: No SD card — …（FAT16 / FAT32 の説明）」と出たか。'),
        'q_nocard_alive': Q('ボタンの列', 'そのあと Read を押すと、ツールはふつうに動くか（固まっていないか）。'),
        'exfat_ask': Q('手元のカード', 'exFAT で初期化したカードがあるか（無ければ n）。'),
        'exfat': D('そのカードを先に Mac に挿し、ターミナルで「diskutil info /Volumes/（カードの名前）」を実行して、File System Personality が ExFAT であることを確かめる'
                   '（FAT32 だと、この確認にならない。段 3 では、保存が成功してしまった）。',
                   'STEP400 の電源を切り、そのカードを入れて、電源を入れる。'),
        'chrome_exfat': D('Chrome のツールで Connect を押し、Save to SD を押す。'),
        'q_exfat_msg': Q('ツールの上部の赤い帯', 'exFAT の説明が付いた「No SD card」が出たか。'),
        'q_exfat_sd': Q('「Real-time Status」の Board の欄', 'SD が「ERR」になっているか。'),
        'fat': D('STEP400 の電源を切り、いつもの FAT32 のカードを入れて、電源を入れる。5 秒待つ。',
                 '動いているボードから、そのカードを取り出す（電源は入れたまま）。'),
        'chrome_removed': D('Chrome のツールで Connect を押し、Save to SD を押す。'),
        'q_removed_msg': Q('ツールの上部の赤い帯', '「Save failed: SD open failed — …（起動後にカードが外れた、など）」と出たか。'),
        'q_removed_read': Q('ボタンの列', 'Read は、今も使えるか。'),
        'putback': D('カードをボードに挿し直す。3 秒待つ。'),
        'chrome_reboot': D('Chrome のツールで Reboot を押し、OK を押す。', '「Board rebooted」と出たら Connect を押し、Save to SD をもう一度押す。'),
        'q_saved': Q('状態表示', '今度は「Saved to SD」と出て、保存できたか。'),
        'end': D('ツールの Disconnect を押す。'),
    },
    'brake': {
        'purpose': P('モーターが回っている間に Reboot を押したとき、モーターが止まり（ブレーキがあれば保持し）、ツールがエラーを出さないことを確かめる（10.3）。'
                     'この手順だけ、モーターが動く。ゆっくり（400 マイクロステップ/秒 ≒ 1 秒に約 3 フルステップ）。'),
        'q_motor': Q('モーターと電源', 'STEP400 にモーターがつながり、その電源が入っていて、自由に回れて、周りに何も無いか（n なら、この手順を飛ばす）。'),
        'q_brake': Q('そのモーター', 'そのモーターには電磁ブレーキ（EMB-STEP400、24 V 入力）がついているか。'),
        'brake_on': '電磁ブレーキを有効にした（この手順の終わりに元に戻す）。ボードを再起動して、有効を反映する。',
        'release': '電磁ブレーキを解放する（/activate {m} 1）。解放まで {sec:.1f} 秒待つ。',
        'start': D('Chrome のツールで Connect を押し、「Config loaded from board」を待つ。',
                   'ここで Enter を押すと、モーターがゆっくり回り始める。'),
        'q_turn': Q('モーター', 'モーターはゆっくり回っているか。'),
        'reboot': D('Chrome のツールで Reboot を押し、OK を押す。モーター（ブレーキ）の動きを見る。',
                    '「Board rebooted…」と出たら、Enter を押す。'),
        'q_stop': Q('モーター', 'モーターは止まったか（ブレーキがあれば、保持されたか）。'),
        'q_noerr': Q('ツールの上部の赤い帯', '「Serial response timeout」のエラーは出なかったか。'),
        'end': D('ツールの Disconnect を押す。'),
    },
    'card-restore': {
        'purpose': P('手順 card で使ったカードを、元の状態に戻す（試験用のファイルを消す）。'),
        'take': D('STEP400 の電源を切り、カードを取り出して Mac に挿す。'),
        'put': D('カードを STEP400 に挿し、電源を入れる（USB と Ethernet）。'),
    },
    'final': {
        'purpose': P('両方のボードの設定を元に戻し、基準と比べる。'),
    },
}

# --dry-run が {…} に入れる例の値
SAMPLE = dict(scheme='DARK', template=TEMPLATE400, downloads=DOWNLOADS, m=1, sec=0.6)


class Guide:
    dry = False

    def __init__(self, path, results):
        self.path = path
        self.results = results
        self.boards = None
        self.golden = {}
        self.step_id = None

    # ---- 話す
    def say(self, *a):
        print(*a, flush=True)

    def head(self, sid, title):
        self.step_id = sid
        self.say('\n' + '=' * 72 + f'\n[{sid}] {title}\n' + '=' * 72)

    def text(self, sid, key, **kw):
        b = GUIDE[sid][key]
        return b.format(**{**SAMPLE, **kw}) if isinstance(b, str) else b

    def purpose(self, sid, **kw):
        self.say('\n【目的】' + GUIDE[sid]['purpose'][1].format(**{**SAMPLE, **kw}))

    def info(self, sid, key, **kw):
        self.say('   ' + self.text(sid, key, **kw))

    def do(self, sid, key, **kw):
        """【操作】を出して、終わったら Enter を待つ。"""
        ops = GUIDE[sid][key][1]
        self.say('\n【操作】')
        for i, o in enumerate(ops, 1):
            self.say(f'  {i}. ' + o.format(**{**SAMPLE, **kw}))
        self.wait_enter()

    def wait_enter(self):
        try:
            a = input('   -> 終わったら Enter（q + Enter: ここで止める） ')
        except EOFError:
            raise Stop()
        if a.strip().lower() == 'q':
            raise Stop('stopped by the person')

    def ask(self, sid, key, **kw):
        """【見る所】と質問。y = はい / n = いいえ / s = 分からない・飛ばす → True / False / None。"""
        _, look, question = GUIDE[sid][key]
        kw = {**SAMPLE, **kw}
        self.say('\n【見る所】' + look.format(**kw))
        while True:
            try:
                a = input(f'{question.format(**kw)}  [y=はい / n=いいえ / s=分からない] ').strip().lower()
            except EOFError:
                raise Stop()
            if a in ('y', 'n', 's'):
                return {'y': True, 'n': False, 's': None}[a]

    def yn(self, msg):
        while True:
            try:
                a = input(f'\n{msg}  [y=はい / n=いいえ / s=飛ばす] ').strip().lower()
            except EOFError:
                raise Stop()
            if a in ('y', 'n', 's'):
                return {'y': True, 'n': False, 's': None}[a]

    def choose(self, msg, options):
        for i, o in enumerate(options, 1):
            self.say(f'  {i}. {o}')
        while True:
            a = input(f'{msg}（番号） ').strip()
            if a.isdigit() and 1 <= int(a) <= len(options):
                return options[int(a) - 1]

    def paste_log(self, label):
        """うまくいかなかったとき、コンソールの [serial] の行を貼ってもらい、結果のファイルに残す。"""
        self.say('\nうまくいかなかったようです。Chrome のコンソール（⌥⌘J）にある「[serial]」で始まる行を（「[board]」の行はボードの文なので要らない）、'
                 '全部コピーして、ここに貼り付けてください。貼り終わったら、空の行（Enter だけ）を送ります。'
                 '（貼らないときは、すぐ Enter）')
        lines = []
        while True:
            try:
                ln = input()
            except EOFError:
                break
            if not ln.strip():
                break
            lines.append(ln)
        self.results.setdefault('serial_logs', {})[f'{label} {datetime.datetime.now().isoformat(timespec="seconds")}'] = lines
        self.save()
        self.say(f'   {len(lines)} 行を結果のファイルに保存した。')

    # ---- 結果
    def record(self, rid, ok, detail='', rows=()):
        """ok: True / False / None (skipped). すぐファイルに書く。前の同じ項目は history に移す。"""
        res = self.results['results']
        if rid in res:
            self.results.setdefault('history', []).append(dict(res[rid], id=rid, superseded=datetime.datetime.now().isoformat(timespec='seconds')))
        res[rid] = dict(ok=ok, detail=detail, rows=list(rows), step=self.step_id,
                        time=datetime.datetime.now().isoformat(timespec='seconds'))
        self.save()
        mark = {True: 'PASS', False: 'FAIL', None: 'SKIP'}[ok]
        self.say(f'   [{mark}] {rid}  {detail}')

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.results, f, indent=1, default=str, ensure_ascii=False)

    # ---- ボード
    def find(self):
        self.boards = hp.find_boards()
        return self.boards

    def show_ports(self):
        self.say('\n2 枚のボードと USB のポート（G を送って見分けた。ポートの名前では見分けていない）:')
        for prod, b in sorted(self.boards.items()):
            self.say(f'  {b.device:28s} {prod}  USB シリアル番号 {b.serial_number}  場所 {b.port["location"]}'
                     f'  IP {b.my_ip}  ID {b.my_id}')
        names = {b.port['description'] for b in self.boards.values()}
        if len(names) == 1:
            self.say('  2 枚のボードはポートの一覧で同じ名前（例: "Arduino Zero"）に見える。Chrome の一覧の順番は当てにならない。\n'
                     '  選んだあとで、このプログラムがどちらのボードか確かめる。迷うときは、もう一方の USB を抜く。')

    def holders(self, b):
        return hp.port_holders(b.device)

    def wait_port(self, b, present, timeout=60):
        t0 = time.time()
        while time.time() - t0 < timeout:
            here = any(p['serial_number'] == b.serial_number for p in hp.usb_ports())
            if here == present:
                if present:
                    b.find_again(5)
                return True
            time.sleep(0.2)
        return False

    def wait_held(self, b, held, timeout=60):
        t0 = time.time()
        while time.time() - t0 < timeout:
            if bool(self.holders(b)) == held:
                return True
            time.sleep(0.2)
        return False

    def need_free(self, b):
        """シリアルポートを開く前に必ず呼ぶ。ほかのプログラム（Chrome）が開いていたら、閉じるよう出して待つ。"""
        while self.holders(b):
            self.say(f'\n⚠ {b.product} のシリアルポートが、ほかのプログラム（Chrome など）で開かれたままです: {CHROME_HINT}。')
            for _ in range(20):                  # 自分で閉じたら、すぐ先へ進む
                time.sleep(0.25)
                if not self.holders(b):
                    return
            try:
                input('   -> 閉じたら Enter ')
            except EOFError:
                raise Stop()

    def line(self, b):
        """ボードのシリアルを開く（開く前に、空いているか確かめる）。with で使う。"""
        self.need_free(b)
        return b.line()

    def wait_booted(self, b, timeout=40):
        """同じ USB シリアル番号のボードが戻り、メインループが T に答えるまで待つ。"""
        if not self.wait_port(b, True, timeout):
            return False
        for _ in range(int(timeout * 2)):
            self.need_free(b)            # Stop は外へ出す
            try:
                with b.line() as ln:
                    b.T = ln.get_status(timeout=1)
                    b.G = ln.get_config(timeout=2)
                return True
            except Exception:       # noqa: BLE001  （まだ起動中）
                time.sleep(0.5)
        return False

    def restore(self, prod):
        self.need_free(self.boards[prod])
        d = hp.restore(self.golden[prod])
        if d:                           # 1 回で戻らなかった（10.3 の後に起きた）: もう 1 回やる
            self.say(f'   戻した結果が基準と違った。もう 1 回戻す: {"; ".join(d)}')
            d = hp.restore(self.golden[prod])
        b = self.boards[prod] = hp.find_boards()[prod]
        b.osc_set_dest()
        return d

    def restore_all(self):
        out = {}
        for prod in self.boards:
            try:
                out[prod] = self.restore(prod)
            except Exception as e:      # noqa: BLE001
                out[prod] = [f'restore failed: {e!r}']
        return out


def open_app(app, path):
    subprocess.run(['open', '-a', app, path])


# ====================================================================== 手順
@step('chrome', '本物の Chrome: Connect（ポートの選択）、Disconnect → Connect を 3 回、ダーク・ライト')
def s_chrome(g):
    sid = 'chrome'
    b4 = g.boards['STEP400']
    g.purpose(sid)
    g.show_ports()
    g.do(sid, 'open')
    open_app('Google Chrome', TOOL)
    g.do(sid, 'connect')
    held = [p for p, b in g.boards.items() if g.holders(b)]
    g.record('1.1 chrome port choice', held == ['STEP400'], f'Chrome がポートを開いているボード: {held}')
    if held == ['STEP800']:
        g.do(sid, 'wrong_board')
        g.wait_held(g.boards['STEP800'], False)
    r = g.ask(sid, 'q_status')
    g.record('1.1 chrome: Config loaded from board', r)
    r = g.ask(sid, 'q_info')
    g.record('1.2 chrome: Product / Firmware / Axes', r)
    # Disconnect -> Connect を 3 回: ポートが開かれる回数をこのプログラムが数える
    g.say('\n【操作】')
    g.say('  ' + GUIDE[sid]['cycle'][1][0])
    g.say('  ' + GUIDE[sid]['cycle'][1][1])
    prev = bool(g.holders(b4))
    t0 = time.time()
    opens = 0
    while time.time() - t0 < 90 and opens < 3:
        now = bool(g.holders(b4))
        if now and not prev:
            opens += 1
            g.say(f'   ポートが開かれた（Connect {opens} 回目）')
        prev = now
        time.sleep(0.15)
    g.record('1.6 chrome: Connect x3 (port opened)', opens >= 3, f'Disconnect 後に開かれた回数: {opens}')
    r1 = g.ask(sid, 'q_nobanner')
    g.record('1.6 chrome: no banner after Disconnect', r1)
    r2 = g.ask(sid, 'q_reads')
    g.record('1.6 chrome: every Connect read the config', r2)
    for scheme in ('DARK', 'LIGHT'):
        g.do(sid, 'appearance', scheme=scheme)
        r = g.ask(sid, 'q_labels', scheme=scheme)
        g.record(f'11.2 {scheme.lower()} mode: button labels', r)
        r = g.ask(sid, 'q_hover', scheme=scheme)
        g.record(f'11.2 {scheme.lower()} mode: hover', r)
    g.do(sid, 'end')
    g.wait_held(b4, False)


@step('unplug', 'USB を抜く: 帯・Reconnect・保存の途中で抜く・Reboot → Connect')
def s_unplug(g):
    sid = 'unplug'
    b = g.boards['STEP400']
    g.purpose(sid)
    g.need_free(b)
    g.do(sid, 'console')
    g.do(sid, 'connect')
    g.wait_held(b, True)
    g.do(sid, 'pull')
    gone = g.wait_port(b, False, 30)
    g.record('1.7 unplug seen', gone, 'ポートが消えた' if gone else 'ポートが残っている')
    r1 = g.ask(sid, 'q_banner')
    g.record('1.7 banner after unplug', r1)
    r2 = g.ask(sid, 'q_connectbtn')
    g.record('1.7 button back to Connect', r2)
    g.do(sid, 'replug')
    back = g.wait_port(b, True, 30)
    r3 = g.ask(sid, 'q_reconnect')
    held = bool(g.holders(b))
    g.record('1.7 reconnect', bool(back and r3 and held), f'ポート復帰={back} 画面={r3} Chrome がポートを開いている={held}')
    if not (back and r3 and held):
        g.paste_log('1.7 reconnect')
        g.do(sid, 'recover')
    # 保存の途中で抜く
    g.do(sid, 'save_prep')
    g.wait_held(b, True, 60)
    g.do(sid, 'save_pull')
    g.wait_port(b, False, 15)
    ra = g.ask(sid, 'q_save_btn')
    g.record('3.x unplug during save: button back to Connect', ra)
    rb = g.ask(sid, 'q_save_msg')
    g.record('3.x unplug during save: message', rb)
    if ra is not True:
        rc = g.ask(sid, 'q_save_disc')
        g.record('3.x unplug during save: Disconnect still works', rc)
        g.paste_log('3.x unplug during save')
    g.do(sid, 'save_back')
    g.wait_port(b, True, 30)
    g.wait_held(b, False, 120)
    g.wait_booted(b)
    name = b.G['information']['configName']
    g.record('3.x unplug during save: result on the board', None,
             f'G の configName = {name!r}（保存は{"された" if name == "unplugtest" else "されていない"}）; resetCause {b.T["board"]["resetCause"]}')
    d = g.restore('STEP400')
    g.record('unplug: settings back', not d, '; '.join(d))
    g.do(sid, 'reboot')
    g.wait_held(b, True, 120)
    r = g.ask(sid, 'q_reboot')
    g.record('10.1/10.2 reboot -> connect in Chrome', r)
    g.do(sid, 'end')
    g.wait_held(b, False)


@step('ethernet', 'Ethernet ケーブル: ステータスの Link が OFF / ON')
def s_ethernet(g):
    sid = 'ethernet'
    b = g.boards['STEP400']
    g.purpose(sid)
    g.need_free(b)
    g.do(sid, 'start')
    r = g.ask(sid, 'q_on')
    g.do(sid, 'pull')
    time.sleep(2)
    ping = subprocess.run(['ping', '-c', '1', '-t', '2', b.my_ip], capture_output=True).returncode
    r2 = g.ask(sid, 'q_off')
    g.do(sid, 'plug')
    time.sleep(3)
    ping2 = subprocess.run(['ping', '-c', '1', '-t', '2', b.my_ip], capture_output=True).returncode
    r3 = g.ask(sid, 'q_on2')
    g.record('2.2 link off/on', bool(r and r2 and r3 and ping != 0 and ping2 == 0),
             f'ON={r} OFF={r2} ON again={r3}; ケーブルを抜いたときの ping rc={ping}（0 以外が正）, 戻したとき rc={ping2}')
    g.do(sid, 'end')
    g.wait_held(b, False)


@step('safari', 'Safari: 帯・Connect が押せない・Load / Download')
def s_safari(g):
    sid = 'safari'
    g.purpose(sid)
    g.do(sid, 'open')
    open_app('Safari', TOOL)
    r1 = g.ask(sid, 'q_banner')
    g.record('11.1 safari: banner names Web Serial / Chrome / Edge', r1)
    r1b = g.ask(sid, 'q_banner_ff')
    g.record('11.1 safari: banner says Firefox 151+ untested', r1b)
    r2 = g.ask(sid, 'q_grey')
    g.record('11.1 safari: Connect is greyed', r2)
    g.do(sid, 'load')
    r3 = g.ask(sid, 'q_load')
    g.record('11.1 safari: Load JSON fills the tables', r3)
    before = set(os.listdir(DOWNLOADS)) if os.path.isdir(DOWNLOADS) else set()
    g.do(sid, 'download')
    new = sorted(n for n in (set(os.listdir(DOWNLOADS)) - before) if n.lower().endswith('.json')) if os.path.isdir(DOWNLOADS) else []
    r4 = g.ask(sid, 'q_download')
    g.record('11.1 safari: Download JSON saves a file', r4, f'{DOWNLOADS} に増えた .json: {new}（このプログラムが見たもの）')


# ---------------------------------------------------------------- カードの手順
def volumes():
    return sorted(os.listdir('/Volumes'))


def first_json(card):
    """loadConfig.cpp findFirstValidJson(): ルートの *.json をアルファベット順（大小無視）に見て最初のもの。
    名前が '.' で始まるものは飛ばす。それが正しくなければ、次は試さない。名前（なければ None）を返す。"""
    names = [n for n in os.listdir(card) if not n.startswith('.') and n.lower().endswith('.json')
             and os.path.isfile(os.path.join(card, n))]
    names.sort(key=str.lower)
    if not names:
        return None
    try:
        d = json.load(open(os.path.join(card, names[0])))
        return '/' + names[0] if d['information']['configVersion'] is not None else None
    except Exception:
        return None


def expected_boot_file(card):
    cfg = os.path.join(card, 'config.txt')
    if os.path.exists(cfg):
        try:
            json.load(open(cfg))
            return '/config.txt'
        except Exception:
            pass
    return first_json(card)


def one_line_json(raw):
    """3.7: 中身が改行を含まない 1 行の JSON か。末尾の改行（LF か CRLF）1 つは許す。(ok, 理由)"""
    body = raw
    if body.endswith(b'\r\n'):
        body = body[:-2]
    elif body.endswith(b'\n'):
        body = body[:-1]
    if b'\n' in body or b'\r' in body:
        return False, '中身に改行がある'
    try:
        d = json.loads(body)
    except Exception as e:      # noqa: BLE001
        return False, f'JSON ではない ({e})'
    if not isinstance(d, dict) or 'information' not in d:
        return False, 'information が無い'
    return True, ''


def judge_card_files(card):
    """カードの（または退避の）ルートの .json / .txt を 3.7 で判定する。(判定できたファイル数, 不合格の一覧)"""
    bad, n = [], 0
    for name in sorted(os.listdir(card)):
        p = os.path.join(card, name)
        if name.startswith('.') or not os.path.isfile(p) or not name.lower().endswith(('.json', '.txt')):
            continue
        n += 1
        ok, why = one_line_json(open(p, 'rb').read())
        if not ok:
            bad.append(f'{name}: {why}')
    return n, bad


def pick_card(g, sid, key):
    before = set(volumes())
    g.do(sid, key)
    time.sleep(3)
    new = sorted(set(volumes()) - before)
    opts = new + [v for v in volumes() if v not in new]
    g.say('いま見えているボリューム: ' + ', '.join(volumes()))
    vol = g.choose('どれが STEP400 のカードか', opts)
    path = os.path.join('/Volumes', vol)
    info = subprocess.run(['diskutil', 'info', path], capture_output=True, text=True).stdout
    fs = next((l.split(':', 1)[1].strip() for l in info.splitlines() if 'File System Personality' in l), '?')
    g.say(f'   {path}: {fs}')
    if 'FAT' not in fs.upper():
        raise Stop(f'{path} は {fs} で、FAT ではない。何も書かずに止める')
    ok = g.yn(f'{path} に書き込んでよいか（書くのは LEFTOVERS の名前のファイルと、場面のファイルだけ）')
    if not ok:
        raise Stop('カードが確認されなかった')
    return path


def eject(g, path):
    subprocess.run(['sync'])
    subprocess.run(['diskutil', 'eject', path], capture_output=True)
    g.say('   カードを取り出し済みにした。')


def board_booted_with_card(g, b):
    g.do('card', 'put')
    ok = g.wait_booted(b, 60)
    if ok:
        b.osc_set_dest()
    return ok


def scene(g, card, name, setup, expect_name, why):
    """カードに setup(card) をして、ボードに入れ、起動し、/getConfigName を OSC で聞く。"""
    b = g.boards['STEP400']
    setup(card)
    exp_file = expected_boot_file(card)
    eject(g, card)
    if not board_booted_with_card(g, b):
        g.record(name, False, 'ボードが戻ってこなかった')
        return False
    r = b.osc_query('/getConfigName', timeout=1.5)
    got = r[0][1] if r else None
    ok = bool(got) and got[4] == exp_file and got[0] == expect_name and tuple(got[1:4]) == (1, 1, 1)
    g.record(name, ok, f'{why}: /configName = {got}; 読まれるはずのファイル {exp_file}, 名前 {expect_name!r}')
    return ok


def write_cfg(card, fname, cfg_name, g):
    base = json.loads(json.dumps(g.golden_G['STEP400']))
    base.pop('board')
    base['information'] = dict(configName=cfg_name, configVersion=[1, 2], targetProduct='STEP400')
    with open(os.path.join(card, fname.lstrip('/')), 'w') as f:
        f.write(json.dumps(base, separators=(',', ':')) + '\n')


@step('card', 'カード（STEP400）: 試験で残ったファイル・起動で読まれるファイルの順（3.7, 4.8, 9.5, 9.6, 4.9）')
def s_card(g):
    sid = 'card'
    b = g.boards['STEP400']
    g.purpose(sid)
    g.need_free(b)
    card = pick_card(g, 'card', 'take')
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    bk = os.path.join(OUT, f'card_backup_{stamp}')
    shutil.copytree(card, bk, ignore=shutil.ignore_patterns('.Spotlight*', '.fseventsd', '.Trashes'))
    g.results['card_backup'] = bk
    g.results['card_volume'] = card
    g.save()
    g.say(f'   カードの中身を全部 {bk} に退避した')
    files = sorted(n for n in os.listdir(card) if not n.startswith('.'))
    g.say('   カードにあるファイル: ' + ', '.join(files))
    # 3.7: 自動テストが書いたファイルは 1 行の JSON（末尾の改行 1 つは許す）
    n, bad = judge_card_files(card)
    tmp = [x for x in os.listdir(card) if x.startswith('.') and x.endswith('.tmp')]
    g.record('3.7 files on the card are one-line JSON', not bad and not tmp,
             f'{n} 個を判定。' + '; '.join(bad + ([f'残った一時ファイル: {tmp}'] if tmp else [])))
    cfgtxt = os.path.join(card, 'config.txt')
    if os.path.exists(cfgtxt):
        d = json.load(open(cfgtxt))
        g.record('3.7 config.txt information.configName', d['information']['configName'] == b.G['information']['configName'],
                 f'{d["information"]["configName"]!r}')
    g.record('4.1 long-name file exists', os.path.exists(os.path.join(card, LEFTOVERS[4].lstrip('/'))))
    held = os.path.join(bk, '_held')
    os.makedirs(held, exist_ok=True)

    def only(*keep):
        def f(card):
            for n in os.listdir(card):
                if n.startswith('.'):
                    continue
                p = os.path.join(card, n)
                if os.path.isfile(p) and n not in keep and ('/' + n) in LEFTOVERS:
                    shutil.move(p, os.path.join(held, n))
        return f

    g.say('\n' + GUIDE[sid]['scene_a'])
    def a(card):
        only('ABC.JSON', 'My Config.json', 'zzz.json', LEFTOVERS[5].lstrip('/'), LEFTOVERS[4].lstrip('/'))(card)
    scene(g, card, '4.8 no config.txt, several .json -> first in alphabetical order', a, 'Default', 'config.txt を除いた')
    card = pick_card(g, 'card', 'take_again')
    g.say('\n' + GUIDE[sid]['scene_b'])
    def bscene(card):
        only()(card)
        write_cfg(card, '/test_offline.json', 'offline-b', g)
    scene(g, card, '9.5 downloaded file as /test_offline.json (config.txt moved away)', bscene, 'offline-b',
          'test_offline.json だけ')
    card = pick_card(g, 'card', 'take_again')
    g.say('\n' + GUIDE[sid]['scene_c'])
    def cscene(card):
        only()(card)
        write_cfg(card, '/config.txt', 'offline-c', g)
    scene(g, card, '9.6 downloaded file as config.txt', cscene, 'offline-c', 'config.txt')
    card = pick_card(g, 'card', 'take_again')
    g.say('\n' + GUIDE[sid]['scene_d'])
    def dscene(card):
        only()(card)
        write_cfg(card, '/My Config.json', 'spaced-boot', g)
    scene(g, card, '4.9 only "My Config.json" is read at start-up', dscene, 'spaced-boot', '空白のある名前')
    g.say('\n' + GUIDE[sid]['done'])


@step('card-errors', 'カードのエラー: 起動時に無い・起動後に外れた・戻した・再起動（2.3, 5, 13.7〜13.9）')
def s_card_errors(g):
    sid = 'card-errors'
    b = g.boards['STEP400']
    g.purpose(sid)
    g.need_free(b)
    cfg = json.loads(json.dumps(b.G))
    # 起動時にカードが無い
    g.do(sid, 'nocard')
    g.wait_booted(b, 60)                       # （ポートを使う前に、Chrome が開いていないか確かめる）
    sd = b.T['board']['sdInitialized']
    with g.line(b) as ln:
        r = ln.send_config(cfg)
    g.record('5.1 no card at start: board side', sd is False and r == {'result': 'error', 'message': 'No SD card'},
             f'sdInitialized={sd}, 保存の答え {r}')
    g.do(sid, 'chrome_nocard')
    g.record('5.1 tool: read works', g.ask(sid, 'q_nocard_read'))
    g.record('5.1/2.3 tool: SD ERR / Config Not loaded', g.ask(sid, 'q_nocard_sd'))
    g.record('13.7 tool: save error message (no SD card)', g.ask(sid, 'q_nocard_save'))
    g.record('13.7 tool still works after the error', g.ask(sid, 'q_nocard_alive'))
    g.do(sid, 'end')
    g.wait_held(b, False)
    # exFAT（あれば）
    if g.ask(sid, 'exfat_ask'):
        g.do(sid, 'exfat')
        g.wait_booted(b, 60)
        with g.line(b) as ln:
            r = ln.send_config(cfg)
        g.record('5.2 exFAT: board side', b.T['board']['sdInitialized'] is False and r.get('message') == 'No SD card', f'{r}')
        g.do(sid, 'chrome_exfat')
        g.record('13.9 tool: exFAT hint in the error', g.ask(sid, 'q_exfat_msg'))
        g.record('5.2 tool: SD ERR with exFAT', g.ask(sid, 'q_exfat_sd'))
        g.do(sid, 'end')
        g.wait_held(b, False)
    else:
        g.record('5.2/13.9 exFAT', None, 'exFAT のカードが無い')
    # 起動後に外す
    g.do(sid, 'fat')
    g.wait_booted(b, 60)
    before = b.T['board']['resetCauseRaw'], b.T['board']['sdInitialized']
    with g.line(b) as ln:
        r = ln.send_config(cfg)
        t = ln.get_status()
    g.record('5.3 card removed after start: board side', before[1] and r == {'result': 'error', 'message': 'SD open failed'}
             and t['board']['resetCause'] == b.T['board']['resetCause'], f'保存の答え {r}; ボードは再起動しなかった')
    g.do(sid, 'chrome_removed')
    g.record('13.8 tool: save error message (SD open failed)', g.ask(sid, 'q_removed_msg'))
    g.record('5.3 tool: Read still works', g.ask(sid, 'q_removed_read'))
    g.do(sid, 'end')
    g.wait_held(b, False)
    # 戻しても、再起動するまで保存は失敗する
    g.do(sid, 'putback')
    with g.line(b) as ln:
        r = ln.send_config(cfg)
    g.record('5.4 card put back: save still fails until a restart', r.get('message') == 'SD open failed', f'{r}')
    g.do(sid, 'chrome_reboot')
    g.record('5.4 after the restart the save works', g.ask(sid, 'q_saved'))
    g.do(sid, 'end')
    g.wait_held(b, False)
    d = g.restore('STEP400')
    g.record('card-errors: settings back', not d, '; '.join(d))


def osc_errors(msgs):
    """/error/command などの OSC エラー。(文, 引数) の一覧。"""
    return [(a, args) for a, args, *_ in msgs if a.startswith('/error')]


@step('brake', '10.3 モーターが回っている間に Reboot（モーターがつながり、電源が入っているとき）')
def s_brake(g):
    sid = 'brake'
    b = g.boards['STEP400']
    g.purpose(sid)
    g.need_free(b)
    if not g.ask(sid, 'q_motor'):
        g.record('10.3 reboot while turning', None, '飛ばした: モーターが無い')
        return
    m = int(g.choose('モーターは STEP400 の何番の出力か', ['1', '2', '3', '4']))
    brake = bool(g.ask(sid, 'q_brake'))
    changed = False
    try:
        if brake:
            cfg = json.loads(json.dumps(b.G))
            cfg['driverSettings']['electromagnetBrakeEnable'][m - 1] = True
            with g.line(b) as ln:
                ln.send_config(cfg)
                ln.send(b'R')
            changed = True
            g.wait_booted(b, 40)
            b.osc_set_dest()
            g.info(sid, 'brake_on')
        with hp.allowed('/activate', '/run', '/softStop'):
            if brake:
                dur = b.G['driverSettings']['brakeTransitionDuration'][m - 1] / 1000.0
                g.info(sid, 'release', m=m, sec=dur + 0.5)
                b.osc_send('/activate', m, 1)
                time.sleep(dur + 0.5)
                rs = b.osc_query('/getBrakeStatus', m, timeout=1.0)
                state = next((args[1] for a, args, *_ in rs if a == '/brakeStatus' and args and args[0] == m), None)
                if state != 2:                        # 2 = RELEASED（brakeControl.h）
                    errs = osc_errors(rs)
                    g.say(f'   ブレーキが解放されなかった（/brakeStatus の状態 {state}; 2 が解放）。ボードのエラー: {errs}')
                    g.record('10.3 reboot while turning', None, f'ブレーキが解放されず飛ばした: 状態 {state}, エラー {errs}')
                    return
            g.do(sid, 'start')
            b.osc_set_dest()
            rs = b.osc_query('/run', m, 400, timeout=0.6)
            errs = osc_errors(rs)
            if errs:
                g.say(f'   ボードが /run を受け付けなかった: {errs}')
                b.osc_send('/softStop', m)
                g.record('10.3 reboot while turning', None, f'/run が拒否された: {errs}')
                return
            r = g.ask(sid, 'q_turn')
            if not r:
                b.osc_send('/softStop', m)
                if brake:
                    b.osc_send('/activate', m, 0)
                g.record('10.3 reboot while turning', None, 'モーターが回らなかった（止めた）')
                return
            g.do(sid, 'reboot')
            b.osc_send('/softStop', m)        # ボードが再起動中なら何も起きない
        r1 = g.ask(sid, 'q_stop')
        r2 = g.ask(sid, 'q_noerr')
        g.record('10.3 reboot while turning', bool(r1 and r2), f'brake={brake} motor={m} 止まった={r1} タイムアウトなし={r2}')
        g.do(sid, 'end')
        g.wait_held(b, False)
    finally:
        if changed:
            d = g.restore('STEP400')
            g.record('brake: settings back', not d, '; '.join(d))


@step('card-restore', 'カードを元に戻す。この確認用に作ったファイルを消す')
def s_card_restore(g):
    sid = 'card-restore'
    b = g.boards['STEP400']
    g.purpose(sid)
    g.need_free(b)
    card = pick_card(g, 'card-restore', 'take')
    bk = g.results.get('card_backup')
    present = [n for n in LEFTOVERS if os.path.exists(os.path.join(card, n.lstrip('/')))]
    g.say('カードから消すファイル（この名前だけ）: ' + (', '.join(present) or '（なし）'))
    others = sorted(n for n in os.listdir(card) if not n.startswith('.') and ('/' + n) not in LEFTOVERS)
    if others:
        g.say('   ほかのファイル（そのまま）: ' + ', '.join(others))
    if g.yn('上のファイルを消してよいか'):
        for n in present:
            os.remove(os.path.join(card, n.lstrip('/')))
        left = [n for n in os.listdir(card) if n.endswith('.tmp')]
        for n in left:
            os.remove(os.path.join(card, n))
        g.record('card restored (test files deleted)', True, f'消した {present} {left}; カード全体の退避 {bk}')
    eject(g, card)
    g.do(sid, 'put')
    g.wait_booted(b, 60)
    d = g.restore('STEP400')
    g.record('card-restore: settings back', not d, '; '.join(d))


@step('final', '両方のボードを元に戻して比べる')
def s_final(g):
    g.purpose('final')
    out = g.restore_all()
    ok = all(not v for v in out.values())
    g.record('settings of both boards are as before', ok, json.dumps(out))
    for p, b in g.boards.items():
        g.record(f'OSC answers at the original IP {p}', bool(b.osc_query('/getVersion', timeout=1.5)), b.my_ip)


# ====================================================================== main
def dry_run():
    """案内の文を全部出す（ボードも Chrome も要らない）。"""
    for sid, title, _ in STEPS:
        print('\n' + '=' * 72 + f'\n[{sid}] {title}\n' + '=' * 72)
        for key, b in GUIDE[sid].items():
            if isinstance(b, str):
                print(f'\n（メッセージ {key}）\n   ' + b.format(**SAMPLE))
            elif b[0] == 'P':
                print('\n【目的】' + b[1].format(**SAMPLE))
            elif b[0] == 'D':
                print(f'\n【操作】（{key}）')
                for i, o in enumerate(b[1], 1):
                    print(f'  {i}. ' + o.format(**SAMPLE))
                print('   -> 終わったら Enter')
            else:
                print(f'\n【見る所】（{key}）' + b[1].format(**SAMPLE))
                print(f'{b[2].format(**SAMPLE)}  [y=はい / n=いいえ / s=分からない]')
    return 0


def step_of(rid, rec):
    """結果の項目がどの手順のものか（前の結果のファイルには step が無い）。"""
    if rec.get('step'):
        return rec['step']
    table = [('chrome', ('1.1', '1.6', '11.2')), ('unplug', ('1.7', '3.x', 'unplug:', '10.1')), ('ethernet', ('2.2',)),
             ('safari', ('11.1',)), ('card-errors', ('5.', '13.', 'card-errors', '2.3')),
             ('brake', ('10.3', 'brake:')), ('card-restore', ('card restored', 'card-restore')),
             ('final', ('settings of both', 'OSC answers')), ('card', ('3.7', '4.', '9.'))]
    for sid, keys in table:
        if any(rid.startswith(k) for k in keys):
            return sid
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--resume', metavar='FILE', help='前の結果のファイル。同じファイルに書き足す（前の結果は消さない）')
    ap.add_argument('--only', help='手順の id（コンマ区切り）')
    ap.add_argument('--redo', action='store_true', help='--resume のファイルで FAIL や飛ばしの結果がある手順と、まだ走らせていない手順だけ走らせる')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--dry-run', action='store_true', help='案内の文を全部表示して終わる（ボードは要らない）')
    ap.add_argument('--judge-37', metavar='DIR', help='カードの退避の中身を 3.7 で判定し直して終わる')
    ap.add_argument('--check', action='store_true', help='ボードを探して退避するだけ')
    a = ap.parse_args()
    if a.list:
        for sid, title, _ in STEPS:
            print(f'{sid:12s} {title}')
        return 0
    if a.dry_run and not a.resume:
        return dry_run()
    if a.judge_37:
        n, bad = judge_card_files(a.judge_37)
        print(f'{n} files judged; not one-line JSON: {bad or "none"}')
        return 0 if not bad else 1
    os.makedirs(OUT, exist_ok=True)
    if a.resume:
        path = a.resume
        results = json.load(open(path))
        results.setdefault('resumed', []).append(datetime.datetime.now().isoformat(timespec='seconds'))
    else:
        path = os.path.join(OUT, f'guided_{hp.stamp()}.json')
        results = dict(started=datetime.datetime.now().isoformat(timespec='seconds'), results={}, steps_done=[])
    g = Guide(path, results)
    only = set(a.only.split(',')) if a.only else None
    if a.redo:
        if not a.resume:
            print('--redo は --resume と一緒に使う')
            return 2
        failed = {step_of(k, v) for k, v in results['results'].items()
                  if v['ok'] is False or (v['ok'] is None and 'exFAT' not in k and not k.startswith('3.x unplug during save: result'))}
        ran = {step_of(k, v) for k, v in results['results'].items()}
        only = {sid for sid, _, _ in STEPS if sid in failed or sid not in ran}
        g.say('やり直す手順: ' + ', '.join(sid for sid, _, _ in STEPS if sid in only))
    if only:
        unknown = only - {sid for sid, _, _ in STEPS}
        if unknown:
            print(f'知らない手順: {sorted(unknown)}（--list で一覧）')
            return 2
    if a.dry_run:          # --resume と一緒: 何を走らせるかだけ表示（ボードには触らない）
        print('走らせる手順: ' + ', '.join(sid for sid, _, _ in STEPS if not only or sid in only))
        return 0
    g.say('ボードを探している（USB のシリアルポートすべてに G を送る） ...')
    holders = {p['device']: hp.port_holders(p['device']) for p in hp.usb_ports()}
    while any(holders.values()):
        g.say(f'\n⚠ シリアルポートが、ほかのプログラムで開かれたままです: {holders}')
        g.say(f'   {CHROME_HINT}。')
        try:
            input('   -> 閉じたら Enter（q + Ctrl-C: やめる） ')
        except (EOFError, KeyboardInterrupt):
            return 2
        holders = {p['device']: hp.port_holders(p['device']) for p in hp.usb_ports()}
    g.find()
    g.show_ports()
    for p, b in g.boards.items():
        golden = os.path.join(OUT, f'golden_{p}.json')
        if not os.path.exists(golden):
            shutil.copy(hp.backup(b), golden)
        else:
            hp.backup(b)
        g.golden[p] = golden
        g.say(f'   {p} の設定を退避した。基準: {golden}')
    g.golden_G = {p: json.load(open(path_))['G'] for p, path_ in g.golden.items()}
    results['ports'] = {p: dict(device=b.device, serial=b.serial_number, ip=b.my_ip, id=b.my_id) for p, b in g.boards.items()}
    for p, b in g.boards.items():
        want = g.golden_G[p]
        dd = hp.diff(hp._strip_volatile(want), hp._strip_volatile(b.G))
        dd = [x for x in dd if 'canSendMsgBeforeDestIp' not in x]
        if dd:
            g.say(f'   {p} は基準と違う: {dd[:3]} ... 先に元に戻す')
            g.restore(p)
        b.osc_set_dest()
    g.save()
    if a.check:
        g.say('ボードを見つけ、退避し、OSC で届くことを確かめた。ほかには何もしていない。')
        return 0
    try:
        for sid, title, fn in STEPS:
            if only and sid not in only:
                continue
            if sid in results['steps_done'] and not only:
                continue
            g.head(sid, title)
            if input('   Enter = この手順を始める、s = 飛ばす、q = ここで止める: ').strip().lower() == 's':
                g.record(f'step {sid}', None, '人が飛ばした')
            else:
                try:
                    fn(g)
                except Stop as e:
                    g.say(f'\n止めた: {e}')
                    raise
            if sid not in results['steps_done']:
                results['steps_done'].append(sid)
            g.save()
    except (KeyboardInterrupt, Stop):
        g.save()
        g.say(f'\n中断した。続きは:\n  {sys.executable} {os.path.abspath(__file__)} --resume {path}')
        g.say('（設定を変える手順の途中だったら、手順 final が全部元に戻す。）')
        return 1
    n = results['results']
    g.say(f'\n終わり: 合格 {sum(1 for v in n.values() if v["ok"] is True)}, 不合格 {sum(1 for v in n.values() if v["ok"] is False)}, '
          f'飛ばし {sum(1 for v in n.values() if v["ok"] is None)}。結果のファイル: {path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
