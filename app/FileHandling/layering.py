from app.FileHandling.fileHandler import Quill2VecFileLayer, Quill2VecPage

from PySide6.QtWidgets import QHBoxLayout, QLabel, QCheckBox, QGridLayout, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QImage


class Quilll2VecBackgroundImage:
    def __init__(self, image, visibile):
        self.image = image
        self.visible = visibile
    @classmethod
    def fromLoadState(self, imagePath, visible):
        pass


    def toggle_visibility(self, state:bool):
        self.visible = state

def makeThumbnail(inImage) -> QImage:
    pass

def makeThumbnailFromSVG(inSVG):
    pass

def generateLayerLinks(inPage:Quill2VecPage, parentLayout):

    for layer in layers:
        layerLayoutGrid = QHBoxLayout()
        layerName = layer.name 
        layerLayoutGrid.setObjectName(layerName+'LayoutGrid')
        layerImageThumbnail = makeThumbnailFromSVG()
    originalImageLayout = QHBoxLayout(parentLayout)
    originalImageLayout.setObjectName(u"OriginalImageLayerLayout")
    originalImagVisibilityCheckBox = QCheckBox(originalImageLayout)
    originalImagVisibilityCheckBox.setChecked(inPage.backgroundImage.visibile)
    originalImagVisibilityCheckBox.connect(inPage.backgroundImage.toggle_visibility)
    originalImageThumbnail = makeThumbnail(inPage.backgroundImage.image)
    originalImageThumbnailScene = QGraphicsScene(originalImageThumbnail)
    originalImageThumbnailScene.addItem()
    originalImageThumbnailView = QGraphicsView(originalImageThumbnailScene, originalImageLayout)
    originalImageThumbnailView.setObjectName(f'OriginalImageLayerPreview')
    originalImageLayout.set
    originalImageThumbnailView.set


#######

from PySide6.QtWidgets import (QWidget, QLabel, QCheckBox, QSlider, QHBoxLayout, QVBoxLayout, QScrollArea)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QImage, QColor, QPainter, QPen, QBrush
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea


class LayerWidget(QWidget):
    visibilityChanged = Signal(bool)
    opacityChanged = Signal(float)

    def __init__(self, layer, parent=None):
        super().__init__(parent)
        self.layer = layer  # Reference to the actual layer object

        # Name Label
        self.name_label = QLabel(layer.name)
        self.name_label.setAlignment(Qt.AlignLeft)

        # Thumbnail (dummy placeholder for now)
        self.thumbnail = QLabel()
        self.thumbnail.setFixedSize(64, 64)
        self.thumbnail.setPixmap(self.generate_thumbnail())

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

    def generate_thumbnail(self):
        """Generate a thumbnail QPixmap of the layer content."""
        # Placeholder thumbnail; replace with actual rendering
        img = QImage(64, 64, QImage.Format_ARGB32)
        img.fill(QColor(200, 200, 200, 255))  # grey box
        return QPixmap.fromImage(img)

    def on_visibility_toggled(self, checked):
        self.layer.visible = checked
        self.visibilityChanged.emit(checked)

    def on_opacity_changed(self, value):
        self.layer.opacity = value / 100.0
        self.opacityChanged.emit(self.layer.opacity)


class LayerPanel(QWidget):
    def __init__(self, page, parent=None):
        super().__init__(parent)
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
        self.setLayout(main_layout)

        self.load_layers()

    def load_layers(self):
        """Load layers from the Page object into the panel."""
        self.container_layout.setSpacing(4)
        self.container_layout.setContentsMargins(0, 0, 0, 0)

        # Special background image layer
        if hasattr(self.page, "background_image"):
            bg_layer = LayerWidget(self.page.background_image)
            bg_layer.visibilityChanged.connect(self.on_layer_changed)
            bg_layer.opacityChanged.connect(self.on_layer_changed)
            self.container_layout.addWidget(bg_layer)

        # Add all layers from Page
        for layer in self.page.layers:
            layer_widget = LayerWidget(layer)
            layer_widget.visibilityChanged.connect(self.on_layer_changed)
            layer_widget.opacityChanged.connect(self.on_layer_changed)
            self.container_layout.addWidget(layer_widget)

        self.container_layout.addStretch(1)

    def on_layer_changed(self, *_):
        """Called when any layer's visibility or opacity changes."""
        self.parent().update_canvas()

def generate_thumbnail(self, brush: QBrush):
    img = QImage(64, 64, QImage.Format_ARGB32)
    img.fill(Qt.transparent)
    painter = QPainter(img)
    painter.setRenderHint(QPainter.Antialiasing)

    # pen = QPen(Qt.black)
    # pen.setWidth(2)
    # painter.setPen(pen)
    # brush = QBrush(Qt.black)
    painter.setBrush(brush)
    for path in self.layer.vectors:  # assuming layer.vectors is a list of svg.path.Path
        for segment in path:
            painter.drawLine(segment.start.real, segment.start.imag,
                             segment.end.real, segment.end.imag)

    painter.end()
    return QPixmap.fromImage(img)