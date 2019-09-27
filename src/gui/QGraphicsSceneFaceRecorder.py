from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# from src.gui.DisplayCamera import D
import cv2
import time
import src.controller.person_face_records_controller as pfrc


# TODO ou aqui deve ter uma nova thread, ao inves/alem de  ser no reconhecimento ???
# TODO refatorar para uma so classe (ja ta igual quase)
class QGraphicsSceneFaceRecorder(QGraphicsScene):
    form_camera = None

    def __init__(self, graphics_view, face_rec, control_suspect=None, control_graphics_face=None, main_form=None):
        super(QGraphicsSceneFaceRecorder, self).__init__()
        self.graphics_view = graphics_view
        self.control_suspect = control_suspect
        self.control_graphics_face = control_graphics_face
        self.main_form = main_form
        self.scene_face = None
        if control_graphics_face:
            self.scene_face = QGraphicsScene()
        self.fps = 56
        self.face_rec = face_rec
        self.frame = None
        self.face = None
        self.millis = 0
        self.timer = None
        self.frame, self.millis = self.face_rec.capture()
        img = QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
        self.pix_item = self.addPixmap(QPixmap.fromImage(img))

    def setFPS(self, fps):
        self.fps = fps

    def nextFrameSlot(self):
        self.frame, self.millis = self.face_rec.capture()
        if self.frame is None:
            return None
        if self.control_graphics_face:
            self.face = self.face_rec.current_face_image
            if self.face is not None:
                # TODO working poorly
                self.face = cv2.cvtColor(self.face, cv2.COLOR_BGR2RGB)
                img_face = QImage(self.face, self.face.shape[1], self.face.shape[0], QImage.Format_RGB888)
                self.scene_face.setPixmap(QPixmap.fromImage(img_face))
                self.control_graphics_face.setScene(self.scene_face)
                self.control_graphics_face.fitInView(self.scene_face.sceneRect(), Qt.KeepAspectRatio)
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        img = QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
        self.pix_item.setPixmap(QPixmap.fromImage(img))
        self.graphics_view.setScene(self)
        self.graphics_view.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
        if self.control_suspect:
            self.control_suspect.setText(self.face_rec.current_suspect_name)
            self.main_form.status_message('Recognition time in milliseconds: {}'.format(str(self.face_rec.recog_time_last)))

        if self.main_form is not None and self.main_form.control_auto_1 is not None and self.main_form.control_auto_1.isChecked() and len(self.face_rec.all_recog) > 0:
            # time.sleep(1)
            time_now = time.time()
            diff = time_now - self.face_rec.recog_timestamp_last
            if diff > self.face_rec.cam.recog_save_timeout:
                self.main_form.splashMessage('Timeout of {} seconds reached.\nRecording faces, please wait ...'.format(self.face_rec.cam.recog_save_timeout))
                # self.stop_timer()
                # self.face_rec.stop()
                self.face_rec.recognize()
                pfr = pfrc.create_pfr(self.face_rec.cam)
                self.face_rec.initialize(self.face_rec.train_exec, pfr, self.face_rec.video_capture)
                self.main_form.refresh_list_persons()
                self.main_form.refresh_list_control()
                self.main_form.clearSplash()
                # self.start_timer()

    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.start_timer()

    def start_timer(self):
        self.timer.start(1000. / self.fps)

    def stop_timer(self):
        self.timer.stop()

    def stop(self):
        self.stop_timer()

    def deleteLater(self):
        self.face_rec.stop()
        super(QGraphicsScene, self).deleteLater()


class TimerThread(QThread):

    def __init__(self, qgraphics):
        QThread.__init__(self)
        self.qgraphics = qgraphics

    def nextFrameSlot(self):
        self.qgraphics.nextFrameSlot()

    def run(self):
        while True:
            self.nextFrameSlot()
            time.sleep(1000. / self.qgraphics.fps)


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
