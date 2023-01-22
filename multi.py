import time

import colour_set as clr
import led_driver as dr

colours = clr.colours_list
svn_colours = clr.seven_colours

clr = clr.colour_set

ar = dr.ar
sm = dr.sm
sw = dr.SW
LEDS = dr.LEDS


# 輝度を増減させたのち色を切り替えるパターン

def cycle_colours():

    time.sleep_ms(100)

    while True:

        for i in range(len(colours)):
            for x in range(20, 101, 2):  # 増光処理
                for j in range(LEDS):
                    ar[j] = clr(*colours[i] + (x,))
                sm.put(ar, 0)
                time.sleep_ms(20)

                if sw.value() == 0:  # スイッチ操作を監視し押された場合処理を終了する。以下同様
                    return

            for _ in range(5):  # 最大輝度で維持
                if sw.value() == 0:
                    return
                time.sleep_ms(100)

            for x in range(100, 19, -2):  # 減光処理
                for j in range(LEDS):
                    ar[j] = clr(*colours[i] + (x,))
                sm.put(ar, 0)
                time.sleep_ms(20)

                if sw.value() == 0:
                    return


# 色が流れるように輝度を変えるパターン
def wave_colours():

    time.sleep_ms(100)

    while True:

        for i in range(len(colours)):
            for j in range(20, 201, 20):  # 輝度を20%から20刻みで100％まで上げる処理をLED1個ずつ遅らせて行う

                x = j
                if x > 100:
                    x = 100

                for n in range(4, -1, -1):
                    for m in range(3):
                        ar[n + m * 5] = ar[n-1]
                        if n == 0:
                            ar[n + m * 5] = clr(*colours[i] + (x,))

                sm.put(ar, 0)
                time.sleep_ms(50)

                if sw.value() == 0:
                    return

            for _ in range(5):  # 最大輝度で維持
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
                            ar[n + m * 5] = clr(*colours[i] + (x,))

                sm.put(ar, 0)
                time.sleep_ms(50)

                if sw.value() == 0:
                    return


# 設定色から3色をLED1列ずつ発行させ順番に色を切り替えるパターン
def rotation_colours():

    time.sleep_ms(100)

    while True:

        for i in range(len(colours)):
            for x in range(20, 101, 5):  # cycle_coloursに似た増光処理
                for j in range(5):
                    y = i+1
                    z = i+2
                    if y > 4:
                        y -= 5
                    if z > 4:
                        z -= 5
                    ar[j] = clr(*colours[i] + (x,))
                    ar[j+5] = clr(*colours[y] + (x,))  # LEDは1列に5個設置しているため変数「j」に「5」を足していく
                    ar[j+10] = clr(*colours[z] + (x,))

                sm.put(ar, 0)
                time.sleep_ms(30)

                if sw.value() == 0:
                    return

            for _ in range(5):  # 最大輝度を維持
                if sw.value() == 0:
                    return
                time.sleep_ms(100)

            for x in range(100, 19, -5):  # 減光処理
                for j in range(5):
                    y = i+1
                    z = i+2
                    if y > 4:
                        y -= 5
                    if z > 4:
                        z -= 5
                    ar[j] = clr(*colours[i] + (x,))
                    ar[j+5] = clr(*colours[y] + (x,))
                    ar[j+10] = clr(*colours[z] + (x,))

                sm.put(ar, 0)
                time.sleep_ms(30)

                if sw.value() == 0:
                    return


# 設定した7色をcycle_coloursと同様に輝度を増減させて発光色を切り替える
def seven_colours():

    for i in range(7):
        for x in range(20, 101, 4):  # 増光処理
            for j in range(LEDS):
                ar[j] = clr(*svn_colours[i] + (x,))
            sm.put(ar, 0)
            time.sleep_ms(12)

        for x in range(100, 19, -4):  # 減光処理
            for j in range(LEDS):
                ar[j] = clr(*svn_colours[i] + (x,))
            sm.put(ar, 0)
            time.sleep_ms(12)

    for j in range(LEDS):  # LEDを消灯し1秒ほど間を空ける
        ar[j] = 0
    sm.put(ar, 0)
    time.sleep_ms(1000)
    return 0


# 発光パターンの切り替えを行う
# この関数から各発光パターンを呼び出す
def switcher():
    global ar

    sw_cnt = 0
    pattern = -1

    cc = cycle_colours
    wc = wave_colours
    rc = rotation_colours

    patterns = [wc, cc, rc]

    while True:

        time.sleep_ms(100)

        if sw_cnt == 9:  # スイッチを約1秒長押しすることで次の条件分岐へ移行する
            for j in range(LEDS):  # LEDを弱発光させ条件分岐へ移行したことを知らせる
                ar[LEDS - 1 - j] = clr(*colours[j % len(colours)] + (5,))
            sm.put(ar, 0)

            time.sleep_ms(700)

            if sw.value() == 0:  # 条件分岐開始からスイッチを離さなければ「multi.py」を終了させる

                for j in range(LEDS):  # 弱発光しているLEDを最大輝度にしモード移行を知らせる
                    ar[LEDS - 1 - j] = clr(*colours[j % len(colours)])
                    sm.put(ar, 0)
                    time.sleep_ms(20)

                time.sleep_ms(500)

                return 1

            else:  # 条件分岐開始から約0.7秒以内にスイッチを離すことで七色サイクル(seven_colours)の実行待機へ移行する
                sw_cnt = 0

                for j in range(LEDS):  # LEDを消灯することで七色サイクル待機状態へ移行したことを知らせる
                    ar[j] = 0
                sm.put(ar, 0)

                while True:

                    if sw.value() == 0:  # スイッチを押してから離すまでの時間で動作を変更する

                        while True:

                            time.sleep_ms(50)

                            if sw_cnt == 39:  # スイッチを約2秒間押し続けることで七色サイクルをキャンセルする
                                for j in range(LEDS):  # LEDを弱発光させキャンセルされたことをしらせる
                                    ar[LEDS - 1 - j] = clr(*colours[j % len(colours)] + (5,))
                                sm.put(ar, 0)
                                pattern -= 1
                                time.sleep_ms(500)
                                break

                            elif sw.value() == 0:  # スイッチが押されている場合「sw_cnt」に「1」を加算する
                                sw_cnt += 1

                            else:  # スイッチが離されたら「sw_cnt」を初期化し　七色サイクルを実行する
                                sw_cnt = 0
                                pattern -= 1
                                seven_colours()
                                break

                        break

        elif sw.value() == 0:  # スイッチが押されている場合「sw_cnt」に「1」を加算する
            sw_cnt += 1

        else:  # 「sw_cnt」を初期化し次の発光パターンを実行する
            sw_cnt = 0
            pattern = (pattern + 1) % (len(patterns))
            patterns[pattern]()  # 変更した発光パターンでLEDを制御する

            for j in range(LEDS):  # LEDを消灯させ、スイッチが押されていることを知らせる
                ar[j] = 0
            sm.put(ar, 0)
