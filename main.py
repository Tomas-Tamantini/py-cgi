"""
py-cgi - A python ray tracing program
Tomas Tamantini 2020
"""
from pre_cooked_scenes.mentos import scene

im = scene.render_image()
im.save_as_png('output/test.png')
print("Image saved.")
