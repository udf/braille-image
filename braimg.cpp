#undef cimg_display
#define cimg_display 0
#include "CImg/CImg.h"
#include <iostream>
#include <sstream>
#include <stdio.h>
#include <algorithm>
#include <chrono>
#include <thread>

#define MAX_CHARS 160
#define PI_2_3 M_PI * (2.0f / 3.0f)

using namespace cimg_library;
using namespace std;

using Clock = std::chrono::steady_clock;
using std::chrono::time_point;
using std::chrono::duration_cast;
using std::chrono::milliseconds;

unsigned ceil_multiple(const unsigned n, const unsigned m) {
    return ((n + m - 1) / m) * m;
}


const CImg<unsigned char> get_palette() {
    static const unsigned int PAL_SIZE = 256;
    CImg<unsigned char> palette(PAL_SIZE, 1, 1, 3);

    // from: https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
    static const unsigned int PAL_256[] = {
        0x000000, 0x800000, 0x008000, 0x808000, 0x000080, 0x800080, 0x008080, 0xc0c0c0,
        0x808080, 0xff0000, 0x00ff00, 0xffff00, 0x0000ff, 0xff00ff, 0x00ffff, 0xffffff,
        0x000000, 0x00005f, 0x000087, 0x0000af, 0x0000d7, 0x0000ff, 0x005f00, 0x005f5f, 0x005f87, 0x005faf, 0x005fd7, 0x005fff, 0x008700, 0x00875f, 0x008787, 0x0087af, 0x0087d7, 0x0087ff, 0x00af00, 0x00af5f, 0x00af87, 0x00afaf, 0x00afd7, 0x00afff, 0x00d700, 0x00d75f, 0x00d787, 0x00d7af, 0x00d7d7, 0x00d7ff, 0x00ff00, 0x00ff5f, 0x00ff87, 0x00ffaf, 0x00ffd7, 0x00ffff,
        0x5f0000, 0x5f005f, 0x5f0087, 0x5f00af, 0x5f00d7, 0x5f00ff, 0x5f5f00, 0x5f5f5f, 0x5f5f87, 0x5f5faf, 0x5f5fd7, 0x5f5fff, 0x5f8700, 0x5f875f, 0x5f8787, 0x5f87af, 0x5f87d7, 0x5f87ff, 0x5faf00, 0x5faf5f, 0x5faf87, 0x5fafaf, 0x5fafd7, 0x5fafff, 0x5fd700, 0x5fd75f, 0x5fd787, 0x5fd7af, 0x5fd7d7, 0x5fd7ff, 0x5fff00, 0x5fff5f, 0x5fff87, 0x5fffaf, 0x5fffd7, 0x5fffff,
        0x870000, 0x87005f, 0x870087, 0x8700af, 0x8700d7, 0x8700ff, 0x875f00, 0x875f5f, 0x875f87, 0x875faf, 0x875fd7, 0x875fff, 0x878700, 0x87875f, 0x878787, 0x8787af, 0x8787d7, 0x8787ff, 0x87af00, 0x87af5f, 0x87af87, 0x87afaf, 0x87afd7, 0x87afff, 0x87d700, 0x87d75f, 0x87d787, 0x87d7af, 0x87d7d7, 0x87d7ff, 0x87ff00, 0x87ff5f, 0x87ff87, 0x87ffaf, 0x87ffd7, 0x87ffff,
        0xaf0000, 0xaf005f, 0xaf0087, 0xaf00af, 0xaf00d7, 0xaf00ff, 0xaf5f00, 0xaf5f5f, 0xaf5f87, 0xaf5faf, 0xaf5fd7, 0xaf5fff, 0xaf8700, 0xaf875f, 0xaf8787, 0xaf87af, 0xaf87d7, 0xaf87ff, 0xafaf00, 0xafaf5f, 0xafaf87, 0xafafaf, 0xafafd7, 0xafafff, 0xafd700, 0xafd75f, 0xafd787, 0xafd7af, 0xafd7d7, 0xafd7ff, 0xafff00, 0xafff5f, 0xafff87, 0xafffaf, 0xafffd7, 0xafffff,
        0xd70000, 0xd7005f, 0xd70087, 0xd700af, 0xd700d7, 0xd700ff, 0xd75f00, 0xd75f5f, 0xd75f87, 0xd75faf, 0xd75fd7, 0xd75fff, 0xd78700, 0xd7875f, 0xd78787, 0xd787af, 0xd787d7, 0xd787ff, 0xd7af00, 0xd7af5f, 0xd7af87, 0xd7afaf, 0xd7afd7, 0xd7afff, 0xd7d700, 0xd7d75f, 0xd7d787, 0xd7d7af, 0xd7d7d7, 0xd7d7ff, 0xd7ff00, 0xd7ff5f, 0xd7ff87, 0xd7ffaf, 0xd7ffd7, 0xd7ffff,
        0xff0000, 0xff005f, 0xff0087, 0xff00af, 0xff00d7, 0xff00ff, 0xff5f00, 0xff5f5f, 0xff5f87, 0xff5faf, 0xff5fd7, 0xff5fff, 0xff8700, 0xff875f, 0xff8787, 0xff87af, 0xff87d7, 0xff87ff, 0xffaf00, 0xffaf5f, 0xffaf87, 0xffafaf, 0xffafd7, 0xffafff, 0xffd700, 0xffd75f, 0xffd787, 0xffd7af, 0xffd7d7, 0xffd7ff, 0xffff00, 0xffff5f, 0xffff87, 0xffffaf, 0xffffd7, 0xffffff,
        0x080808, 0x121212, 0x1c1c1c, 0x262626, 0x303030, 0x3a3a3a, 0x444444, 0x4e4e4e, 0x585858, 0x626262, 0x6c6c6c, 0x767676, 0x808080, 0x8a8a8a, 0x949494, 0x9e9e9e, 0xa8a8a8, 0xb2b2b2, 0xbcbcbc, 0xc6c6c6, 0xd0d0d0, 0xdadada, 0xe4e4e4, 0xeeeeee
    };

    for (int i = 0; i < PAL_SIZE; i++) {
        palette(i, 0, 0, 0) = (PAL_256[i] >> 16) & 0xFF;
        palette(i, 0, 0, 1) = (PAL_256[i] >> 8) & 0xFF;
        palette(i, 0, 0, 2) = PAL_256[i] & 0xFF;
    }

    return palette;
}


