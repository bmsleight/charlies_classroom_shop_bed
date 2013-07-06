#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#   signstl - generate an stl file based upon input usign OpenScad. 
#   Copyright (C) Brendan M. Sleight, et al. <bms.stl#barwap.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from solid import *
from solid.utils import *
import os, sys, re, argparse


# http://en.wikipedia.org/wiki/Bed_size : matress 91 cm × 190 cm
# http://www.ikea.com/gb/en/catalog/categories/departments/bedroom/Mattresses/
# http://www.ikea.com/gb/en/catalog/products/70163300/ 
# Length: 190 cm
# Width: 90 cm
# Thickness: 17 cm

matress_length = 1900
matress_width = 900
matress_thickness = 170

#from chiney
room_length_bed_section = 2222

#140 ch
chim_length = 480
chim_depth = 300
alcove_length = 1400 - chim_length
wall_height = 2400

timber_width=37
timber_thickness=60
mdf_thickness=12


top_platform_height = 1500
bottom_platform_height = 500
front_top_platform_height = 1700

top_platform_width=matress_width + matress_thickness + (2*timber_thickness)

#slide http://www.activegarden.co.uk/wmsimages/40779Slides.jpg

slide_width = alcove_length
#slide_width = 650


#slide_platform_width = 900 #top_platform_width - 
slide_platform_width = alcove_length

room_length = room_length_bed_section + chim_length + alcove_length
room_width = 3500
room_door = 840 



# Using the corner where the chimeny start to jut out at 0,0


#To Have Marks 
MARK = False

class Parts(object):
    def __init__(self):
        self.total_parts = 0
        self.name = "Default Name"
    def mark_part(self, comments=""):
        # A nice fancy function would be better....
        marks = union()
        self.total_parts += 1
        print self.name + ", " + comments + ", Marked :", bin(self.total_parts)
        for power in range(0,7):
            m = up(power*2)(left(0.5)(back(0.5)(cube([1,1,1]) ) ))
            m = m + forward(power*2)(up(-0.5)(left(0.5)(cube([1,1,1]) ) ))
            m = m + right(power*2)(forward(-0.5)(up(-0.5)(cube([1,1,1]) ) ))
            if self.total_parts & int((math.pow(2,power))):
                m = color(Black)(m)
            else:
                m = color(White)(m)
            marks = marks + m
        return marks

def wood(timber_width, timber_thickness, timber_length, direction=1):
    # directions 1, 2, 3 
    #  is 1 along, (y-axis) 
    #  is 2 up, (z-axis)
    #  is 3 out, (x-axis)
 
    if direction == 1:
        timber = color(Pine)(cube([timber_width, timber_length, timber_thickness]))
    elif direction == 2:
        timber = color(Pine)(cube([timber_width, timber_thickness, timber_length]))
    elif direction == 3:
        timber = color(Pine)(cube([timber_length, timber_width, timber_thickness]))

    elif direction == 4: # as 1
        timber = color(Pine)(cube([timber_thickness, timber_length, timber_width]))
    elif direction == 5:
        timber = color(Pine)(cube([timber_thickness, timber_width, timber_length]))
    elif direction == 6:
        timber = color(Pine)(cube([timber_length, timber_thickness, timber_width]))

    if MARK:
        comments = "Length: " + str(timber_length) + ", width: " + str(timber_width) + ", thickness:" + str(timber_thickness)
        timber = timber + parts.mark_part(comments)
    return timber

def timber(timber_length, direction=1):
#    timber_width=37
#    timber_thickness=60
    return wood(timber_width, timber_thickness, timber_length, direction)

def mdf_sheet(timber_length, timber_width, direction=1, timber_thickness=mdf_thickness):
    return wood(timber_width, timber_thickness, timber_length, direction)

def timber_angle_cut(timber_length, angle, direction=1):
    t = wood(timber_width, timber_thickness, timber_length, direction)
