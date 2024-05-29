import numpy as np
from PyQt5.QtGui import QPixmap, QImage, QColor
from numba import jit


def is_binary(pixmap: QPixmap) -> bool:
    temp: QImage = pixmap.toImage()
    for y in range(temp.height()):
        for x in range(temp.width()):
            color: QColor = temp.pixelColor(x, y)
            _sum = color.redF() + color.greenF() + color.blueF()
            if not (_sum == 3 or _sum == 0):
                return False
    return True


@jit(nopython=True, cache=True, parallel=True)
def _to_binary(img_array: np.ndarray, threshold: float) -> np.ndarray:
    red_channel = img_array[:, :, 0] / 255.0
    green_channel = img_array[:, :, 1] / 255.0
    blue_channel = img_array[:, :, 2] / 255.0
    grayscale = 0.2126 * red_channel + 0.7152 * green_channel + 0.0722 * blue_channel
    bitmap = np.where((grayscale == 0) | ((grayscale < threshold) & (grayscale != 1)), 1, 0)
    return bitmap


def to_binary(pixmap: QPixmap, threshold: float) -> np.ndarray:
    temp: QImage = pixmap.toImage()
    img_data = temp.convertToFormat(QImage.Format_ARGB32_Premultiplied)
    ptr = img_data.constBits()
    ptr.setsize(img_data.byteCount())
    img_array = np.frombuffer(ptr, dtype=np.uint8).reshape((temp.height(), temp.width(), 4))
    bitmap = _to_binary(img_array, threshold)
    return bitmap.astype(np.ubyte)


@jit(nopython=True, cache=True, parallel=True)
def get_im_np(bitmap: np.ndarray) -> np.ndarray:
    height, width = bitmap.shape[:2]
    black = np.zeros((1, 3), dtype=np.uint8)
    white = np.full((1, 3), 255, dtype=np.uint8)
    im_np = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            if bitmap[y][x] == 0:
                im_np[y][x] = white
            else:
                im_np[y][x] = black
    return im_np


def get_image_by_bitmap(bitmap: np.ndarray) -> QImage:
    height, width = bitmap.shape[:2]
    im_np: np.ndarray = get_im_np(bitmap)
    image = QImage(im_np, width, height, im_np.strides[0], QImage.Format_RGB888)
    return image.copy()


@jit(nopython=True, cache=True, parallel=True)
def get_negative_bitmap(bitmap: np.ndarray) -> np.ndarray:
    return 1 - bitmap
