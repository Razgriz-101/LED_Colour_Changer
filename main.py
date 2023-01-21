import time

import led_driver as dr
import multi
import single


# マルチカラーモードを初期設定とし実行
def led_func():

    mode = 0
    modes = [multi, single]

    while True:

        time.sleep_ms(100)
        for j in range(dr.LEDS):  # LEDを消灯させる
            dr.ar[j] = 0
        dr.sm.put(dr.ar, 0)
        time.sleep_ms(100)

        mode = (mode + modes[mode % len(modes)].switcher()) % len(modes)
        # 各モード終了時に'1'を返すことで'mode'の値を'modes'のインデックス内で切り替える


if __name__ == "__main__":

    led_func()
