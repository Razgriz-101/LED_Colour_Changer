import array
from machine import Pin
import rp2

LEDS = 15
PIN_NUMBER = 26


@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW,
             out_shiftdir=rp2.PIO.SHIFT_LEFT,
             autopull=True,
             pull_thresh=32)
def driver():
    t1 = 2
    t2 = 3
    t3 = 5
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)[t3 - 1]
    jmp(not_x, "do_zero")   .side(1)[t1 - 1]
    jmp("bitloop")          .side(1)[t2 - 1]
    label("do_zero")
    nop()                   .side(0)[t2 - 1]
    wrap()


# 発光パターン切り替えスイッチの設定
SW = Pin(1, Pin.IN, Pin.PULL_UP)

# Create the StateMachine with the driver program, outputting on Pin(PIN_NUMBER).
sm = rp2.StateMachine(0, driver, freq=8_000_000, sideset_base=Pin(PIN_NUMBER))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(LEDS)])
