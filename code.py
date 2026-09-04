import time
import board
import terminalio
import displayio

from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.matrixportal import MatrixPortal

# global font
FONT = bitmap_font.load_font("/fonts/HaxorNarrow-16.bdf")

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

def make_big_dot(x, y, color):
    bitmap = displayio.Bitmap(6, 6, 2)

    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = color
    palette.make_transparent(0)

    pixels = [
        (1,0), (2,0), (3,0), (4,0),

        (0,1), (1,1), (2,1), (3,1), (4,1), (5,1),
        (0,2), (1,2), (2,2), (3,2), (4,2), (5,2),
        (0,3), (1,3), (2,3), (3,3), (4,3), (5,3),
        (0,4), (1,4), (2,4), (3,4), (4,4), (5,4),

        (1,5), (2,5), (3,5), (4,5)
    ]

    for px, py in pixels:
        bitmap[px, py] = 1

    return displayio.TileGrid(
        bitmap,
        pixel_shader=palette,
        x=x,
        y=y
    )

def make_snowflake(x, y, color):
    bitmap = displayio.Bitmap(1, 1, 2)

    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = color
    palette.make_transparent(0)

    bitmap[0, 0] = 1

    tile = displayio.TileGrid(
        bitmap,
        pixel_shader=palette,
        x=x,
        y=y
    )

    return tile, palette


# ==========================================
# TOP LINE
# ==========================================

group.append(
    label.Label(
        FONT,
        text="Insi",
        color=0xFFFFFF,
        x=1,
        y=8
    )
)

# Yellow dot
group.append(
    make_dot(
        36,         # was 34 → RIGHT 2
        6,
        0xFFD800
    )
)

group.append(
    make_dot(
        36,        
        11,
        0xFF0055
    )
)

group.append(
    label.Label(
        FONT,
        text="ht",
        color=0xFFFFFF,
        x=43,       
        y=8
    )
)
# ==========================================
# BOTTOM LINE
# ==========================================

# "Gl" — DON'T MOVE
group.append(
    label.Label(
        FONT,
        text="Gl",
        color=0xFFFFFF,
        x=8,
        y=24
    )
)

group.append(
    make_big_dot(
        24,
        22,         
        0x55DDF2
    )
)

group.append(
    label.Label(
        FONT,
        text="bal",
        color=0xFFFFFF,
        x=32,       
        y=24
    )
)

# ==========================================
# RAINBOW SNOWFLAKES
# ==========================================

snowflake_data = [
    # TOP EDGE
    (2, 1,  0xFF0000),   # red
    (12, 2, 0xFF8800),   # orange
    (23, 1, 0xFFFF00),   # yellow
    (48, 3, 0x00FF00),   # green
    (60, 4, 0x00FFFF),   # cyan

    # LEFT / RIGHT SIDES
    (1, 17, 0x0088FF),
    (62, 16, 0x4444FF),

    # MIDDLE
    (6, 16,  0xFF00AA),
    (15, 17, 0xAA00FF),
    (23, 15, 0x00FFFF),
    (31, 18, 0x00FF66),
    (47, 16, 0xFFFF00),
    (56, 17, 0xFF8800),

    # BOTTOM EDGE
    (3, 30, 0xAA00FF),
    (16, 29, 0xFF00AA),
    (46, 31, 0xFF4444),
    (59, 28, 0x00FF88),
]
snowflakes = []

for x, y, color in snowflake_data:
    tile, palette = make_snowflake(x, y, color)
    group.append(tile)

    snowflakes.append({
        "palette": palette,
        "color": color
    })

display.root_group = group

brightness_steps = [
    0.10,
    0.25,
    0.45,
    0.70,
    1.00,
    0.70,
    0.45,
    0.25
]

step = 0

while True:

    for i, snowflake in enumerate(snowflakes):

        brightness = brightness_steps[
            (step + i) % len(brightness_steps)
        ]

        original = snowflake["color"]

        r = (original >> 16) & 0xFF
        g = (original >> 8) & 0xFF
        b = original & 0xFF

        r = int(r * brightness)
        g = int(g * brightness)
        b = int(b * brightness)

        faded_color = (r << 16) | (g << 8) | b

        snowflake["palette"][1] = faded_color

    step = (step + 1) % len(brightness_steps)

    time.sleep(0.12)