#    c = cube([timber_thickness, timber_thickness, timber_thickness])
    c = cube([99, 99, 99])

    if direction == 1:
        c = rotate([0, 0, angle])(c)
        c = translate([0,timber_length, 0])(c)
    elif direction == 2:
        c = rotate([0, angle, 0])(c)
        c = translate([0,0,timber_length])(c)
    elif direction == 3:
        c = rotate([0, 0, angle])(c)
        c = translate([timber_length, 0, 0])(c)
    elif direction == 4: # as 1
        c = rotate([angle, 0, 0])(c)
        c = translate([0, timber_length, 0])(c)
    elif direction == 5:
        c = rotate([angle, 0, 0])(c)
        c = translate([0,0,timber_length])(c)
    elif direction == 6:
        c = rotate([0, angle, 0])(c)
        c = translate([timber_length, 0, 0])(c)
    return t - c
 
def timber_square(length=1000, width=1000, direction=1, join="thick"):
    #   
    #   144442
    #   1    2
    #   1    2
    #   1    2
    #   133332
    #  

    if direction == 1 and join=="thick":
        d1 = 1
        d2 = 3
    if direction == 2 and join=="thick":
        d1 = 2
        d2 = 6
    if direction == 3 and join=="thick":
        d1 = 2
        d2 = 1
    if direction == 4 and join=="thick":
        d1 = 5
        d2 = 3

    if direction == 1 or direction == 2:
        long_strut = timber(length, d1)
        long_strut2 = timber(length,d1)
        short_strut = timber(width-(2*timber_width), d2)
        short_strut2 = timber(width-(2*timber_width), d2)
    if direction == 3 or direction == 4:
        long_strut = timber(length, d1)
        long_strut2 = timber(length, d1)
        short_strut = timber(width-(2*timber_thickness), d2)
        short_strut2 = timber(width-(2*timber_thickness), d2)

    if direction == 1 or direction == 2:
        strut1 = long_strut
        strut2 = right(width-timber_width)(long_strut2)
        strut3 = right(timber_width)(short_strut)
    if direction == 3:
        strut1 = long_strut
        strut2 = forward(width-timber_thickness)(long_strut2)
        strut3 = forward(timber_thickness)(short_strut)
    if direction == 4:
        strut1 = long_strut
        strut2 = right(width-timber_thickness)(long_strut2)
        strut3 = right(timber_thickness)(short_strut)
    if direction == 1:
        strut4 = forward(length-timber_width)(right(timber_width)(short_strut2))
    if direction == 2:
        strut4 = up(length-timber_width)(right(timber_width)(short_strut2))
    if direction == 3:
        strut4 = up(length-timber_thickness)(forward(timber_thickness)(short_strut2))
    if direction == 4:
        strut4 = up(length-timber_thickness)(right(timber_thickness)(short_strut2))

    return strut1 + strut2 + strut3 + strut4



def walls():
    # floor (not technically a wall)
    walls = down(100)(cube([room_width, room_length,100]))
    # Door
    walls = walls + right(room_width-room_door/1.4)(forward(room_door*0.4-100)(rotate([0,0,45])(cube([room_door, 100,wall_height]))))
    walls = walls + right(room_width-room_door)(forward(room_door)(rotate([0,0,0])(cube([room_door, 100,wall_height]))))

    # Back wall
    walls = walls + left(100)(cube([100, room_length, wall_height]))
    # chim
    walls = walls + forward(alcove_length)(cube([chim_depth,100,wall_height]))
    walls = walls + forward(alcove_length+100)(right(chim_depth-100)(cube([100,chim_length-200,wall_height])))
    walls = walls + forward(alcove_length+chim_length-100)(cube([chim_depth,100,wall_height]))

    # End wall by window
    walls = walls + forward(room_length)(cube([1050,100,wall_height]))

    walls = color(Transparent)(walls)
    return walls

