from basics import Vector, Point
from class_lib.light import Ray, Color

c = Color(1.0, 1.1, 0.5)
c1 = Color(0.0, -0.2, 0.3)

s = 0.8 * c * 0.3
print(s)
print(0.264*255)
print(s.write_as_ppm())
