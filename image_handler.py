import numpy as np
from PyQt5.QtGui import QPixmap, QImage, QColor


def is_binary(pixmap: QPixmap):
    temp: QImage = pixmap.toImage()
    for y in range(temp.height()):
        for x in range(temp.width()):
            color: QColor = temp.pixelColor(x, y)
            _sum = color.redF() + color.greenF() + color.blueF()
            if not (_sum == 3 or _sum == 0):
                return False
    return True


def to_binary(pixmap: QPixmap, threshold: float) -> np.array:
    temp: QImage = pixmap.toImage()
    bitmap: np.array = np.zeros((temp.height(), temp.width()), dtype=bool)
    for y in range(temp.height()):
        for x in range(temp.width()):
            color: QColor = temp.pixelColor(x, y)
            _sum = (0.2126 * color.redF() + 0.7152 * color.greenF() + 0.0722 * color.blueF())
            if _sum >= threshold:
                bitmap[y][x] = 0
            else:
                bitmap[y][x] = 1
    return bitmap


def get_image(bitmap: np.array) -> QImage:
    height = bitmap.shape[0]
    width = bitmap.shape[1]
    white: QColor = QColor(255, 255, 255)
    black: QColor = QColor(0, 0, 0)
    image: QImage = QImage(width, height, QImage.Format_RGB888)
    for y in range(height):
        for x in range(width):
            bit = bitmap[y][x]
            if bit == 0:
                image.setPixelColor(x, y, white)
            else:
                image.setPixelColor(x, y, black)
    return image
