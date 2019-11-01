import re

import cv2
import numpy as np
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QFileDialog
from PyQt5.uic import loadUi


class Types:
    NORMAL = 'NORMAL'
    GRAY = 'GRAY'
    EQUALIZED = 'EQUALIZED'

    keys = (NORMAL, GRAY, EQUALIZED)


class MainWindow(QMainWindow):
    scenes, cv_images, cv_images_meta = {}, {}, {}

    def __init__(self):
        super().__init__()
        loadUi('ui/main_window.ui', self)
        self.__init__connections()
        self.__init_scenes()
        self.__prepare_images()
        self.__draw_images()

    def __init__connections(self):
        self.open.triggered.connect(self.open_image)
        self.save.triggered.connect(self.save_image)

    def __init_scenes(self):
        self.scenes.update({
            Types.NORMAL: QGraphicsScene(),
            Types.GRAY: QGraphicsScene(),
            Types.EQUALIZED: QGraphicsScene()
        })
        self.gv_normal.setScene(self.scenes[Types.NORMAL])
        self.gv_gray.setScene(self.scenes[Types.GRAY])
        self.gv_eq.setScene(self.scenes[Types.EQUALIZED])

    def __draw_images(self):
        if not self.cv_images:
            return

        for _type in Types.keys:
            scene, image = self.scenes.get(_type), self.cv_images.get(_type)
            if scene and image is not None:
                scene.addPixmap(QPixmap.fromImage(QImage(
                    image,
                    self.cv_images_meta['width'],
                    self.cv_images_meta['height'],
                    self.cv_images_meta['byte_value'],
                    QImage.Format_RGB888
                )))

    def __prepare_images(self, image_uri='src/coffee.jpg'):
        cv_image = cv2.imread(image_uri)
        height, width, byte_value = cv_image.shape
        byte_value = byte_value * width

        normal_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)  # Приведення в RGB формат
        gray_rgb = cv2.cvtColor(cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2RGB)  # Сіре зображення
        eq_rgb = cv2.threshold(gray_rgb, 127, 255, 0)[1]

        self.cv_images_meta = {
            'width': width,
            'height': height,
            'byte_value': byte_value
        }
        self.cv_images = {
            Types.NORMAL: normal_rgb,
            Types.GRAY: gray_rgb,
            Types.EQUALIZED: eq_rgb,
        }

    @staticmethod
    def __write_image(image, uri, name='default_image_name', suffix=''):
        cv2.imwrite(uri.format(name=name, suffix=suffix), image)

    @pyqtSlot()
    def save_image(self):
        search_regex = r'[\w\\/\:\-\.\s]+/(?P<name>\w+)\.jpg$'
        replace_regex = r'([\w\\/\:\-\.\s]+/)(?P<name>\w+)(\.jpg$)'
        if self.cv_images:
            file_uri = QFileDialog.getSaveFileName(self, 'Save', '/Users/mac', 'Images (*.jpg)')[0]
            if not file_uri:
                return

            file_name = re.match(search_regex, file_uri).group(1)
            file_uri = re.sub(replace_regex, r'\1{name}{suffix}\3', file_uri)

            self.__write_image(self.cv_images[Types.GRAY], file_uri, file_name)
            self.__write_image(self.cv_images[Types.EQUALIZED], file_uri, file_name, '_eq')

    @pyqtSlot()
    def open_image(self):
        image_uri = QFileDialog.getOpenFileName(self, 'Save', '/Users/mac', 'Images (*.jpg)')[0]
        if not image_uri:
            return

        self.__prepare_images(image_uri)
        self.__draw_images()
