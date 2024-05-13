import numpy as np
from PyQt5.QtGui import QPixmap, QImage, QColor


def is_binary(pixmap: QPixmap) -> bool:
    temp: QImage = pixmap.toImage()
    for y in range(temp.height()):
        for x in range(temp.width()):
            color: QColor = temp.pixelColor(x, y)
            _sum = color.redF() + color.greenF() + color.blueF()
            if not (_sum == 3 or _sum == 0):
                return False
    return True


def to_binary(pixmap: QPixmap, threshold: float) -> np.ndarray:
    temp: QImage = pixmap.toImage()
    img_data = temp.convertToFormat(QImage.Format_ARGB32_Premultiplied)
    ptr = img_data.constBits()
    ptr.setsize(img_data.byteCount())
    img_array = np.frombuffer(ptr, dtype=np.uint8).reshape((temp.height(), temp.width(), 4))
    red_channel = img_array[:,:,0] / 255.0
    green_channel = img_array[:,:,1] / 255.0
    blue_channel = img_array[:,:,2] / 255.0
    grayscale = 0.2126 * red_channel + 0.7152 * green_channel + 0.0722 * blue_channel
    bitmap = np.where((grayscale == 0) | ((grayscale < threshold) & (grayscale != 1)), 1, 0)
    return bitmap.astype(np.uint8)


def get_image_by_bitmap(bitmap: np.ndarray) -> QImage:
    height, width = bitmap.shape[:2]
    black = np.zeros((1, 3), dtype=np.uint8)
    white = np.full((1, 3), 255, dtype=np.uint8)
    im_np = np.zeros((height, width, 3), dtype=np.uint8)

    im_np[bitmap == 0] = white
    im_np[bitmap == 1] = black

    image = QImage(im_np, width, height, im_np.strides[0], QImage.Format_RGB888)
    return image.copy()


def get_negative_bitmap(bitmap: np.ndarray) -> np.ndarray:
    new_bitmap = 1 - bitmap
    # h_img, w_img = bitmap.shape
    # for y in range(h_img):
    #     for x in range(w_img):
    #         if bitmap[y][x] == 1:
    #             new_bitmap[y][x] = 0
    #         else:
    #             new_bitmap[y][x] = 1
    return new_bitmap
