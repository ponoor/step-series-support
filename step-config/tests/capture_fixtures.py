"""Save real answers of the boards (G, T, and the lines after R) to fixtures/real/.
They contain individual values (MAC address, IP) of the bench boards; the repository is public."""
import json
import os

import hw_protocol as hw


def capture():
    os.makedirs(hw.FIXTURES, exist_ok=True)
    for prod, b in sorted(hw.find_boards().items()):
        d = hw.FIXTURES
        out = {}
        with b.line() as ln:
            out['G'] = ln.get_config()
            out['T'] = ln.get_status()
            # the exact bytes of G and T, to compare the number formats
            ln.drain(0.05)
            ln.send(b'G')
            out['G_raw'] = ln.drain(0.5).decode()
            ln.send(b'T')
            out['T_raw'] = ln.drain(0.5).decode()
        res = hw.reboot_and_wait(b)
        out['reboot'] = {k: v for k, v in res.items() if k != 'T'}
        out['T_after_reboot'] = res['T']
        with open(os.path.join(d, f'{prod}_sd_ok.json'), 'w') as f:
            json.dump(out, f, indent=1)
        print(prod, 'saved', {k: res[k] for k in ('reply', 'gone', 'back', 'opened', 't_answers')})
        print('  startup lines:', res['startup_lines'], repr(res['pre'][:200]))
