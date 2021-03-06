#!/usr/bin/env python3
# usage: braimg.py /path/to/image [max width in chars]

import sys
from PIL import Image
import math
import colorsys as coloursys
import time


# from: https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
PAL_256 = [
    0x000000, 0x800000, 0x008000, 0x808000, 0x000080, 0x800080, 0x008080, 0xc0c0c0,
    0x808080, 0xff0000, 0x00ff00, 0xffff00, 0x0000ff, 0xff00ff, 0x00ffff, 0xffffff,
    0x000000, 0x00005f, 0x000087, 0x0000af, 0x0000d7, 0x0000ff, 0x005f00, 0x005f5f, 0x005f87, 0x005faf, 0x005fd7, 0x005fff, 0x008700, 0x00875f, 0x008787, 0x0087af, 0x0087d7, 0x0087ff, 0x00af00, 0x00af5f, 0x00af87, 0x00afaf, 0x00afd7, 0x00afff, 0x00d700, 0x00d75f, 0x00d787, 0x00d7af, 0x00d7d7, 0x00d7ff, 0x00ff00, 0x00ff5f, 0x00ff87, 0x00ffaf, 0x00ffd7, 0x00ffff,
    0x5f0000, 0x5f005f, 0x5f0087, 0x5f00af, 0x5f00d7, 0x5f00ff, 0x5f5f00, 0x5f5f5f, 0x5f5f87, 0x5f5faf, 0x5f5fd7, 0x5f5fff, 0x5f8700, 0x5f875f, 0x5f8787, 0x5f87af, 0x5f87d7, 0x5f87ff, 0x5faf00, 0x5faf5f, 0x5faf87, 0x5fafaf, 0x5fafd7, 0x5fafff, 0x5fd700, 0x5fd75f, 0x5fd787, 0x5fd7af, 0x5fd7d7, 0x5fd7ff, 0x5fff00, 0x5fff5f, 0x5fff87, 0x5fffaf, 0x5fffd7, 0x5fffff,
    0x870000, 0x87005f, 0x870087, 0x8700af, 0x8700d7, 0x8700ff, 0x875f00, 0x875f5f, 0x875f87, 0x875faf, 0x875fd7, 0x875fff, 0x878700, 0x87875f, 0x878787, 0x8787af, 0x8787d7, 0x8787ff, 0x87af00, 0x87af5f, 0x87af87, 0x87afaf, 0x87afd7, 0x87afff, 0x87d700, 0x87d75f, 0x87d787, 0x87d7af, 0x87d7d7, 0x87d7ff, 0x87ff00, 0x87ff5f, 0x87ff87, 0x87ffaf, 0x87ffd7, 0x87ffff,
    0xaf0000, 0xaf005f, 0xaf0087, 0xaf00af, 0xaf00d7, 0xaf00ff, 0xaf5f00, 0xaf5f5f, 0xaf5f87, 0xaf5faf, 0xaf5fd7, 0xaf5fff, 0xaf8700, 0xaf875f, 0xaf8787, 0xaf87af, 0xaf87d7, 0xaf87ff, 0xafaf00, 0xafaf5f, 0xafaf87, 0xafafaf, 0xafafd7, 0xafafff, 0xafd700, 0xafd75f, 0xafd787, 0xafd7af, 0xafd7d7, 0xafd7ff, 0xafff00, 0xafff5f, 0xafff87, 0xafffaf, 0xafffd7, 0xafffff,
    0xd70000, 0xd7005f, 0xd70087, 0xd700af, 0xd700d7, 0xd700ff, 0xd75f00, 0xd75f5f, 0xd75f87, 0xd75faf, 0xd75fd7, 0xd75fff, 0xd78700, 0xd7875f, 0xd78787, 0xd787af, 0xd787d7, 0xd787ff, 0xd7af00, 0xd7af5f, 0xd7af87, 0xd7afaf, 0xd7afd7, 0xd7afff, 0xd7d700, 0xd7d75f, 0xd7d787, 0xd7d7af, 0xd7d7d7, 0xd7d7ff, 0xd7ff00, 0xd7ff5f, 0xd7ff87, 0xd7ffaf, 0xd7ffd7, 0xd7ffff,
    0xff0000, 0xff005f, 0xff0087, 0xff00af, 0xff00d7, 0xff00ff, 0xff5f00, 0xff5f5f, 0xff5f87, 0xff5faf, 0xff5fd7, 0xff5fff, 0xff8700, 0xff875f, 0xff8787, 0xff87af, 0xff87d7, 0xff87ff, 0xffaf00, 0xffaf5f, 0xffaf87, 0xffafaf, 0xffafd7, 0xffafff, 0xffd700, 0xffd75f, 0xffd787, 0xffd7af, 0xffd7d7, 0xffd7ff, 0xffff00, 0xffff5f, 0xffff87, 0xffffaf, 0xffffd7, 0xffffff,
    0x080808, 0x121212, 0x1c1c1c, 0x262626, 0x303030, 0x3a3a3a, 0x444444, 0x4e4e4e, 0x585858, 0x626262, 0x6c6c6c, 0x767676, 0x808080, 0x8a8a8a, 0x949494, 0x9e9e9e, 0xa8a8a8, 0xb2b2b2, 0xbcbcbc, 0xc6c6c6, 0xd0d0d0, 0xdadada, 0xe4e4e4, 0xeeeeee
]
# convert to list of tuples
PAL_256 = [ ((c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF) for c in PAL_256 ]

# build integer sequence
PAL_256_INT = []
for rgb in PAL_256:
    PAL_256_INT.append(rgb[0])
    PAL_256_INT.append(rgb[1])
    PAL_256_INT.append(rgb[2])

# create an image that uses the above palette
PAL_256_IMAGE = Image.new('P', (16, 16))
PAL_256_IMAGE.putpalette(PAL_256_INT)

# create an image that uses a 1-bit palette
PAL_1_IMAGE = Image.new('P', (16, 16))
PAL_1_IMAGE.putpalette([0, 0, 0, 255, 255, 255] * 128)

# constants
ESCAPE = chr(27)
BRAILLE_CHARS = []
for i in range(256):
    BRAILLE_CHARS.append( chr(0x2800 + i) )

PI_2_3 = math.pi * (2 / 3)



def braillify(image):
    chars = ''
    image_data = image.getdata()

    y_offsets = []
    for i in range(image.height):
        y_offsets.append(i * image.width)

    for y in range(0, image.height, 4):
        for x in range(0, image.width, 2):
            p1 = image_data[x + 0 + y_offsets[y + 0]]
            p2 = image_data[x + 0 + y_offsets[y + 1]]
            p3 = image_data[x + 0 + y_offsets[y + 2]]
            p4 = image_data[x + 1 + y_offsets[y + 0]]
            p5 = image_data[x + 1 + y_offsets[y + 1]]
            p6 = image_data[x + 1 + y_offsets[y + 2]]
            p7 = image_data[x + 0 + y_offsets[y + 3]]
            p8 = image_data[x + 1 + y_offsets[y + 3]]

            offset = p1 | p2 << 1 | p3 << 2 | p4 << 3 | p5 << 4 | p6 << 5 | p7 << 6 | p8 << 7
            chars += BRAILLE_CHARS[offset]

    return chars




def print_with_colour(image, braille_chars):
    last_colour = -1
    output = ''
    for i, colour in enumerate(image.getdata()):
        if colour != last_colour:
            output += ESCAPE + '[38;5;{}m'.format(colour)
            last_colour = colour
        output += braille_chars[i]
        if (i+1) % image.width == 0:
            output += '\n'
    print(output)




# adapted from https://stackoverflow.com/a/34407200
def remove_luma(r, g, b):
    if r + g + b == 0:
        return 255, 255, 255

    scale = 255 / max(r, g, b)
    return round(r * scale), round(g * scale), round(b * scale)



def image_remove_luma(image):
    new_data = []
    for colour in image.getdata():
        new_data.append( remove_luma(colour[0], colour[1], colour[2]) )
    image.putdata(new_data)



def quantizetopalette(silf, palette, dither=True):
    """
    Convert an RGB or L mode image to use a given P image's palette.
    from: https://stackoverflow.com/a/29438149
    """

    silf.load()
    # use palette from reference image
    palette.load()
    if palette.mode != "P":
        raise ValueError("bad mode for palette image")
    if silf.mode != "RGB" and silf.mode != "L":
        raise ValueError(
            "only RGB or L mode images can be quantized to a palette"
            )
    im = silf.im.convert("P", 1 if dither else 0, palette.im)
    # the 0 above means turn OFF dithering

    # Later versions of Pillow (4.x) rename _makeself to _new
    try:
        return silf._new(im)
    except AttributeError:
        return silf._makeself(im)



def main():
    if len(sys.argv) < 2:
        print("usage: braimg.py /path/to/image [max width in chars]")
        exit()

    max_cols = 160
    if len(sys.argv) >= 3:
        max_cols = int(sys.argv[2])
    max_w = max_cols*2

    # load image
    raw_image = Image.open(sys.argv[1]).convert('RGB')
    if raw_image.width > max_w:
        raw_image.thumbnail((max_w, max_w,), Image.ANTIALIAS)

    source_size = (math.ceil(raw_image.width / 2) * 2, math.ceil(raw_image.height / 4) * 4)
    source_image = Image.new('RGB', source_size)
    source_image.paste(raw_image)


    # convert to dithered braille
    braille_image = quantizetopalette(source_image, PAL_1_IMAGE)
    braille_chars = braillify(braille_image)
    
    # make per character colour image
    colour_image = source_image.resize(
        (source_image.width//2, source_image.height//4),
        Image.ANTIALIAS
    )
    image_remove_luma(colour_image)
    colour_image = quantizetopalette(colour_image, PAL_256_IMAGE)

    # set black background
    print(ESCAPE + '[48;5;0m')

    # combine braille and colour while printing
    print_with_colour(colour_image, braille_chars)

    # reset
    print(ESCAPE + '[0m')


if __name__ == '__main__':
    main()
