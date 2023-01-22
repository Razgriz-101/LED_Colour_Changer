import time

import colour_set as clr
import led_driver as dr

colours = clr.colours_list
colour = -1

clr = clr.colour_set

ar = dr.ar
sm = dr.sm
sw = dr.SW
LEDS = dr.LEDS


# 輝度を増減させるパターン
def blink():

    time.sleep_ms(100)

    while True:

        for x in range(20, 101, 2):  # 輝度を増加させる処理
            for j in range(LEDS):
                ar[j] = clr(*colours[colour] + (x,))
            sm.put(ar, 0)
            time.sleep_ms(20)

            if sw.value() == 0:  # スイッチ操作を監視し押された場合処理を終了する。以下同様
                return

        for _ in range(5):  # 最大輝度で維持
            if sw.value() == 0:
                return
            time.sleep_ms(100)

        for x in range(100, 19, -2):  # 輝度を減少させる処理
            for j in range(LEDS):
                ar[j] = clr(*colours[colour] + (x,))
            sm.put(ar, 0)
            time.sleep_ms(20)

            if sw.value() == 0:
                return


# 色が流れるように輝度を変更するパターン
def wave():

    time.sleep_ms(100)

    while True:

        for j in range(20, 201, 20):  # 輝度を20%から20刻みで100％まで上げる処理をLED1個ずつ遅らせて行う

            x = j
            if x > 100:
                x = 100

            for n in range(4, -1, -1):
                for m in range(3):
                    ar[n + m * 5] = ar[n-1]
                    if n == 0:
                        ar[n + m * 5] = clr(*colours[colour] + (x,))

            sm.put(ar, 0)
            time.sleep_ms(50)

            if sw.value() == 0:
                return

        for _ in range(3):  # 最大輝度で維持
            if sw.value() == 0:
                return
            time.sleep_ms(50)

        for j in range(200, 19, -20):  # 輝度を100%から20刻みで20％まで下げる処理をLED1個ずつ遅らせて行う

            x = j
            if x > 100:
                x = 100

            for n in range(4, -1, -1):
                for m in range(3):
                    ar[n + m * 5] = ar[n-1]
                    if n == 0:
                        ar[n + m * 5] = clr(*colours[colour] + (x,))

            sm.put(ar, 0)
            time.sleep_ms(50)

            if sw.value() == 0:
                return


# 輝度を固定するパターン
def flat():

    for j in range(LEDS):  # すべてのLEDを同色・同輝度で発光させる
        ar[j] = clr(*colours[colour])
    sm.put(ar, 0)

    while True:

        if sw.value() == 0:  # スイッチ操作を監視し押された場合処理を終了する
            return


# 発光パターンの切り替えを行う。
# この関数から各発光パターンを呼び出す。
def switcher():
    global ar
    global colour

    sw_cnt = 0
    pattern = 0
    colour = -1
    patterns = [flat, wave, blink]

    while True:

        time.sleep_ms(100)

        if sw_cnt == 9:  # スイッチを約1秒長押しすることで次の条件分岐へ移行する
            for j in range(LEDS):  # LEDを弱発光させ条件分岐へ移行したことを知らせる
                ar[LEDS - 1 - j] = clr(*colours[j % len(colours)] + (5,))
            sm.put(ar, 0)

            time.sleep_ms(700)

            if sw.value() == 0:  # 条件分岐開始からスイッチを離さなければ「single.py」を終了させる

                for j in range(LEDS):  # 弱発光しているLEDを最大輝度にしモード移行を知らせる
                    ar[LEDS - 1 - j] = clr(*colours[j % len(colours)])
                    sm.put(ar, 0)
                    time.sleep_ms(20)

                time.sleep_ms(500)

                return 1

            else:  # 条件分岐開始から約0.7秒以内にスイッチを離すことで「sw_cnt」を初期化したのち発光パターンを変更する
                sw_cnt = 0

                for j in range(LEDS):  # LEDを消灯することで発光パターンを変更すること知らせる
                    ar[j] = 0
                sm.put(ar, 0)

                pattern = (pattern + 1) % len(patterns)
                patterns[pattern]()  # 変更した発光パターンでLEDを制御する

                for j in range(LEDS):  # LEDを消灯させ、スイッチが押されていることを知らせる
                    ar[j] = 0
                sm.put(ar, 0)

        elif sw.value() == 0:  # スイッチが押されている場合「sw_cnt」に「1」を加算する
            sw_cnt += 1

        else:  # 「sw_cnt」を初期化し発光色を変更する
            sw_cnt = 0
            colour = (colour + 1) % len(colours)
            patterns[pattern]()  # 変更した色でLEDを制御する

            for j in range(LEDS):  # LEDを消灯させ、スイッチが押されていることを知らせる
                ar[j] = 0
            sm.put(ar, 0)