def matress_top():
    matress = cube([matress_width, matress_length, matress_thickness])
    matress = up(top_platform_height)(forward(room_length-matress_length)(matress))
    return color(Magenta)(matress)


def matress_bottom():
    matress = cube([matress_width, matress_length, matress_thickness])
    matress = up(bottom_platform_height)(forward(room_length-matress_length)(matress))
    return color(Magenta)(matress)


def front_sheet():
    parts.name="Front Sheet"
    bed_forward = alcove_length+chim_length
    bed_right = top_platform_width
    tw = room_length_bed_section
    th = front_top_platform_height
    da = tw/5.0
#    dh = th/2.5
    wph = th/2.0
    ph = th /5.0
    px = tw /16.0
#    wh = ph
    wx = (tw - da - da - (px*4.0)/2)
 

    print "Door is :", da, wph+ph
    print "Window is :", ph, wx


    b1 = mdf_sheet(tw/2.0 - da, wph, direction=4)   
    b5 = mdf_sheet(tw/2.0 - da, wph, direction=4)   
    b2 = mdf_sheet(px, ph, direction=4)
    b3 = mdf_sheet(px, ph, direction=4)
    b6 = mdf_sheet(px, ph, direction=4)
    b7 = mdf_sheet(px, ph, direction=4)
    b4 = mdf_sheet(tw, th-wph-ph, direction=4)

    b1 = forward(da)(b1)
    b2 = up(wph)(forward(da)(b2))
    b3 = up(wph)(forward(tw/2.0-px)(b3))
    b4 = up(wph+ph)(forward(0)(b4))
    b5 = forward(tw-(tw/2.0-da))(b5)
    b6 = up(wph)(forward(tw-(tw/2.0)+da)(b6))
    b7 = up(wph)(forward(tw-px)(b7))


    b1 = forward(bed_forward)(right(bed_right)(b1))
    b2 = forward(bed_forward)(right(bed_right)(b2))
    b3 = forward(bed_forward)(right(bed_right)(b3))
    b4 = forward(bed_forward)(right(bed_right)(b4))
    b5 = forward(bed_forward)(right(bed_right)(b5))
    b6 = forward(bed_forward)(right(bed_right)(b6))
    b7 = forward(bed_forward)(right(bed_right)(b7))



#    fs = (mdf_sheet(room_length_bed_section, front_top_platform_height, direction=4) )
#    fs = forward(alcove_length+chim_length)(fs)
#    fs = right(top_platform_width)(fs)
    fs = b1 + b2 + b3 + b4 + b5 +b6 + b7
    return fs

def top_platform():
    parts.name="Top Platform"
    tp = mdf_sheet(room_length_bed_section, top_platform_width, direction=1) 
    tp = forward(alcove_length+chim_length)(tp)
    tp = up(top_platform_height)(tp)
    return tp

def bottom_platform():
    parts.name="Bottom Platform"
    tp = mdf_sheet(room_length_bed_section, top_platform_width, direction=1) 
    tp = forward(alcove_length+chim_length)(tp)
    tp = up(bottom_platform_height)(tp)
    return tp

def stairs():
    parts.name="Stairs"
    s = mdf_sheet(chim_length, 300, direction=1) 
    s = forward(alcove_length)(s)
    s = up(1200)(s)
    s = right(chim_depth)(s)
    stwo = mdf_sheet(chim_length, 600, direction=1) 
    stwo = forward(alcove_length)(stwo)
    stwo = up(800)(stwo)
    stwo = right(chim_depth)(stwo)
    sthree = mdf_sheet(chim_length, 900, direction=1) 
    sthree = forward(alcove_length)(sthree)
    sthree = up(400)(sthree)
    sthree = right(chim_depth)(sthree)
    panel = mdf_sheet(top_platform_height+mdf_thickness, 900, direction=2) 
    panel = right(chim_depth)(panel)
    side_panel = forward(alcove_length+chim_length)(panel) + forward(alcove_length)(panel)
    return s + stwo + sthree + side_panel


