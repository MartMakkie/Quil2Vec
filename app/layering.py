from PySide6.QtWidgets import (QWidget, QLabel, QCheckBox, QSlider, QHBoxLayout, QVBoxLayout, QScrollArea, QGridLayout)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QImage, QColor, QPainter, QPen, QBrush, QPainterPath
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from app.FileHandling.fileHandler import Quil2VecImage
from app.core.martsLoggingHandler import get_logger

logger = get_logger("layering")

from PySide6.QtGui import QImage, Qt

def resize_qimage_to_width(image: QImage|QPixmap, target_width: int) -> QImage:
    # Calculate the target height to preserve aspect ratio
    aspect_ratio = image.height() / image.width()
    target_height = int(target_width * aspect_ratio)

    # Scale the image
    scaled_image = image.scaled(
        target_width,
        target_height,
        Qt.AspectRatioMode.KeepAspectRatio,  # Preserve aspect ratio
        Qt.TransformationMode.SmoothTransformation  # Smooth scaling
    )
    return scaled_image


class LayerWidget(QWidget):
    visibilityChanged = Signal(bool)
    opacityChanged = Signal(float)

    def __init__(self, layer, name, aspect_ratio=None, img_size=None,parent=None):
        super().__init__(parent)
        self.layer = layer  # Reference to the actual layer object
        self.name = name
        # Name Label
        self.name_label = QLabel(name)
        self.name_label.setAlignment(Qt.AlignLeft)

        # Thumbnail (dummy placeholder for now)
        self.thumbnail = QLabel()
        self.thumbnail.setFixedSize(64, 64)
        if type(layer) == Quil2VecImage:
            self.thumbnail.setPixmap(self.generate_thumbnail())
        else:
            self.thumbnail.setPixmap(self.generate_thumbnail(aspect_ratio, img_size))
        # Visibility checkbox
        self.visibility_checkbox = QCheckBox("Visible")
        self.visibility_checkbox.setChecked(layer.visible)
        self.visibility_checkbox.toggled.connect(self.on_visibility_toggled)

        # Opacity slider
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(int(layer.opacity * 100))
        self.opacity_slider.valueChanged.connect(self.on_opacity_changed)

        # Layout
        layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.thumbnail)
        hlayout.addWidget(self.name_label)
        layout.addLayout(hlayout)
        layout.addWidget(self.visibility_checkbox)
        layout.addWidget(self.opacity_slider)

        self.setLayout(layout)

    def generate_thumbnail(self, aspect_ratio=None, img_size=None):
        """Generate a thumbnail QPixmap of the layer content."""
        if type(self.layer ) == Quil2VecImage:
            img = self.layer.loadedImage
            img:QPixmap
            img = resize_qimage_to_width(img, 64)  # Resize to 64px width while preserving aspect ratio
            # img.scaled(QSize(), Qt.FastTransformation)
            return img
        else:
            if aspect_ratio and img_size:
                img = QPixmap(*img_size)  # Create a blank image with aspect ratio
            else:
                img = QPixmap(64, 64)
            painterPath = QPainterPath()
            for path in self.layer.paths:
                painterPath=path.paintToQPath(painterPath)
                # qPaths, sequences = path.to_qpath()
                # painterPath.addPath(qPaths)
            painter = QPainter(img)
            img.save('testThumbnail0.png')
            painter.drawPath(painterPath)
            img.save('testThumbnail1.png')
            painter.end()
            img.save('testThumbnail2.png')
            img = resize_qimage_to_width(img, 64)  # Resize to 64px width while preserving aspect ratio
            
            # img.scaledToWidth(64, Qt.FastTransformation)
        # img = QImage(64, 64, QImage.Format_ARGB32)
        # img.fill(QColor(200, 200, 200, 255))  # grey box
        return img#QPixmap.fromImage(img)

    def on_visibility_toggled(self, checked):
        self.layer.visible = checked
        self.visibilityChanged.emit(checked)

    def on_opacity_changed(self, value):
        self.layer.opacity = value / 100.0
        self.opacityChanged.emit(self.layer.opacity)


class LayerGridLayout(QGridLayout):
    def __init__(self, page, parent=None):
        super().__init__()
        self.page = page  # Reference to your Page object

        # Scroll area for layer list
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Container widget inside scroll area
        self.container = QWidget()
        self.container_layout = QVBoxLayout()
        self.container.setLayout(self.container_layout)

        self.scroll_area.setWidget(self.container)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        self.addLayout(main_layout, 0, 0)

        self.load_layers()

    def load_layers(self):
        """Load layers from the Page object into the panel."""
        self.container_layout.setSpacing(4)
        self.container_layout.setContentsMargins(0, 0, 0, 0)

        # Special background image layer
        # if hasattr(self.page, "background_image"):
        if not self.page.image.loadedImage:
            self.page.image.loadedImage = self.page.image.loadImage()
        aspect_ratio = self.page.image.aspect_ratio()
        bg_layer = LayerWidget(self.page.image, 'Original Image')
        bg_layer.visibilityChanged.connect(self.on_layer_changed)
        bg_layer.opacityChanged.connect(self.on_layer_changed)
        self.container_layout.addWidget(bg_layer)

        # Add all layers from Page
        for name, layer in self.page.layers.items():
            layer_widget = LayerWidget(layer, name, aspect_ratio, self.page.image.getImageSize())
            layer_widget.visibilityChanged.connect(self.on_layer_changed)
            layer_widget.opacityChanged.connect(self.on_layer_changed)
            self.container_layout.addWidget(layer_widget)

        self.container_layout.addStretch(1)

    def on_layer_changed(self, *_):
        """Called when any layer's visibility or opacity changes."""
        parent = self.parent()
        if parent is not None and hasattr(parent, 'file') and hasattr(parent.file, 'updateCanvas'):
            parent.file.updateCanvas()

# def generate_thumbnail(self, brush: QBrush):
#     img = QImage(64, 64, QImage.Format_ARGB32)
#     img.fill(Qt.transparent)
#     painter = QPainter(img)
#     painter.setRenderHint(QPainter.Antialiasing)

#     # pen = QPen(Qt.black)
#     # pen.setWidth(2)
#     # painter.setPen(pen)
#     # brush = QBrush(Qt.black)
#     painter.setBrush(brush)
#     for path in self.layer.vectors:  # assuming layer.vectors is a list of svg.path.Path
#         for segment in path:
#             painter.drawLine(segment.start.real, segment.start.imag,
#                              segment.end.real, segment.end.imag)

#     painter.end()
#     return QPixmap.fromImage(img)