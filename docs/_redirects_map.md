# Redirect map: old URL -> new page

Old URLs come from `wp_export/` (the WordPress export). The new page is `docs/<lang>/<path>.md`; the URL depends on where the site is published (undecided). Redirect settings are not made yet.
Anchors of the old pages are not kept (the new anchors are made from the command address only).

| Language | Old URL | Old title | New page | Old file in wp_export |
|---|---|---|---|---|
| en | `/en/docs/emb-step400/` | Electromagnetic brake board for STEP400 | `en/hardware/emb-step400.md` | `wp_export/en/docs/emb-step400.md` |
| en | `/en/docs/emb-step400/commands/` | Sending command | `en/guides/electromagnetic-brake.md` | `wp_export/en/docs/emb-step400/commands.md` |
| en | `/en/docs/emb-step400/connection/` | Wiring | `en/connections/electromagnetic-brake-wiring.md` | `wp_export/en/docs/emb-step400/connection.md` |
| en | `/en/docs/emb-step400/howtowork/` | Electromagnetic brake operation | `en/guides/electromagnetic-brake.md` | `wp_export/en/docs/emb-step400/howtowork.md` |
| en | `/en/docs/emb-step400/specifications/` | Specifications | `en/hardware/emb-step400.md` | `wp_export/en/docs/emb-step400/specifications.md` |
| en | `/en/docs/step-series/` | STEP400/800 | `en/index.md` | `wp_export/en/docs/step-series.md` |
| en | `/en/docs/step-series/functional-description/` | Functional descriptions | `en/guides/index.md` | `wp_export/en/docs/step-series/functional-description.md` |
| en | `/en/docs/step-series/functional-description/homing-and-position-management/` | Homing and position management | `en/guides/homing-and-position.md` | `wp_export/en/docs/step-series/functional-description/homing-and-position-management.md` |
| en | `/en/docs/step-series/functional-description/servo-mode/` | Servo mode | `en/guides/servo-mode.md` | `wp_export/en/docs/step-series/functional-description/servo-mode.md` |
| en | `/en/docs/step-series/functional-description/speed-profile-and-type-of-motor-motions/` | Speed profile and types of motor motion | `en/guides/speed-profile-and-motions.md` | `wp_export/en/docs/step-series/functional-description/speed-profile-and-type-of-motor-motions.md` |
| en | `/en/docs/step-series/functional-description/voltage-mode-and-current-mode/` | Voltage mode and current mode | `en/guides/voltage-and-current-mode.md` | `wp_export/en/docs/step-series/functional-description/voltage-mode-and-current-mode.md` |
| en | `/en/docs/step-series/osc-command-reference/` | OSC command reference | `en/reference/index.md` | `wp_export/en/docs/step-series/osc-command-reference.md` |
| en | `/en/docs/step-series/osc-command-reference/alarm-settings/` | Alarm settings | `en/reference/alarm-settings.md` | `wp_export/en/docs/step-series/osc-command-reference/alarm-settings.md` |
| en | `/en/docs/step-series/osc-command-reference/automatically-sent-messages-from-step-400/` | Automatically sent messages from the device | `en/reference/automatically-sent-messages.md` | `wp_export/en/docs/step-series/osc-command-reference/automatically-sent-messages-from-step-400.md` |
| en | `/en/docs/step-series/osc-command-reference/brake/` | Electromagnet brake | `en/reference/brake.md` | `wp_export/en/docs/step-series/osc-command-reference/brake.md` |
| en | `/en/docs/step-series/osc-command-reference/differences-between-step400-and-step800/` | Differences between STEP400 and STEP800 | `en/reference/differences-step400-step800.md` | `wp_export/en/docs/step-series/osc-command-reference/differences-between-step400-and-step800.md` |
| en | `/en/docs/step-series/osc-command-reference/home-and-limit-sensers/` | HOME and LIMIT sensers | `en/reference/home-and-limit-sensors.md` | `wp_export/en/docs/step-series/osc-command-reference/home-and-limit-sensers.md` |
| en | `/en/docs/step-series/osc-command-reference/homing/` | Homing | `en/reference/homing.md` | `wp_export/en/docs/step-series/osc-command-reference/homing.md` |
| en | `/en/docs/step-series/osc-command-reference/motor-control/` | Motor control | `en/reference/motor-control.md` | `wp_export/en/docs/step-series/osc-command-reference/motor-control.md` |
| en | `/en/docs/step-series/osc-command-reference/motor-driver-settings/` | Motor driver settings | `en/reference/motor-driver-settings.md` | `wp_export/en/docs/step-series/osc-command-reference/motor-driver-settings.md` |
| en | `/en/docs/step-series/osc-command-reference/position-management/` | Position management | `en/reference/position-management.md` | `wp_export/en/docs/step-series/osc-command-reference/position-management.md` |
| en | `/en/docs/step-series/osc-command-reference/servo-mode/` | Servo mode | `en/reference/servo-mode_reference.md` | `wp_export/en/docs/step-series/osc-command-reference/servo-mode.md` |
| en | `/en/docs/step-series/osc-command-reference/speed-profile/` | Speed profile | `en/reference/speed-profile.md` | `wp_export/en/docs/step-series/osc-command-reference/speed-profile.md` |
| en | `/en/docs/step-series/osc-command-reference/system-settings/` | System settings | `en/reference/system-settings.md` | `wp_export/en/docs/step-series/osc-command-reference/system-settings.md` |
| en | `/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/` | Voltage and current mode settings | `en/reference/voltage-and-current-mode-settings.md` | `wp_export/en/docs/step-series/osc-command-reference/voltage-and-current-mode-settings.md` |
| en | `/en/docs/step-series/settings/` | Connections and settings | `en/connections/index.md` | `wp_export/en/docs/step-series/settings.md` |
| en | `/en/docs/step-series/settings/example-parameter-values-for-example-steppers/` | Example parameter values for example steppers | `en/connections/example-parameters.md` | `wp_export/en/docs/step-series/settings/example-parameter-values-for-example-steppers.md` |
| en | `/en/docs/step-series/settings/network-and-dip-switch/` | Network and the DIP switch | `en/connections/network-and-dip-switch.md` | `wp_export/en/docs/step-series/settings/network-and-dip-switch.md` |
| en | `/en/docs/step-series/settings/power-supply-and-motor/` | Power supply and Motor | `en/connections/power-supply-and-motor.md` | `wp_export/en/docs/step-series/settings/power-supply-and-motor.md` |
| en | `/en/docs/step-series/settings/sensor-and-switch/` | Sensor and Switch | `en/connections/sensors-and-switches.md` | `wp_export/en/docs/step-series/settings/sensor-and-switch.md` |
| en | `/en/docs/step-series/settings/setup-with-a-microsd-card/` | Setup with a microSD card | `en/connections/microsd-card.md` | `wp_export/en/docs/step-series/settings/setup-with-a-microsd-card.md` |
| en | `/en/docs/step-series/technical-information/` | Technical information | `en/maintenance/index.md` | `wp_export/en/docs/step-series/technical-information.md` |
| en | `/en/docs/step-series/technical-information/compile-the-arduino-sketch/` | Compiling the Arduino sketch | `en/maintenance/compile-the-arduino-sketch.md` | `wp_export/en/docs/step-series/technical-information/compile-the-arduino-sketch.md` |
| en | `/en/docs/step-series/technical-information/diagnosis/` | Diagnosis via USB serial port | `en/maintenance/usb-serial-diagnosis.md` | `wp_export/en/docs/step-series/technical-information/diagnosis.md` |
| en | `/en/docs/step-series/technical-information/firmware-update/` | The firmware update | `en/maintenance/firmware-update.md` | `wp_export/en/docs/step-series/technical-information/firmware-update.md` |
| en | `/en/docs/step-series/technical-information/hardware-step400/` | Hardware – STEP400 | `en/hardware/step400.md` | `wp_export/en/docs/step-series/technical-information/hardware-step400.md` |
| en | `/en/docs/step-series/technical-information/hardware-step800/` | Hardware – STEP800 | `en/hardware/step800.md` | `wp_export/en/docs/step-series/technical-information/hardware-step800.md` |
| en | `/en/docs/step-series/tutorial/` | Tutorial | `en/getting-started/quickstart.md` | `wp_export/en/docs/step-series/tutorial.md` |
| en | `/en/docs/step100-200/` | STEP100/200 | `en/step100-200/index.md` | `wp_export/en/docs/step100-200.md` |
| en | `/en/docs/step100-200/assemble/` | Assemble | `en/step100-200/assemble/index.md` | `wp_export/en/docs/step100-200/assemble.md` |
| en | `/en/docs/step100-200/assemble/connections/` | Connections | `en/step100-200/assemble/connections.md` | `wp_export/en/docs/step100-200/assemble/connections.md` |
| en | `/en/docs/step100-200/assemble/step100/` | Prepare X-Nucleo – STEP100 | `en/step100-200/assemble/step100.md` | `wp_export/en/docs/step100-200/assemble/step100.md` |
| en | `/en/docs/step100-200/assemble/step200/` | Prepare X-Nucleo – STEP200 | `en/step100-200/assemble/step200.md` | `wp_export/en/docs/step100-200/assemble/step200.md` |
| en | `/en/docs/step100-200/get-the-materials/` | Get the materials | `en/step100-200/get-the-materials.md` | `wp_export/en/docs/step100-200/get-the-materials.md` |
| en | `/en/docs/step100-200/upload-the-sketch/` | Upload the Arduino sketch | `en/step100-200/upload-the-sketch.md` | `wp_export/en/docs/step100-200/upload-the-sketch.md` |
| en | `/en/docs/step100-200/usage/` | Usage | `en/step100-200/usage.md` | `wp_export/en/docs/step100-200/usage.md` |
| ja | `/docs/emb-step400/` | 電磁ブレーキ基板 for STEP400 | `ja/hardware/emb-step400.md` | `wp_export/ja/docs/emb-step400.md` |
| ja | `/docs/emb-step400/commands/` | コマンドの送り方 | `ja/guides/electromagnetic-brake.md` | `wp_export/ja/docs/emb-step400/commands.md` |
| ja | `/docs/emb-step400/connection/` | 接続 | `ja/connections/electromagnetic-brake-wiring.md` | `wp_export/ja/docs/emb-step400/connection.md` |
| ja | `/docs/emb-step400/howtowork/` | 電磁ブレーキの動作 | `ja/guides/electromagnetic-brake.md` | `wp_export/ja/docs/emb-step400/howtowork.md` |
| ja | `/docs/emb-step400/specifications/` | 仕様 | `ja/hardware/emb-step400.md` | `wp_export/ja/docs/emb-step400/specifications.md` |
| ja | `/docs/step-series/` | STEP400/800 | `ja/index.md` | `wp_export/ja/docs/step-series.md` |
| ja | `/docs/step-series/functional-description/` | 機能解説 | `ja/guides/index.md` | `wp_export/ja/docs/step-series/functional-description.md` |
| ja | `/docs/step-series/functional-description/homing-and-position-management/` | 原点復帰と座標管理 | `ja/guides/homing-and-position.md` | `wp_export/ja/docs/step-series/functional-description/homing-and-position-management.md` |
| ja | `/docs/step-series/functional-description/servo-mode/` | サーボモード | `ja/guides/servo-mode.md` | `wp_export/ja/docs/step-series/functional-description/servo-mode.md` |
| ja | `/docs/step-series/functional-description/speed-profile-and-type-of-motor-motions/` | スピードプロファイルとモータ動作の種類 | `ja/guides/speed-profile-and-motions.md` | `wp_export/ja/docs/step-series/functional-description/speed-profile-and-type-of-motor-motions.md` |
| ja | `/docs/step-series/functional-description/voltage-mode-and-current-mode/` | 電圧制御と電流制御 | `ja/guides/voltage-and-current-mode.md` | `wp_export/ja/docs/step-series/functional-description/voltage-mode-and-current-mode.md` |
| ja | `/docs/step-series/osc-command-reference/` | OSCコマンドリファレンス | `ja/reference/index.md` | `wp_export/ja/docs/step-series/osc-command-reference.md` |
| ja | `/docs/step-series/osc-command-reference/absolute-position-management/` | 座標 | `ja/reference/position-management.md` | `wp_export/ja/docs/step-series/osc-command-reference/absolute-position-management.md` |
| ja | `/docs/step-series/osc-command-reference/alarm-settings/` | アラーム | `ja/reference/alarm-settings.md` | `wp_export/ja/docs/step-series/osc-command-reference/alarm-settings.md` |
| ja | `/docs/step-series/osc-command-reference/automatically-sent-messages-from-step-400/` | 自動送信されるメッセージ | `ja/reference/automatically-sent-messages.md` | `wp_export/ja/docs/step-series/osc-command-reference/automatically-sent-messages-from-step-400.md` |
| ja | `/docs/step-series/osc-command-reference/brake/` | 電磁ブレーキ | `ja/reference/brake.md` | `wp_export/ja/docs/step-series/osc-command-reference/brake.md` |
| ja | `/docs/step-series/osc-command-reference/diff_400_800_command/` | STEP400とSTEP800で異なる部分 | `ja/reference/differences-step400-step800.md` | `wp_export/ja/docs/step-series/osc-command-reference/diff_400_800_command.md` |
| ja | `/docs/step-series/osc-command-reference/home-limit-sensors/` | HOME/LIMITセンサ | `ja/reference/home-and-limit-sensors.md` | `wp_export/ja/docs/step-series/osc-command-reference/home-limit-sensors.md` |
| ja | `/docs/step-series/osc-command-reference/homing/` | 原点復帰 | `ja/reference/homing.md` | `wp_export/ja/docs/step-series/osc-command-reference/homing.md` |
| ja | `/docs/step-series/osc-command-reference/motor-control/` | モータの回転・停止 | `ja/reference/motor-control.md` | `wp_export/ja/docs/step-series/osc-command-reference/motor-control.md` |
| ja | `/docs/step-series/osc-command-reference/motordriver-settings/` | モータドライバの設定 | `ja/reference/motor-driver-settings.md` | `wp_export/ja/docs/step-series/osc-command-reference/motordriver-settings.md` |
| ja | `/docs/step-series/osc-command-reference/servo-mode/` | サーボモード | `ja/reference/servo-mode_reference.md` | `wp_export/ja/docs/step-series/osc-command-reference/servo-mode.md` |
| ja | `/docs/step-series/osc-command-reference/speed-profile/` | スピードプロファイル | `ja/reference/speed-profile.md` | `wp_export/ja/docs/step-series/osc-command-reference/speed-profile.md` |
| ja | `/docs/step-series/osc-command-reference/system-settings/` | 基板全体の設定 | `ja/reference/system-settings.md` | `wp_export/ja/docs/step-series/osc-command-reference/system-settings.md` |
| ja | `/docs/step-series/osc-command-reference/voltage-and-current-mode-settings/` | 電圧モード、電流モードの設定 | `ja/reference/voltage-and-current-mode-settings.md` | `wp_export/ja/docs/step-series/osc-command-reference/voltage-and-current-mode-settings.md` |
| ja | `/docs/step-series/settings/` | 接続と設定 | `ja/connections/index.md` | `wp_export/ja/docs/step-series/settings.md` |
| ja | `/docs/step-series/settings/example-parameter-values-for-example-steppers/` | モータ毎のパラメータの例 | `ja/connections/example-parameters.md` | `wp_export/ja/docs/step-series/settings/example-parameter-values-for-example-steppers.md` |
| ja | `/docs/step-series/settings/network-and-dip-switch/` | ネットワークとDIPスイッチの設定 | `ja/connections/network-and-dip-switch.md` | `wp_export/ja/docs/step-series/settings/network-and-dip-switch.md` |
| ja | `/docs/step-series/settings/power-supply-and-motor/` | 電源とモータの選定 | `ja/connections/power-supply-and-motor.md` | `wp_export/ja/docs/step-series/settings/power-supply-and-motor.md` |
| ja | `/docs/step-series/settings/sensor-and-switch/` | センサとスイッチの接続 | `ja/connections/sensors-and-switches.md` | `wp_export/ja/docs/step-series/settings/sensor-and-switch.md` |
| ja | `/docs/step-series/settings/setup-with-a-microsd-card/` | microSDを用いた設定 | `ja/connections/microsd-card.md` | `wp_export/ja/docs/step-series/settings/setup-with-a-microsd-card.md` |
| ja | `/docs/step-series/technical-information/` | 技術情報 | `ja/maintenance/index.md` | `wp_export/ja/docs/step-series/technical-information.md` |
| ja | `/docs/step-series/technical-information/compile-the-arduino-sketch/` | Arduinoスケッチのコンパイル | `ja/maintenance/compile-the-arduino-sketch.md` | `wp_export/ja/docs/step-series/technical-information/compile-the-arduino-sketch.md` |
| ja | `/docs/step-series/technical-information/diagnosis/` | USBシリアルからの診断 | `ja/maintenance/usb-serial-diagnosis.md` | `wp_export/ja/docs/step-series/technical-information/diagnosis.md` |
| ja | `/docs/step-series/technical-information/firmware-update/` | ファームウェアのアップデート | `ja/maintenance/firmware-update.md` | `wp_export/ja/docs/step-series/technical-information/firmware-update.md` |
| ja | `/docs/step-series/technical-information/hardware-step400/` | ハードウェア-STEP400 | `ja/hardware/step400.md` | `wp_export/ja/docs/step-series/technical-information/hardware-step400.md` |
| ja | `/docs/step-series/technical-information/hardware-step800/` | ハードウェア-STEP800 | `ja/hardware/step800.md` | `wp_export/ja/docs/step-series/technical-information/hardware-step800.md` |
| ja | `/docs/step-series/tutorial/` | チュートリアル | `ja/getting-started/quickstart.md` | `wp_export/ja/docs/step-series/tutorial.md` |
| ja | `/docs/step100-200/` | STEP100/200 | `ja/step100-200/index.md` | `wp_export/ja/docs/step100-200.md` |
| ja | `/docs/step100-200/assemble/` | 組み立て | `ja/step100-200/assemble/index.md` | `wp_export/ja/docs/step100-200/assemble.md` |
| ja | `/docs/step100-200/assemble/connections/` | 接続 | `ja/step100-200/assemble/connections.md` | `wp_export/ja/docs/step100-200/assemble/connections.md` |
| ja | `/docs/step100-200/assemble/step100/` | X-Nucleoの事前準備 – STEP100 | `ja/step100-200/assemble/step100.md` | `wp_export/ja/docs/step100-200/assemble/step100.md` |
| ja | `/docs/step100-200/assemble/step200/` | X-Nucleoの事前準備 – STEP200 | `ja/step100-200/assemble/step200.md` | `wp_export/ja/docs/step100-200/assemble/step200.md` |
| ja | `/docs/step100-200/get-the-materials/` | 材料を手に入れる | `ja/step100-200/get-the-materials.md` | `wp_export/ja/docs/step100-200/get-the-materials.md` |
| ja | `/docs/step100-200/upload-the-sketch/` | Arduinoスケッチの書き込み | `ja/step100-200/upload-the-sketch.md` | `wp_export/ja/docs/step100-200/upload-the-sketch.md` |
| ja | `/docs/step100-200/usage/` | 使い方 | `ja/step100-200/usage.md` | `wp_export/ja/docs/step100-200/usage.md` |

92 old URLs mapped (en 46, ja 46).

