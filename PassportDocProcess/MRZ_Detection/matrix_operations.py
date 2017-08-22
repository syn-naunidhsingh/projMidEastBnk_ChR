
import numpy as np


def resizeBox(box, ratio_x, ratio_y):

    ref_box = []
    for el in box:
        ref_box.append([int(float(el[0])*ratio_x + 0.5), int(float(el[1])*ratio_y + 0.5)])

    return np.array(ref_box)

def resizeMinAreaRect(rect, transRatio):

    ref_rect = []
    print rect
    c_x, c_y = rect[0]
    w, h = rect[1]
    ag = rect[2]
    ref_rect.append((float(c_x) * transRatio , float(c_y) * transRatio))
    ref_rect.append((float(w) * transRatio , float(h) * transRatio ))
    ref_rect.append(ag)

    return tuple(ref_rect)


def resizeMRZRects(MRZRects, transRatio):

    ref_MRZRects = []

    for pairRect in MRZRects:

        mrzRect1 = resizeMinAreaRect(pairRect[0], transRatio)
        mrzRect2 = resizeMinAreaRect(pairRect[1], transRatio)
        ref_MRZRects.append([mrzRect1, mrzRect2])

    return ref_MRZRects
