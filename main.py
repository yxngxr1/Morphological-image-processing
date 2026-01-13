import sys
import time
from pathlib import Path

import numpy as np
from PyQt5 import QtCore, QtWebEngineWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QEvent, Qt, QPoint, QFile, QTextStream, QUrl
from PyQt5.QtGui import QPixmap, QImage, QImageWriter, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QMessageBox, QDialog, QVBoxLayout, \
    QTextBrowser
from skimage.morphology import binary_closing, binary_erosion, binary_dilation, binary_opening, rectangle, disk, \
    octagon, diamond

from src.image_handler import morphology, image_handler
from src.design.design import Ui_MainWindow


class WorkerThread(QThread):
    result_ready = pyqtSignal(str)

    def run(self):
        for i in range(2):
            structure: np.ndarray = np.array([
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, 1]
            ])
            warmup_bitmap = np.random.randint(i, 2, (2024, 2024), dtype=np.uint8)
            warmup_colors = np.random.randint(0, 256, (2024, 2024, 4), dtype=np.uint8)

            morphology.binary_erosion(warmup_bitmap, structure)
            morphology.binary_dilation(warmup_bitmap, structure)
            morphology.binary_opening(warmup_bitmap, structure)
            morphology.binary_closing(warmup_bitmap, structure)

            image_handler._to_binary(warmup_colors, 0.5)
            image_handler.get_image_by_bitmap(warmup_bitmap)
            image_handler.get_negative_bitmap(warmup_bitmap)
        result = "Функции прогреты"
        self.result_ready.emit(result)  # Отправка результата через сигнал


