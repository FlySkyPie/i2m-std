import bpy


def load_slot(path):
    try:
        img = bpy.data.images.load(path, check_existing=True)
    except (OSError, IOError, Exception):
        img = None
    return img
