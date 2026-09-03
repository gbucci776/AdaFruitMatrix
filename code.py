import time
import board
import terminalio
import displayio

from adafruit_display_text import label
from adafruit_matrixportal.matrixportal import MatrixPortal

matrixportal = MatrixPortal(
    status_neopixel=board.NEOPIXEL,
    color_order="RBG",
    use_wifi=False
)

display = matrixportal.display
group = displayio.Group()


def make_dot(x, y, color):
    bitmap = displayio.Bitmap(5, 5, 2)

    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = color
    palette.make_transparent(0)

    pixels = [
        (1,0), (2,0), (3,0),
        (0,1), (1,1), (2,1), (3,1), (4,1),
        (0,2), (1,2), (2,2), (3,2), (4,2),
        (0,3), (1,3), (2,3), (3,3), (4,3),
        (1,4), (2,4), (3,4)
    ]

    for px, py in pixels:
        bitmap[px, py] = 1

    return displayio.TileGrid(
        bitmap,
        pixel_shader=palette,
        x=x,
        y=y
    )


# ==========================================
# TOP LINE
#
#       Insi 🟡 ht
#            🔴
#
# Yellow/red replace the "g"
# ==========================================

group.append(
    label.Label(
        terminalio.FONT,
        text="Insi",
        color=0xFFFFFF,
        x=1,
        y=8
    )
)

# Yellow dot
group.append(
    make_dot(
        25,
        6,          
        0xFFD800
    )
)

# Red/pink dot
group.append(
    make_dot(
        25,
        11,         
        0xFF0055
    )
)

# Finish the word after the replaced "g"
group.append(
    label.Label(
        terminalio.FONT,
        text="ht",
        color=0xFFFFFF,
        x=31,
        y=8
    )
)

# ==========================================
# BOTTOM LINE
#
#       Gl 🔵 bal
#
# Blue replaces the "o"
# ==========================================

group.append(
    label.Label(
        terminalio.FONT,
        text="Gl",
        color=0xFFFFFF,
        x=8,
        y=24
    )
)

# Blue dot
group.append(
    make_dot(
        19,
        23,         
        0x55DDF2
    )
)

group.append(
    label.Label(
        terminalio.FONT,
        text="bal",
        color=0xFFFFFF,
        x=25,
        y=24
    )
)


display.root_group = group

while True:
    time.sleep(1)
