import bpy

bpy.ops.preferences.addon_install(filepath="src/ke_i2m.py")
bpy.ops.preferences.addon_enable(module="ke_i2m")

bpy.ops.ke.i2m_filebrowser(filepath="tests/NASA_logo.svg.png")
bpy.ops.ke.i2m(front_only=False, pixel_width=0, width=1)