class Morph(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Morph, self).__init__(parent)
        self.setupUi(self)

        self.window_title = 'Морфологическая обработка изображений'
        self.setWindowTitle(self.window_title)

        self.file_path: str = ""
        self.pixmap_src: QPixmap = None
        self.pixmap_load: QPixmap = None
        self.pixmap_processed: QPixmap = None
        self.pixmap_structure: QPixmap = None
        self.bitmap_load: np.ndarray = None
        self.bitmap_processed: np.ndarray = None
        self.threshold: int = None

        # status
        self.label_status = QLabel()
        self.statusbar.addWidget(self.label_status)

        # structure
        self.structure: np.ndarray = None
        self.combo_box_h.setCurrentIndex(0)
        self.combo_box_w.setCurrentIndex(0)
        self.update_structure()

        # buttons
        self.btn_process.clicked.connect(self.process)
        self.btn_to_black.clicked.connect(self.to_black)
        self.btn_clear.clicked.connect(self.clear)
        self.btn_negative.clicked.connect(self.negative)
        self.btn_struct_create.clicked.connect(self.struct_create)
        self.btn_src.clicked.connect(self.show_src)

        self.check_box_auto_process.clicked.connect(self.auto_process)
        self.check_box_auto_threshold.clicked.connect(self.auto_threshold)

        # menu buttons
        self.action_open.triggered.connect(self.open_image)
        self.action_save.triggered.connect(self.save_image)
        self.action_about.triggered.connect(self.open_about)
        self.action_author.triggered.connect(self.open_author)

        # slider
        self.horizontal_slider.valueChanged.connect(self.slider_update)
        self.slider_update()

        # set image structure
        image = image_handler.get_image_by_bitmap(self.structure)
        self.pixmap_structure = QPixmap.fromImage(image)
        self.set_pixmap_on_label(self.label_struct_image, self.pixmap_structure)

        # warmup jit functions
        self.worker = WorkerThread()
        self.worker.result_ready.connect(self.on_result_ready)
        self.worker.start()

        self.label_struct_image.installEventFilter(self)

    def update_structure(self):
        h, w = map(int, [self.combo_box_h.currentText(), self.combo_box_w.currentText()])
        if self.radio_full.isChecked():
            self.structure = rectangle(h, w)
        elif self.radio_plus.isChecked():
            self.structure = np.zeros((h, w), dtype=int)
            self.structure[h // 2, :] = 1  # горизонтальная линия
            self.structure[:, w // 2] = 1  # вертикальная линия
        elif self.radio_cross.isChecked():
            if h == w:
                size = h
                self.structure = np.zeros((size, size), dtype=int)
                np.fill_diagonal(self.structure, 1)
                np.fill_diagonal(np.fliplr(self.structure), 1)
            else:
                self.label_status.setText("Структурный элемент должен быть квадратным")
        elif self.radio_circle.isChecked():
            if h == w:
                self.structure = disk(h//2)
            else:
                self.label_status.setText("Структурный элемент должен быть квадратным")
        elif self.radio_octagon.isChecked():
            if h == w:
                octagon_mask = octagon(h // 2 + 1, h // 4)
                oct_h, oct_w = octagon_mask.shape
                self.structure = np.zeros((h, w), dtype=np.uint8)
                center_y, center_x = h // 2, w // 2
                start_y = center_y - oct_h // 2
                start_x = center_x - oct_w // 2
                self.structure[start_y:start_y + oct_h, start_x:start_x + oct_w] = octagon_mask
            else:
                self.label_status.setText("Структурный элемент должен быть квадратным")
        elif self.radio_diamond.isChecked():
            if h == w:
                self.structure = diamond(h//2)
            else:
                self.label_status.setText("Структурный элемент должен быть квадратным")
        image = image_handler.get_image_by_bitmap(self.structure)
        self.pixmap_structure = QPixmap.fromImage(image)
        self.set_pixmap_on_label(self.label_struct_image, self.pixmap_structure)

    def struct_create(self):
        self.update_structure()

    def draw_pixel(self, pos: QPoint, color: QColor):
        pixels_h, pixels_w = self.pixmap_structure.height(), self.pixmap_structure.width()
        image_h, image_w = self.label_struct_image.pixmap().height(), self.label_struct_image.pixmap().width()
        label_h, label_w = self.label_struct_image.height(), self.label_struct_image.width()

        offset_x = (label_w - image_w) / 2
        offset_y = (label_h - image_h) / 2

        # print(image_w, image_h, pixels_w, pixels_h, label_w, label_h)
        # print(pos.x(), pos.y())
        if not (offset_x <= pos.x() <= offset_x + image_w and
                offset_y <= pos.y() <= offset_y + image_h):
            raise ValueError("Выход за пределы label")

        x = ((pos.x() - offset_x) / (image_w / pixels_w))
        y = ((pos.y() - offset_y) / (image_h / pixels_h))

        # print(x, y)
        # print()
        painter = QPainter(self.pixmap_structure)
        painter.setPen(color)  # Черный цвет
        painter.drawPoint(int(x), int(y))  # Рисуем точку в позиции курсора
        painter.end()
        self.set_pixmap_on_label(self.label_struct_image, self.pixmap_structure)  # Обновить QLabel для отображения изменений
        self.structure = image_handler.to_binary(self.pixmap_structure, 0.5)

    def eventFilter(self, source, event):
        try:
            if source == self.label_struct_image and event.type() in (QEvent.MouseButtonPress, QEvent.MouseMove):
                if event.buttons() & Qt.LeftButton:
                    self.draw_pixel(event.pos(), QColor(0, 0, 0))
                    return True
                if event.buttons() & Qt.RightButton:
                    self.draw_pixel(event.pos(), QColor(255, 255, 255))
                    return True
        except Exception as e:
            pass
            #print(e)
        return super().eventFilter(source, event)

    def on_result_ready(self, result):
        self.label_status.setText(f"{result}")

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
                self.bitmap_processed = morphology.binary_erosion(self.bitmap_load, self.structure)
            elif self.radio_dilation.isChecked():
                self.bitmap_processed = morphology.binary_dilation(self.bitmap_load, self.structure)
            elif self.radio_opening.isChecked():
                self.bitmap_processed = morphology.binary_opening(self.bitmap_load, self.structure)
            elif self.radio_closing.isChecked():
                self.bitmap_processed = morphology.binary_closing(self.bitmap_load, self.structure)

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
        if self.pixmap_src is None:
            self.label_status.setText("Изображение не загружено")
            return
        # if self.bitmap_load is not None:
        #     self.label_status.setText("Изображение уже в чб")
        #     return
        # if image_handler.is_binary(self.pixmap_load):
        #     self.label_status.setText("Изображение уже в чб")

        try:
            start_time = time.time()
            self.bitmap_load = image_handler.to_binary(self.pixmap_src, self.threshold)
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

    def show_src(self):
        if self.pixmap_src is None:
            self.label_status.setText("Изображение не загружено")
            return
        self.set_pixmap_on_label(self.label_load_image, self.pixmap_src)

    def clear(self):
        self.file_path: str = ""
        self.pixmap_src: QPixmap = None
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

        self.setWindowTitle(self.window_title)

    def open_image(self):
        file_path, options = QFileDialog.getOpenFileName(self, 'Open image', "", "Image files (*.jpg *.png *bmp *tif)")
        self.file_path = file_path
        if file_path:
            try:
                pixmap = QPixmap(file_path)
                self.pixmap_load = pixmap.copy()
                self.pixmap_src = pixmap.copy()
                self.set_pixmap_on_label(self.label_load_image, pixmap)

                self.bitmap_load = None
                self.bitmap_processed = None
                self.setWindowTitle(f"{self.window_title} - {file_path.split('/')[-1]} ({self.pixmap_src.width()}x{self.pixmap_src.height()})")

            except Exception as e:
                self.label_status.setText(str(e))

    def save_image(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", f"{self.file_path}",
                                                   "Image files (*bmp *.png *.jpg, *tif)")

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
        self.threshold = self.horizontal_slider.value() / 100
        self.label_slider_value.setText(f"{self.threshold}")

        if self.check_box_auto_threshold.isChecked():
            self.to_black()
            if self.check_box_auto_process.isChecked():
                self.process()

    def auto_process(self):
        if self.check_box_auto_process.isChecked():
            if not self.check_box_auto_threshold.isChecked():
                self.check_box_auto_threshold.setChecked(True)

    def auto_threshold(self):
        if not self.check_box_auto_threshold.isChecked():
            if self.check_box_auto_process.isChecked():
                self.check_box_auto_process.setChecked(False)

    from PyQt5 import QtWebEngineWidgets
    from pathlib import Path

    def open_about(self):
        # Создаем диалоговое окно
        dialog = QDialog(self)
        dialog.setWindowTitle("О программе")
        dialog.resize(800, 600)

        # Создаем layout
        layout = QVBoxLayout()

        # Создаем QWebEngineView
        view = QtWebEngineWidgets.QWebEngineView()

        try:
            # Читаем HTML-файл
            html_path = Path("help_page/about.html")
            html_content = html_path.read_text(encoding="utf-8")

            base_url = QUrl.fromLocalFile(str(html_path.parent) + "/")

            print(f"HTML path: {html_path}")
            print(f"Base URL: {base_url}")
            print(f"Image exists: {Path('help_page/images/ui_form.png').exists()}")
            html_path = Path("help_page/about.html").absolute()
            view.load(QUrl.fromLocalFile(str(html_path)))
        except Exception as e:
            view.setHtml(f"<h1>Ошибка</h1><p>Не удалось загрузить файл about.html: {str(e)}</p>")

        # Добавляем view в layout
        layout.addWidget(view)
        dialog.setLayout(layout)

        dialog.exec_()

    def open_author(self):

        author_info = """
        <center>
        <h3>Дипломная работа</h3>
        <p>Учебно-образовательная программа - базовые морфологические операция над изображениями</p>
        <br>
        <p><b>Студент:</b> Дерганов Г.Д.</p>
        <p><b>Научный руководитель:</b> Кудрина М.А.</p>
        <p><b>Группа:</b> 6402-090301</p>
        <p><b>Год:</b> 2025</p>
        </center>
        """

        msg = QMessageBox()
        msg.setWindowTitle("Информация об авторе")
        msg.setText(author_info)
        msg.setTextFormat(1)  # 1 означает RichText (HTML-форматирование)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MorphologicalProcess = Morph()
    MorphologicalProcess.show()
    sys.exit(app.exec_())
