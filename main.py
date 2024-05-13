import sys
import time

import numpy as np
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage, QImageWriter
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
from skimage.morphology import binary_closing, binary_erosion, binary_dilation, binary_opening

import functions
from design.design import Ui_MainWindow
import image_handler


class Morph(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Morph, self).__init__(parent)
        self.setupUi(self)

        self.file_path: str = ""
        self.pixmap_load: QPixmap = None
        self.pixmap_processed: QPixmap = None
        self.bitmap_load: np.ndarray = None
        self.bitmap_processed: np.ndarray = None
        self.threshold: int = None

        self.structure: np.ndarray = np.array([
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ])

        # buttons
        self.btn_process.clicked.connect(self.process)
        self.btn_to_black.clicked.connect(self.to_black)
        self.btn_clear.clicked.connect(self.clear)
        self.btn_negative.clicked.connect(self.negative)

        # menu buttons
        self.action_open.triggered.connect(self.open_image)
        self.action_save.triggered.connect(self.save_image)

        # slider
        self.horizontal_slider.valueChanged.connect(self.slider_update)
        self.slider_update()

    def process(self):
        if self.pixmap_load is None:
            self.label_status.setText("Изображение не загружено")
            return
        if self.bitmap_load is None:
            self.label_status.setText("Создайте бинарное изображение (Ч/Б)")
            return
        if not self.struct_is_correct():
            self.label_status.setText("Структурный элемент не подходит по размеру")
            return

        start_time = time.time()
        if self.combo_box_alg.currentText() == "По алгоритму":
            if self.radio_erosion.isChecked():
                self.bitmap_processed = functions.binary_erosion(self.bitmap_load, self.structure)
            elif self.radio_dilation.isChecked():
                self.bitmap_processed = functions.binary_dilation(self.bitmap_load, self.structure)
            elif self.radio_opening.isChecked():
                self.bitmap_processed = functions.binary_opening(self.bitmap_load, self.structure)
            elif self.radio_closing.isChecked():
                self.bitmap_processed = functions.binary_closing(self.bitmap_load, self.structure)

        elif self.combo_box_alg.currentText() == "Scikit-Image":
            if self.radio_erosion.isChecked():
                self.bitmap_processed = binary_erosion(self.bitmap_load, self.structure)
            elif self.radio_dilation.isChecked():
                self.bitmap_processed = binary_dilation(self.bitmap_load, self.structure)
            elif self.radio_opening.isChecked():
                self.bitmap_processed = binary_opening(self.bitmap_load, self.structure)
            elif self.radio_closing.isChecked():
                self.bitmap_processed = binary_closing(self.bitmap_load, self.structure)

        process_time = round(time.time() - start_time, 3)

        start_time = time.time()
        image = image_handler.get_image_by_bitmap(self.bitmap_processed)
        draw_time = round(time.time() - start_time, 3)

        self.pixmap_processed = QPixmap.fromImage(image)
        self.set_pixmap_on_label(self.label_processed_image, self.pixmap_processed)
        self.label_status.setText(f"Обработано за {process_time}с, отрисовка: {draw_time}с")

    def to_black(self):
        if self.pixmap_load is None:
            self.label_status.setText("Изображение не загружено")
            return
        # if self.bitmap_load is not None:
        #     self.label_status.setText("Изображение уже в чб")
        #     return
        # if image_handler.is_binary(self.pixmap_load):
        #     self.label_status.setText("Изображение уже в чб")

        try:
            start_time = time.time()
            self.bitmap_load = image_handler.to_binary(self.pixmap_load, self.threshold)
            process_time = round(time.time() - start_time, 3)

            #self.bitmap_load = image_handler.get_bitmap(self.pixmap_load.toImage(), self.threshold)

            start_time = time.time()
            image = image_handler.get_image_by_bitmap(self.bitmap_load)
            draw_time = round(time.time() - start_time, 3)

            self.pixmap_load = QPixmap(image)
            self.set_pixmap_on_label(self.label_load_image, self.pixmap_load)
            self.label_status.setText(f"Изображение преобразовано в чб за {process_time}, отрисовка {draw_time}с")
        except Exception as e:
            print(e)
            self.label_status.setText(str(e))

    def negative(self):
        if self.pixmap_load is None:
            self.label_status.setText("Изображение не загружено")
            return
        if self.bitmap_load is None:
            self.label_status.setText("Создайте бинарное изображение (Ч/Б)")
            return

        start_time = time.time()
        self.bitmap_load = image_handler.get_negative_bitmap(self.bitmap_load)
        process_time = round(time.time() - start_time, 3)

        start_time = time.time()
        image = image_handler.get_image_by_bitmap(self.bitmap_load)
        draw_time = round(time.time() - start_time, 3)

        self.pixmap_load = QPixmap(image)
        self.set_pixmap_on_label(self.label_load_image, self.pixmap_load)
        self.label_status.setText(f"Изображение преобразовано в негативное за {process_time}, отрисовка {draw_time}с")

    def clear(self):
        self.file_path: str = ""
        self.pixmap_load: QPixmap = None
        self.pixmap_processed: QPixmap = None
        self.bitmap_load: np.array = None
        self.bitmap_processed: np.array = None
        self.horizontal_slider.setValue(self.horizontal_slider.maximum() // 2)

        self.label_status.clear()
        self.label_load_image.clear()
        self.label_processed_image.clear()
        self.label_load_image.setText("Исходное изображение")
        self.label_processed_image.setText("Изображение после обработки")

    def open_image(self):
        file_path, options = QFileDialog.getOpenFileName(self, 'Open image', "", "Image files (*.jpg *.png *bmp)")
        self.file_path = file_path
        if file_path:
            try:
                pixmap = QPixmap(file_path)
                self.pixmap_load = pixmap
                self.set_pixmap_on_label(self.label_load_image, pixmap)

                self.bitmap_load = None
                self.bitmap_processed = None

                print()

            except Exception as e:
                self.label_status.setText(str(e))

    def save_image(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", f"{self.file_path}",
                                                   "Image files (*bmp *.png *.jpg)")

        if file_path:
            image: QImage = self.pixmap_processed.toImage()
            imagefile = QImageWriter()
            imagefile.setFileName(file_path)
            imagefile.setQuality(100)
            imagefile.write(image)
            self.label_status.setText(f"Изображение сохранено в: {file_path}")

    def struct_is_correct(self) -> bool:
        if self.bitmap_load is None:
            return False
        h_img, w_img = self.bitmap_load.shape
        h_struct, w_struct = self.structure.shape
        return (h_img >= h_struct) and (w_img >= w_struct)

    def set_pixmap_on_label(self, label: QLabel, pixmap: QPixmap):
        if pixmap:
            pixmap = pixmap.scaled(label.width(), label.height(), QtCore.Qt.KeepAspectRatio)
            label.setPixmap(pixmap)

    def resizeEvent(self, event):
        self.set_pixmap_on_label(self.label_load_image, self.pixmap_load)
        self.set_pixmap_on_label(self.label_processed_image, self.pixmap_processed)

    def slider_update(self):
        self.threshold = self.horizontal_slider.value() / 10
        self.label_slider_value.setText(f"{self.threshold}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MorphologicalProcess = Morph()
    MorphologicalProcess.show()
    sys.exit(app.exec_())
