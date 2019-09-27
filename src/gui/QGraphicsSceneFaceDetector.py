from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from src.gui.DisplayCamera import DisplayCamera
import cv2


class QGraphicsSceneFaceDetector(QGraphicsScene):
    form_camera = None

    def __init__(self, form_cam, face_detector):
        # super(QWidget, self).__init__()
        super(QGraphicsSceneFaceDetector, self).__init__()
        self.form_camera = form_cam
        self.fps = 30
        self.face_detector = face_detector
        self.timer = None
        frame, time_capture = self.face_detector.capture()
        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.pix_item = self.addPixmap(QPixmap.fromImage(img))

    def setFPS(self, fps):
        self.fps = fps

    def nextFrameSlot(self):
        frame, time_capture = self.face_detector.capture()
        self.form_camera.status_message('Capture (s): {}'.format(str(time_capture)))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.pix_item.setPixmap(QPixmap.fromImage(img))
        self.form_camera.graphicsView.setScene(self)
        self.form_camera.graphicsView.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000./self.fps)

    def stop(self):
        self.timer.stop()

    def deleteLater(self):
        self.face_detector.stop()
        super(QGraphicsScene, self).deleteLater()


# class DisplayQGraphicsSceneCamera(QGraphicsScene, DisplayCamera, QThread):
#
#     face_detector = None
#
#     def __init__(self, form_camera, face_detector, parent=None):
#         QThread.__init__(self)
#         super(DisplayQGraphicsSceneCamera, self).__init__(parent)
#         self.form_camera = form_camera
#         self.isPressed = False
#         self.face_detector = face_detector
#
#     def __del__(self):
#         self.wait()
#
#     def run(self):
#         while True:
#             frame = self.face_detector.current_frame
#             qimg = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
#             pixmap = QPixmap.fromImage(qimg.rgbSwapped())
#             pixmap = pixmap.scaled(self.form_camera.graphicsView.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
#             self.addPixmap(pixmap)
#             self.form_camera.graphicsView.setScene(self)
#             self.form_camera.graphicsView.fitInView(self.sceneRect(), Qt.IgnoreAspectRatio)
#             # self.form_camera.graphicsView.show()






    # def mousePressEvent(self, event):
    #     position = QPointF(event.scenePos())
    #     self.x_init = position.x()
    #     self.y_init = position.y()
    #     self.latInitMap = self.lat_up - self.dlat*position.y()/self.height()
    #     self.lonInitMap = self.lon_left + self.dlon * position.x() / self.width()
    #     self.addPixmap(self.pixmap)
    #     self.isPressed = True
    #
    # def mouseMoveEvent(self, event):
    #     position = QPointF(event.scenePos())
    #     #TODO desenhar ao mover
    #     # if self.isPressed is True:
    #     #     mapSquare = Square()
    #     #     mapSquare.setRect(self.x_init, self.y_init, position.x() - self.x_init, position.y() - self.y_init)
    #     #     self.addItem(mapSquare)
    #     #     sleep(0.01)
    #     #     self.addPixmap(self.pixmap)
    #     #     # self.updateMap()
    #
    #     # TODO - erro de precisao .. maior area menor precisao
    #     try:
    #         self.latActualMap = max(self.lat_up - self.dlat * position.y() / self.height(), self.lat_down)
    #         self.lonActualMap = min(self.lon_left + self.dlon * position.x() / self.width(), self.lon_right)
    #         if self.isPressed is False:
    #             self.ramsinBrams.mapLat_up.setText('{:.2f}'.format(self.latActualMap))
    #             self.ramsinBrams.mapLon_Left.setText('{:.2f}'.format(self.lonActualMap))
    #         else:
    #             self.ramsinBrams.mapLat_Down.setText('{:.2f}'.format(self.latActualMap))
    #             self.ramsinBrams.mapLon_right.setText('{:.2f}'.format(self.lonActualMap))
    #     except:
    #         #TODO - tratar erro
    #         print("Unecpected error...")
    #         pass
    #
    #
    # def mouseReleaseEvent(self, event):
    #     self.latEndMap = self.latActualMap
    #     self.lonEndMap = self.lonActualMap
    #     position = QPointF(event.scenePos())
    #     mapSquare = Square()
    #     mapSquare.setRect(self.x_init,self.y_init, position.x()-self.x_init, position.y()-self.y_init)
    #     self.addItem(mapSquare)
    #     self.isPressed = False
