# from libcpp.vector cimport vector
# cimport numpy as np
cimport cython
import numpy as np
cimport numpy as np


def mask_to_box(np.ndarray[dtype=np.float64_t, ndim=2] coords, xywh=True):
    """
    return:
        bouding box (List): 
    """
    cdef np.ndarray[dtype=np.float64_t, ndim=1] xs = coords[:, 0]
    cdef np.ndarray[dtype=np.float64_t, ndim=1] ys = coords[:, 1]
    cdef np.float64_t x_min, y_min, x_max, y_max

    x_min = min(xs)
    y_min = min(ys)
    x_max = max(xs)
    y_max = max(ys)

    if xywh:
        x_max = x_max - x_min
        y_max = y_max - y_min

    return [x_min, y_min, x_max, y_max]
