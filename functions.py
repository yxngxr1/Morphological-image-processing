import numpy as np


def binary_erosion(bitmap: np.ndarray, struct: np.ndarray) -> np.ndarray:
    new_bitmap = np.zeros(bitmap.shape)
    h_img, w_img = bitmap.shape
    h_struct, w_struct = struct.shape
    for y in range(h_struct // 2, h_img - h_struct // 2):
        for x in range(w_struct // 2, w_img - w_struct // 2):
            #  bit = bitmap[y][x]
            bit_is_correct = True
            #if bitmap[y][x] == struct[h_struct//2][w_struct//2]:
            for y_s in range(-(h_struct//2), h_struct//2 + 1):
                for x_s in range(-(w_struct//2), w_struct//2 + 1):
                    if bitmap[y+y_s][x+x_s] != struct[y_s+h_struct//2][x_s+w_struct//2]:
                        bit_is_correct = False
                        break
                if not bit_is_correct:
                    break
            if bit_is_correct:
                new_bitmap[y][x] = 1
    return new_bitmap


def binary_dilation(bitmap: np.ndarray, struct: np.ndarray) -> np.ndarray:
    new_bitmap = np.zeros(bitmap.shape)
    h_img, w_img = bitmap.shape
    h_struct, w_struct = struct.shape
    for y in range(h_struct // 2, h_img - h_struct // 2):
        for x in range(w_struct // 2, w_img - w_struct // 2):
            #  bit = bitmap[y][x]
            if bitmap[y][x] == 1:
                for y_s in range(-(h_struct//2), h_struct//2 + 1):
                    for x_s in range(-(w_struct//2), w_struct//2 + 1):
                        new_bitmap[y+y_s][x+x_s] = struct[y_s+h_struct//2][x_s+w_struct//2]
    return new_bitmap


def binary_opening(bitmap: np.ndarray, struct: np.ndarray) -> np.ndarray:
    new_bitmap = binary_erosion(bitmap, struct)
    new_bitmap = binary_dilation(new_bitmap, struct)
    return new_bitmap


def binary_closing(bitmap: np.ndarray, struct: np.ndarray) -> np.ndarray:
    new_bitmap = binary_dilation(bitmap, struct)
    new_bitmap = binary_erosion(new_bitmap, struct)
    return new_bitmap
