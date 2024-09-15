import bpy
from collections import Counter

kei2m_version = 1.307


def load_slot(path):
    try:
        img = bpy.data.images.load(path, check_existing=True)
    except (OSError, IOError, Exception):
        img = None
    return img


def is_bversion(req_ver):
    """Is current Blender version the required version (as int: #### )"""
    if int("".join([str(i) for i in bpy.app.version]).ljust(4, "0")) < req_ver:
        return False
    return True


def make_entry(h, width, w, pixels):
    idx = (h * width) + w
    px_index = idx * 4
    return pixels[px_index : px_index + 4]


def alpha_check(images, rgb=False, c2m=False):
    has_alpha = True
    for img in images:
        if img.depth != 32 and not rgb and not c2m:
            has_alpha = False
    return has_alpha


def reduce_colors(pixelmap, threshold=0.51, cap=None):
    colors = [p[2] for p in pixelmap if p[2][3] == 1]
    color_groups = []
    common_colors = [c for c in Counter(colors).most_common()]
    if cap is not None:
        if len(common_colors) > cap:
            common_colors = common_colors[:cap]
    for c in common_colors:
        rmin = c[0][0] - threshold
        rmax = c[0][0] + threshold
        gmin = c[0][1] - threshold
        gmax = c[0][1] + threshold
        bmin = c[0][2] - threshold
        bmax = c[0][2] + threshold
        similar = [[c][0]]
        for oc in reversed(common_colors):
            if oc != c:
                if (
                    rmin < oc[0][0] < rmax
                    and gmin < oc[0][1] < gmax
                    and bmin < oc[0][2] < bmax
                ):
                    similar.append(oc[0])
                    common_colors.remove(oc)
        color_groups.append(similar)
    for p in pixelmap:
        for i, g in enumerate(color_groups):
            if p[2] in g:
                p[2] = g[0][0]
    return pixelmap, [g[0][0] for g in color_groups]
