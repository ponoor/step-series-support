## 電磁ブレーキとは
ステッピングモータの中には電磁ブレーキが取り付けられているものがあります。ステッピングモータは通常、停止時にも保持トルクがあり負荷を保持できますが、停電などで電源が落ちた場合には保持力がなくなり、負荷を吊り下げている場合には負荷が落下してしまいます。 電磁ブレーキはモータの軸をロックする装置で、通電しているときだけ軸が解放されますので、予期しない電源断が発生した場合にただちに軸がロックされ、負荷が動いたり落下したりするのを防ぎます。特に負荷を上下に移動させる場合には必要です。

## 電磁ブレーキの動作タイミング
電磁ブレーキの電源を切ると軸がロックされますが、ブレーキ機構が物理的に動作する時間が必要ですので、その間に負荷が動かないようにモータの励磁を切るまでに、モータ、ブレーキ双方がオーバーラップして保持する時間 (brakeTransitionDuration) を置く必要があります。このオーバーラップ時間はブレーキがかかるまでの時間には影響しませんが、ブレーキ操作の後、モータを動作・解放させるまでの待ち時間に影響します。STEP400ではこのオーバーラップ時間の初期値は100ms(0.1秒)になっていますが、`/setBrakeTransitionDuration` コマンドや初期設定ツールで変更できます。
モータを励磁して電磁ブレーキを開放する際にも同じオーバーラップ時間を設けています。

[![Brake Transition Duration](https://ponoor.com/cms/wp-content/uploads/2021/03/brakeTransition.png)](https://ponoor.com/cms/wp-content/uploads/2021/03/brakeTransition.png)

## 電磁ブレーキのついたステッピングモータの例

<a href="https://ponoor.com/cms/wp-content/uploads/2021/03/nema-23-stepper-19nm269ozin-w-brake-friction-torque-20nm283ozin-52372-1000x1000-1.jpg"><img src="https://ponoor.com/cms/wp-content/uploads/2021/03/nema-23-stepper-19nm269ozin-w-brake-friction-torque-20nm283ozin-52372-1000x1000-1.jpg" width="500"></a>

[STEPPER ONLINE](https://www.omc-stepperonline.com/stepper-motor-brake/nema-23-stepper-19nm269ozin-w-brake-friction-torque-20nm283ozin-23hs30-2804d-b200.html)

[![](https://ponoor.com/cms/wp-content/uploads/2021/03/pkp243d-700x525.jpg)](https://ponoor.com/cms/wp-content/uploads/2021/03/pkp243d.jpg)

[Orientalmotor](https://www.orientalmotor.co.jp/) PKP243D23M2