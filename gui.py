#!/usr/bin/env python3
import os
import warnings

from PyQt5.QtCore import (
    QSize, QTimer, Qt, QByteArray, QBuffer, QIODevice
)
from PyQt5.QtGui import (
    QPalette, QColor
)
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QSizePolicy, QApplication, QPushButton, QFileDialog,
    QMessageBox, QProgressDialog
)

from anistate import AniState

try:
    import imageio
except ImportError:
    imageio = None
    warnings.warn('Export as video feature disabled, imageio module missing')


FPS = 60  # Frames Per Second at which to render the animation
DURATION = 5  # In seconds
CENTER = False  # Should everything be translated to the center?
BACKGROUND = QColor('#fff')


class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        pal = QPalette()
        pal.setColor(QPalette.Background, BACKGROUND)
        self.setPalette(pal)
        self.setAutoFillBackground(True)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.frame_no = 1

    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(400, 400)

    def next_animation_frame(self):
        self.update()
        self.frame_no += 1

    def export_video(self):
        if not imageio:
            return QMessageBox(
                QMessageBox.Information, 'Export not available',
                'imageio and ffmpeg must be installed to export videos'
            ).exec()

        location = QFileDialog.getSaveFileName(
            self, 'Choose export location', filter='Video (*.mp4)'
        )[0]
        if not location:
            return

        if not location.endswith('.mp4'):
            location += '.mp4'

        frame_count = int(DURATION * FPS)
        progress_box = QProgressDialog(
            'Recording and exporting video...', 'Cancel', 1, frame_count, self
        )
        progress_box.setWindowModality(Qt.WindowModal)
        with imageio.get_writer(location, format='mp4', mode='I',
                                fps=FPS, quality=6) as writer:
            self.frame_no = 1
            for i in range(frame_count):
                progress_box.setValue(i)
                if progress_box.wasCanceled():
                    os.remove(location)
                    return

                im_bytes = QByteArray()
                buf = QBuffer(im_bytes)
                buf.open(QIODevice.WriteOnly)
                self.grab().save(buf, 'PNG', 100)  # Triggers paintEvent
                self.frame_no += 1
                writer.append_data(imageio.imread(im_bytes.data(), 'png'))
        progress_box.setValue(progress_box.maximum())

        return QMessageBox(
            QMessageBox.Information, 'Completed',
            'Export finished! Saved to {}'.format(location)
        ).exec()

    def paintEvent(self, *args):
        (AniState(self)
         .size(5)
         .color((0, 0, 255, 64)).line(0, 0, self.width(), self.height())
         .color((0, 255, 0, 64)).line(0, self.height(), self.width(), 0)
         .size(self.frame_no)
         .color((255, 0, 0, 64)).point(self.width() / 2, self.height() / 2))


class Animake(QWidget):
    def __init__(self):
        super().__init__(None)
        self.setWindowTitle("Animake")
        self.setWindowFlags(Qt.Dialog)
        layout = QVBoxLayout(self)
        self.canvas = CanvasWidget()
        self.canvas.timer = QTimer(self)
        self.canvas.timer.timeout.connect(self.canvas.next_animation_frame)
        layout.addWidget(self.canvas)

        export_button = QPushButton("Export a video")
        export_button.pressed.connect(self.canvas.export_video)
        layout.addWidget(export_button)

        self.canvas.timer.start(int((1000 + FPS - 1) / FPS))


def main():
    app = QApplication([])
    win = Animake()
    win.show()
    return app.exec()


if __name__ == '__main__':
    main()