bool parse_int(const char* str, int &number) {
    const int old_number = number;
    istringstream ss(str);
    if (!(ss >> number)) {
        number = old_number;
        return false;
    }
    return true;
}


void remove_luma(unsigned char &r, unsigned char &g, unsigned char &b) {
    if (r + g + b == 0) {
        r = g = b = 255;
        return;
    }
    const float scale = 255.0f / (max(max(r, g), b));

    r = r * scale;
    g = g * scale;
    b = b * scale;
}


int main(int argc, char **argv) {
    time_point<Clock> start;
    std::setlocale(LC_ALL, "en_US.utf8");
    cimg::exception_mode(0);


   // parse command line args
    if (argc < 2) {
        std::cerr << "usage: braimg /path/to/image [max width in chars]" << std::endl;
        return 1;
    }
    int max_chars = MAX_CHARS;
    if (argc >= 3) {
        if (!parse_int(argv[2], max_chars) || max_chars <= 0) {
            max_chars = MAX_CHARS;
            std::cerr << "Invalid width specified, defaulting to " << max_chars << std::endl;    
        }
    }
    const int max_width = max_chars * 2;


    // load image
    CImg<unsigned char> source;
    try {
        source.assign(argv[1]);
    } catch (CImgIOException& e) {
        std::cerr << "Failed to load image: " << e.what() << std::endl;
        return 1;
    }
    if (source.width() > max_width)
        source.resize(
            max_width,
            (max_width * source.height()) / source.width(),
            -100,
            -100,
            5
        );
    source.resize(ceil_multiple(source.width(), 2), ceil_multiple(source.height(), 4));


    // convert to b/w for braille (luma)
    const CImg<unsigned char> luma = source.get_index(
        CImg<unsigned char>(2,1,1,3, 0,0,0, 255,255,255),
        1,
        false
    );


    // resize source to 1px per character and remove the luma component
    source.resize(source.width() / 2, source.height() / 4, -100, -100, 5);
    cimg_forY(source, y) {
        cimg_forX(source, x) {
            unsigned char r, g, b;

            r = source(x, y, 0, 0);
            g = source(x, y, 0, 1);
            b = source(x, y, 0, 2);

            remove_luma(r, g, b);

            source(x, y, 0, 0) = r;
            source(x, y, 0, 1) = g;
            source(x, y, 0, 2) = b;
        }
    }


    // convert to paletted
    const CImg<unsigned char> palette = get_palette();
    source.index(palette, 1, false);


    // print
    int last_colour = -1;
    // set background to black
    wcout << "\33[48;5;0m" << endl;
    for (int y = 0; y < luma.height(); y += 4) {
        for (int x = 0; x < luma.width(); x += 2) {
            unsigned char colour = source(x/2, y/4);
            if (colour != last_colour) {
                wcout << "\33[38;5;" << (unsigned)colour << "m";
                last_colour = colour;
            }

            const unsigned char offset =
                  luma(x + 0, y + 0)
                | luma(x + 0, y + 1) << 1
                | luma(x + 0, y + 2) << 2
                | luma(x + 1, y + 0) << 3
                | luma(x + 1, y + 1) << 4
                | luma(x + 1, y + 2) << 5
                | luma(x + 0, y + 3) << 6
                | luma(x + 1, y + 3) << 7;
            wcout << (wchar_t)(0x2800 + offset); 
        }
        wcout << endl;
    }
    // reset
    wcout << "\33[0m" << endl;

    return 0;
}