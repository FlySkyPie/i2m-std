import bpy
from bpy.types import Operator

class KeI2Mreload(Operator):
    bl_idname = "ke.i2m_reload"
    bl_label = "I2M Reload"
    bl_description = "Reload I2M image(s)"

    def execute(self, context):
        k = context.scene.kei2m
        front_img = bpy.data.images.get(k.FRONT)
        right_img = bpy.data.images.get(k.RIGHT)
        top_img = bpy.data.images.get(k.TOP)
        back_img = bpy.data.images.get(k.BACK)
        left_img = bpy.data.images.get(k.LEFT)
        bottom_img = bpy.data.images.get(k.BOTTOM)
        images = [front_img, right_img, top_img, back_img, left_img, bottom_img]
        kindex = ["FRONT", "RIGHT", "TOP", "BACK", "LEFT", "BOTTOM"]
        missing = 0
        found = 0
        for index, i in enumerate(images):
            if i is None:
                k[kindex[index]] = ""
                missing += 1
            if i is not None:
                i.reload()
        context.area.tag_redraw()
        if missing:
            self.report(
                {"INFO"},
                "%s slot(s) reloaded - %s slot(s) empty/invalid"
                % (str(found), str(missing)),
            )
        return {"FINISHED"}
