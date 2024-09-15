from bpy.types import Panel

from ..utilities import kei2m_version


# ------------------------------------------------------------------------------------------------------------
# UI
# ------------------------------------------------------------------------------------------------------------
class VIEW3D_PT_i2m(Panel):
    bl_label = "keI2M v%s" % str(kei2m_version)
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "kei2m"

    def draw_header_preset(self, context):
        layout = self.layout
        layout.emboss = "NONE"
        row = layout.row(align=False)
        row.prop(
            context.scene.kei2m,
            "info",
            text="",
            icon="QUESTION",
            icon_only=True,
            emboss=False,
        )
        row.separator(factor=0.5)

    def draw(self, context):
        k = context.scene.kei2m
        has_front = bool(k.FRONT)
        has_2 = any([bool(k.RIGHT), bool(k.TOP)])

        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)
        row.enabled = False
        row.alignment = "LEFT"
        row.label(text="Select Mode")
        row = col.row(align=True)
        row.prop(k, "geo", text="", expand=False)
        row = col.row(align=True)
        row.enabled = False
        row.alignment = "LEFT"

        if k.geo == "BOOLEAN":
            row.label(text="Load Images")
            row = layout.row(align=True)
            row.prop(k, "autofill")
            row = layout.row(align=True)
            row.operator(
                "ke.i2m_filebrowser", text="Front   ", icon="FILEBROWSER"
            ).axis = "FRONT"
            row.prop(k, "FRONT", text="")
            row.operator("ke.i2m_clearslot", text="", icon="X").axis = "FRONT"
            row = layout.row(align=True)
            if not has_front:
                row.enabled = False
            row.operator(
                "ke.i2m_filebrowser", text="Right   ", icon="FILEBROWSER"
            ).axis = "RIGHT"
            row.prop(k, "RIGHT", text="")
            row.operator("ke.i2m_clearslot", text="", icon="X").axis = "RIGHT"
            row = layout.row(align=True)
            if not has_front:
                row.enabled = False
            row.operator(
                "ke.i2m_filebrowser", text="Top      ", icon="FILEBROWSER"
            ).axis = "TOP"
            row.prop(k, "TOP", text="")
            row.operator("ke.i2m_clearslot", text="", icon="X").axis = "TOP"

            row = layout.row(align=True)
            row.scale_y = 0.5
            row.enabled = False
            row.label(text="Extra Textures Only:")

            row = layout.row(align=True)
            if not has_front or not has_2:
                row.enabled = False
            row.scale_y = 1
            row.operator(
                "ke.i2m_filebrowser", text="Back    ", icon="FILEBROWSER"
            ).axis = "BACK"
            row.prop(k, "BACK", text="")
            row.operator("ke.i2m_clearslot", text="", icon="X").axis = "BACK"
            row = layout.row(align=True)
            if not has_front or not has_2:
                row.enabled = False
            row.operator(
                "ke.i2m_filebrowser", text="Left     ", icon="FILEBROWSER"
            ).axis = "LEFT"
            row.prop(k, "LEFT", text="")
            row.operator("ke.i2m_clearslot", text="", icon="X").axis = "LEFT"
            row = layout.row(align=True)
            if not has_front or not has_2:
                row.enabled = False
            row.operator(
                "ke.i2m_filebrowser", text="Bottom", icon="FILEBROWSER"
            ).axis = "BOTTOM"
            row.prop(k, "BOTTOM", text="")
            row.operator("ke.i2m_clearslot", text="", icon="X").axis = "BOTTOM"
            row = layout.row(align=True)
            if not has_front:
                row.enabled = False
            row.operator("ke.i2m_clearslot", text="Clear All", icon="CANCEL").axis = (
                "ALL"
            )
        else:
            row.label(text="Load Image")
            row = col.row(align=True)
            row.operator("ke.i2m_filebrowser", text="", icon="FILEBROWSER").axis = (
                "FRONT"
            )
            row.prop(k, "FRONT", text="")
            row.operator("ke.i2m_clearslot", text="", icon="X").axis = "FRONT"

        row = layout.row(align=False)
        row.operator("ke.i2m_reload", text="Reload Image(s)", icon="LOOP_BACK")
        box = layout.box()
        box.operator("ke.i2m", text="Reset To Defaults").reset = True
        box.operator("ke.i2m_batchbrowser", icon="FILE_FOLDER")

        row = box.row()
        row.scale_y = 1.8
        if not has_front:
            row.enabled = False
        if k.geo == "BOOLEAN" and not has_2:
            row.enabled = False
        if k.geo == "BOOLEAN":
            row.operator("ke.i2m", text="Image To Mesh").reduce = "DISSOLVE"
        else:
            row.operator("ke.i2m", text="Image To Mesh")
