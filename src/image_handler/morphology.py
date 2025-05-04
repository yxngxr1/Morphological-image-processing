import numpy as np
from numba import jit


@jit(nopython=True, cache=True, parallel=True)
def binary_erosion(bitmap: np.ndarray, struct: np.ndarray) -> np.ndarray:
    new_bitmap = np.zeros(bitmap.shape[:2])
    h_img, w_img = bitmap.shape[:2]
    h_struct, w_struct = struct.shape[:2]
    h_offset, w_offset = h_struct // 2, w_struct // 2
    for y in range(h_offset, h_img - h_offset):
        for x in range(w_offset, w_img - w_offset):
            bit_is_correct = True
            for y_s in range(h_struct):
                for x_s in range(w_struct):
                    if struct[y_s][x_s] == 1:
                        if struct[y_s][x_s] != bitmap[y + y_s - h_offset][x + x_s - w_offset]:
                            bit_is_correct = False
                            break
                if not bit_is_correct:
                    break
            if bit_is_correct:
                new_bitmap[y][x] = bitmap[y][x]
    return new_bitmap


@jit(nopython=True, cache=True, parallel=True)
def binary_dilation(bitmap: np.ndarray, struct: np.ndarray) -> np.ndarray:
    new_bitmap = np.zeros(bitmap.shape[:2])
    h_img, w_img = bitmap.shape[:2]
    h_struct, w_struct = struct.shape[:2]
    h_offset, w_offset = h_struct // 2, w_struct // 2
    for y in range(h_offset, h_img - h_offset):
        for x in range(w_offset, w_img - w_offset):
            if bitmap[y][x] == 1:
                for y_s in range(h_struct):
                    for x_s in range(w_struct):
                        if struct[y_s][x_s] == 1:
                            new_bitmap[y + y_s - h_offset][x + x_s - w_offset] = 1
    return new_bitmap


def binary_opening(bitmap: np.ndarray, struct: np.ndarray) -> np.ndarray:
    new_bitmap = binary_erosion(bitmap, struct)
    new_bitmap = binary_dilation(new_bitmap, struct)
    return new_bitmap


def binary_closing(bitmap: np.ndarray, struct: np.ndarray) -> np.ndarray:
    new_bitmap = binary_dilation(bitmap, struct)
    new_bitmap = binary_erosion(new_bitmap, struct)
    return new_bitmap
