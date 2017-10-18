#!/usr/bin/env python3
# usage: braimg.py /path/to/image [max width in chars]

import sys
from PIL import Image
import math
import colorsys as coloursys

# from: https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
PAL_256 = [0x000000, 0x800000, 0x008000, 0x808000, 0x000080, 0x800080, 0x008080, 0xc0c0c0, 0x808080, 0xff0000, 0x00ff00, 0xffff00, 0x0000ff, 0xff00ff, 0x00ffff, 0xffffff, 0x000000, 0x00005f, 0x000087, 0x0000af, 0x0000d7, 0x0000ff, 0x005f00, 0x005f5f, 0x005f87, 0x005faf, 0x005fd7, 0x005fff, 0x008700, 0x00875f, 0x008787, 0x0087af, 0x0087d7, 0x0087ff, 0x00af00, 0x00af5f, 0x00af87, 0x00afaf, 0x00afd7, 0x00afff, 0x00d700, 0x00d75f, 0x00d787, 0x00d7af, 0x00d7d7, 0x00d7ff, 0x00ff00, 0x00ff5f, 0x00ff87, 0x00ffaf, 0x00ffd7, 0x00ffff, 0x5f0000, 0x5f005f, 0x5f0087, 0x5f00af, 0x5f00d7, 0x5f00ff, 0x5f5f00, 0x5f5f5f, 0x5f5f87, 0x5f5faf, 0x5f5fd7, 0x5f5fff, 0x5f8700, 0x5f875f, 0x5f8787, 0x5f87af, 0x5f87d7, 0x5f87ff, 0x5faf00, 0x5faf5f, 0x5faf87, 0x5fafaf, 0x5fafd7, 0x5fafff, 0x5fd700, 0x5fd75f, 0x5fd787, 0x5fd7af, 0x5fd7d7, 0x5fd7ff, 0x5fff00, 0x5fff5f, 0x5fff87, 0x5fffaf, 0x5fffd7, 0x5fffff, 0x870000, 0x87005f, 0x870087, 0x8700af, 0x8700d7, 0x8700ff, 0x875f00, 0x875f5f, 0x875f87, 0x875faf, 0x875fd7, 0x875fff, 0x878700, 0x87875f, 0x878787, 0x8787af, 0x8787d7, 0x8787ff, 0x87af00, 0x87af5f, 0x87af87, 0x87afaf, 0x87afd7, 0x87afff, 0x87d700, 0x87d75f, 0x87d787, 0x87d7af, 0x87d7d7, 0x87d7ff, 0x87ff00, 0x87ff5f, 0x87ff87, 0x87ffaf, 0x87ffd7, 0x87ffff, 0xaf0000, 0xaf005f, 0xaf0087, 0xaf00af, 0xaf00d7, 0xaf00ff, 0xaf5f00, 0xaf5f5f, 0xaf5f87, 0xaf5faf, 0xaf5fd7, 0xaf5fff, 0xaf8700, 0xaf875f, 0xaf8787, 0xaf87af, 0xaf87d7, 0xaf87ff, 0xafaf00, 0xafaf5f, 0xafaf87, 0xafafaf, 0xafafd7, 0xafafff, 0xafd700, 0xafd75f, 0xafd787, 0xafd7af, 0xafd7d7, 0xafd7ff, 0xafff00, 0xafff5f, 0xafff87, 0xafffaf, 0xafffd7, 0xafffff, 0xd70000, 0xd7005f, 0xd70087, 0xd700af, 0xd700d7, 0xd700ff, 0xd75f00, 0xd75f5f, 0xd75f87, 0xd75faf, 0xd75fd7, 0xd75fff, 0xd78700, 0xd7875f, 0xd78787, 0xd787af, 0xd787d7, 0xd787ff, 0xd7af00, 0xd7af5f, 0xd7af87, 0xd7afaf, 0xd7afd7, 0xd7afff, 0xd7d700, 0xd7d75f, 0xd7d787, 0xd7d7af, 0xd7d7d7, 0xd7d7ff, 0xd7ff00, 0xd7ff5f, 0xd7ff87, 0xd7ffaf, 0xd7ffd7, 0xd7ffff, 0xff0000, 0xff005f, 0xff0087, 0xff00af, 0xff00d7, 0xff00ff, 0xff5f00, 0xff5f5f, 0xff5f87, 0xff5faf, 0xff5fd7, 0xff5fff, 0xff8700, 0xff875f, 0xff8787, 0xff87af, 0xff87d7, 0xff87ff, 0xffaf00, 0xffaf5f, 0xffaf87, 0xffafaf, 0xffafd7, 0xffafff, 0xffd700, 0xffd75f, 0xffd787, 0xffd7af, 0xffd7d7, 0xffd7ff, 0xffff00, 0xffff5f, 0xffff87, 0xffffaf, 0xffffd7, 0xffffff, 0x080808, 0x121212, 0x1c1c1c, 0x262626, 0x303030, 0x3a3a3a, 0x444444, 0x4e4e4e, 0x585858, 0x626262, 0x6c6c6c, 0x767676, 0x808080, 0x8a8a8a, 0x949494, 0x9e9e9e, 0xa8a8a8, 0xb2b2b2, 0xbcbcbc, 0xc6c6c6, 0xd0d0d0, 0xdadada, 0xe4e4e4, 0xeeeeee]
# convert to list of tuples
PAL_256 = [ ((c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF) for c in PAL_256 ]
# build to integer sequence
PAL_256_INT = []
for rgb in PAL_256:
    PAL_256_INT.append(rgb[0])
    PAL_256_INT.append(rgb[1])
    PAL_256_INT.append(rgb[2])

# build dict of indicies
PAL_256_DICT = {rgb: i for i, rgb in enumerate(PAL_256)}

# create an image that uses the above palette
PAL_256_IMAGE = Image.new('P', (16, 16))
PAL_256_IMAGE.putpalette(PAL_256_INT)

# create an image that uses a 1-bit palette
PAL_1_IMAGE = Image.new('P', (16, 16))
PAL_1_IMAGE.putpalette([0, 0, 0, 255, 255, 255] * 128)

BRAILLE_OFFSET = 0x2800
ESCAPE = chr(27)




def normalise_v(rgb, v=1):
    hsv = coloursys.rgb_to_hsv(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
    rgb_new = coloursys.hsv_to_rgb(hsv[0], hsv[1], v)
    return round(rgb_new[0] * 255), round(rgb_new[1] * 255), round(rgb_new[2] * 255)




def image_normalize_v(image, v=1):
    new_data = []
    for colour in image.getdata():
        new_data.append( normalise_v(colour, v) )
    image.putdata(new_data)




def get_pixel_safe(image, x, y, default=(0,0,0,)):
    if x >= image.width or y >= image.height:
        return default

    return image.getpixel((x, y))




def braillify(image):
    lines = []
    for y in range(0, image.height, 4):
        row = ''
        for x in range(0, image.width, 2):
            p1 = get_pixel_safe(image, x, y, 0)
            p2 = get_pixel_safe(image, x, y + 1, 0)
            p3 = get_pixel_safe(image, x, y + 2, 0)
            p4 = get_pixel_safe(image, x + 1, y, 0)
            p5 = get_pixel_safe(image, x + 1, y + 1, 0)
            p6 = get_pixel_safe(image, x + 1, y + 2, 0)
            p7 = get_pixel_safe(image, x, y + 3, 0)
            p8 = get_pixel_safe(image, x + 1, y + 3, 0)

            n = 0
            n |= p1
            n |= p2 << 1
            n |= p3 << 2
            n |= p4 << 3
            n |= p5 << 4
            n |= p6 << 5
            n |= p7 << 6
            n |= p8 << 7

            row += chr(BRAILLE_OFFSET + n)

        lines.append(row)
    return lines




def print_with_colour(image, braille_chars):
    lines = []
    last_index = -1
    for y in range(0, image.height):
        row = ''
        for x in range(0, image.width):
            index = get_pixel_safe(image, x, y)

            if index != last_index:
                row += ESCAPE + '[38;5;{}m'.format(index)
                last_index = index
            row += braille_chars[y][x]
        print(''.join(row))




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
    source_image = Image.open(sys.argv[1]).convert('RGB')
    if source_image.width > max_w:
        source_image.thumbnail((max_w, max_w,), Image.ANTIALIAS)

    # convert to dithered braille
    braille_image = quantizetopalette(source_image, PAL_1_IMAGE)
    braille_chars = braillify(braille_image)
    
    # make per character colour image
    colour_image = source_image.resize(
        (math.ceil(source_image.width/2), math.ceil(source_image.height/4)),
        Image.ANTIALIAS
    )
    image_normalize_v(colour_image)
    colour_image = quantizetopalette(colour_image, PAL_256_IMAGE)

    # combine braille and colour while printing
    print_with_colour(colour_image, braille_chars)

    # reset
    print(ESCAPE + '[0m')


if __name__ == '__main__':
    main()
