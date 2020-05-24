"""
py-cgi - A python ray tracing program
Tomas Tamantini 2020
"""

from basics import Vector, Point
from class_lib.light import Ray
from class_lib.color import Color
from class_lib.imaging import Image

c = Color(1.0, 1.1, 0.5)
c1 = Color(0.0, 0.5, 0.5)

i = Image(20, 30)
i.set_pixel(c1, 0, 1)
i.set_pixel(c, 1, 2)
i.set_pixel(0.5*c+0.5*c1, 1, 0)
i.set_pixel( Color(1,0,0),0,0)
i.set_pixel( Color(0,1,0),0,2)
# x = i.get_pixel(0, 1)
# x = Color(1, 1, 1)
# print(x)
i.save_as_ppm('output/test.ppm')

