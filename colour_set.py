# colour set : clr(r, g, b, w, lum) | [r, g, b, w => 0~255],[lum (輝度:デフォルト100%) => 0~100]

def colour_set(r=0, g=0, b=0, w=0, lum=100):
    return (g * lum // 100 * 16777216
            + r * lum // 100 * 65536
            + b * lum // 100 * 256
            + w * lum // 100)


# デフォルトの色を設定
w = (0, 0, 0, 110)
b = (0, 0, 255, 0)
g = (0, 255, 0, 0)
p = (123, 50, 73, 0)
v = (45, 0, 255, 0)
r = (255, 0, 0, 0)
c = (0, 100, 255, 0)

colours_list = [w, b, p, v, c]
seven_colours = [v, w, p, r, b, g, c]


red         = (255, 0, 0, 0)
green       = (0, 255, 0, 0)
blue        = (0, 0, 255, 0)
cyan        = (0, 255, 255, 0)
magenta     = (255, 0, 255, 0)
yellow      = (255, 255, 0, 0)
white_rgb   = (255, 255, 255, 0)
white       = (0, 0, 0, 255)
all_colours = (255, 255, 255, 255)

colours = [red, green, blue, cyan, magenta, yellow, white_rgb, white, all_colours]