def slide():
    parts.name="Slidieeeee"
    platform = mdf_sheet(alcove_length, slide_platform_width, direction=1)
    platform = up(top_platform_height)(platform)
    s = mdf_sheet(slide_width, top_platform_height*1.4, direction=1)
    s = s + up(mdf_thickness)(timber(top_platform_height*1.4,  3))
    s = s + forward(slide_platform_width-timber_width)(up(mdf_thickness)(timber(top_platform_height*1.4,  3)))
    s = rotate([0,45,0])(s)
    s = right(slide_platform_width-timber_thickness)(s)
    s = up(top_platform_height+(mdf_thickness+timber_width)*1.4)(s)
    return platform + s



def frame_slide():
    f = union()
    parts.name="Frame Slide"
    # Wall peice
    parts.name="Frame Slide - wall connector"
    f = f + up(top_platform_height/2.0)( timber(slide_platform_width,  3) )
    f = f + up(top_platform_height/2.0)(forward(timber_width)(timber(alcove_length - timber_width,  1) ))
    parts.name="Frame Slide - squares"
    f = f + right(timber_width)(forward(timber_width)(timber_square(alcove_length-timber_width-timber_width, slide_platform_width-timber_width, 1) ))
    f = f + up(top_platform_height-timber_thickness)(right(timber_width)(forward(timber_width)(timber_square(alcove_length-timber_width-timber_width, slide_platform_width-timber_width, 1) )))

    f = f + up(timber_thickness)(right(timber_width+chim_depth)(forward(timber_width)(timber_square(top_platform_height-timber_thickness*2, slide_platform_width-timber_width-chim_depth, 4) )))
    f = f + right(timber_width+chim_depth)(forward(-timber_width+alcove_length)(timber_square(top_platform_height, slide_platform_width-timber_width-chim_depth, 4) ))
    f = f + up(timber_thickness)(right(timber_width)(forward(timber_width)(timber_square(top_platform_height-timber_thickness-timber_thickness, alcove_length-timber_width-timber_width, 3) )))


#    f = f + up(3000)(timber_angle_cut(1000, 45, 2))

    return f


def frames():
    return frame_slide()


if __name__ == '__main__':    

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store', dest='fn',
                    default="60", help='openscad $fn=')
    parser.add_argument('-s', action='store', dest='openscad',
                    help='Openscad file name')
    parser.add_argument('-w', action='store_true', default=False,
                    dest='walls',
                    help='Include the walls')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    options = parser.parse_args()


    parts = Parts()
    a = union()

#    a = a + matress() + timber()

#    a = a + timber(1000, parts, 1)
#    a = a + timber(1000, parts, 2)
#    a = a + up(100)(timber(2000, 4))

#    a = a + up(100)(timber(2000, 5))

#    a = a + timber_square(1200, 800, 1)
#    a = a + up(timber_thickness)(timber_square(1200, 800, 4))
#    a = a + up(timber_thickness)(right(timber_width)(timber_square(1200, 800-timber_width, 4)))
#    a = a + up(timber_thickness)(timber_square(1200, 800, 3))

#    a = a + up(100)(mdf_sheet(600, 1200, 1) )
#    a = a + up(100)(mdf_sheet(600, 1200, 2) )
#    a = a + up(100)(mdf_sheet(600, 1200, 3) )
#    a = a + up(100)(mdf_sheet(600, 1200, 4) )
#    a = a + up(100)(mdf_sheet(600, 1200, 5) )
#    a = a + up(100)(mdf_sheet(600, 1200, 6) )
#    a = a + forward(100)(timber(1000, 3))


    a = a + frame_slide()
    a = a + matress_top() + matress_bottom() + front_sheet() + top_platform() + bottom_platform()
    a = a + stairs() + slide()


    if options.walls:
        a = a + walls()

    fn = '$fn=' + options.fn + ';'
    scad_render_to_file( a, options.openscad, include_orig_code=True, file_header=fn)



