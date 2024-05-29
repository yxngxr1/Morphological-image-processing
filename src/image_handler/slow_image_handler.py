import numpy as np
from PyQt5.QtGui import QImage, QColor


# def to_binary(pixmap: QPixmap, threshold: float) -> np.ndarray:
#     temp: QImage = pixmap.toImage()
#     bitmap: np.array = np.zeros((temp.height(), temp.width()), dtype=np.uint8)
#     for y in range(temp.height()):
#         for x in range(temp.width()):
#             color: QColor = temp.pixelColor(x, y)
#             _sum = (0.2126 * color.redF() + 0.7152 * color.greenF() + 0.0722 * color.blueF())
#             if _sum == 0:
#                 bitmap[y][x] = 1
#             elif _sum == 1:
#                 bitmap[y][x] = 0
#             else:
#                 if _sum > threshold:
#                     bitmap[y][x] = 0
#                 else:
#                     bitmap[y][x] = 1
#     return bitmap


# def get_image(bitmap: np.array) -> QImage:
#     height = bitmap.shape[0]
#     width = bitmap.shape[1]
#     white: QColor = QColor(255, 255, 255)
#     black: QColor = QColor(0, 0, 0)
#     image: QImage = QImage(width, height, QImage.Format_RGB888)
#     for y in range(height):
#         for x in range(width):
#             bit = bitmap[y][x]
#             if bit == 0:
#                 image.setPixelColor(x, y, white)
#             else:
#                 image.setPixelColor(x, y, black)
#     return image


# def get_array_from_image(image: QImage) -> np.ndarray:
#     im_in = image.convertToFormat(QImage.Format_RGB32)
#     color_bitmap: np.ndarray = np.zeros((image.height()* image.width()* 3))
#     t = 1
#     for i in range(im_in.height()):
#         a = im_in.scanLine(i)
#         a.setsize(16)
#         cv_im_in = np.array(a, copy=True).reshape(1, 16, 1)
#         for j in range(len(cv_im_in[0])):
#             print(cv_im_in[0][j][0])
#             color_bitmap[i * 16 + j] = cv_im_in[0][j][0]
#         t += 1
#     color_bitmap = np.array(color_bitmap, copy=True).reshape(im_in.height(), im_in.width(), 3)
#     print(color_bitmap)
#     ptr = im_in.constBits()
#     print(ptr.getsize(), im_in.height(), im_in.width())
#     ptr.setsize(im_in.byteCount())
#     cv_im_in = np.array(ptr, copy=True).reshape(im_in.height(), im_in.width(), 3)
#     return cv_im_in


# def get_bitmap(image: QImage, threshold: float) -> np.ndarray:
#     bitmap: np.ndarray = np.zeros((image.height(), image.width()), dtype=bool)
#     color_map: np.ndarray = get_array_from_image(image)
#
#     print(color_map)
#     for y in range(image.height()):
#         for x in range(image.width()):
#             redF = color_map[y][x][0] / 255
#             greenF = color_map[y][x][1] / 255
#             blueF = color_map[y][x][2] / 255
#             _sum = (0.2126 * redF + 0.7152 * greenF + 0.0722 * blueF)
#             if _sum == 0:
#                 bitmap[y][x] = 1
#             elif _sum == 1:
#                 bitmap[y][x] = 0
#             else:
#                 if _sum > threshold:
#                     bitmap[y][x] = 0
#                 else:
#                     bitmap[y][x] = 1
#     return bitmap
