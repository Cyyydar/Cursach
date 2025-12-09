from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QRadioButton, QPushButton, 
    QDialog, QFormLayout, QDoubleSpinBox, QLabel, QButtonGroup
)
from gui.augmentMethodWidget import AugmentationMethodWidget
from PyQt5.QtCore import Qt

class AugmentationMethodRadio(AugmentationMethodWidget):
    def __init__(self, name: str, method_callable, parameters: dict = None, on_change_callable=None):
        QWidget.__init__(self)
        self.method = method_callable
        self.parameters = parameters or {}

        self.on_change_callable = on_change_callable

        self.name = name
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.button = QRadioButton(name)
        self.button.setEnabled(False)
        self.button.toggled.connect(self._trigger)
        #self.button.setCheckable(True)
        self.button.setAutoExclusive(False)
        self.layout.addWidget(self.button)

        self.settings_button = QPushButton("^")
        self.settings_button.setEnabled(False)
        self.settings_button.setFixedWidth(25)
        self.settings_button.clicked.connect(self.open_settings)
        if self.parameters:
            self.layout.addWidget(self.settings_button)

        self.param_widgets = {}
        for param_name, (default, min_val, max_val, step) in self.parameters.items():
            spin = QDoubleSpinBox()
            spin.setRange(min_val, max_val)
            spin.setSingleStep(step)
            spin.setValue(default)
            spin.valueChanged.connect(self._trigger)
            self.param_widgets[param_name] = spin

        self.dialog = QDialog(self)
        flags = Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint
        self.dialog.setWindowFlags(flags)

        self.dialog.setWindowTitle("Параметры")
        form = QFormLayout(self.dialog)

        for name, widget in self.param_widgets.items():
            form.addRow(QLabel(name), widget)

    def setEnabled(self, bool):
        self.button.setEnabled(bool)
        self.settings_button.setEnabled(bool)

    def open_settings(self):
        if self.dialog is None:
            raise("Окно не создано")
            
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()

    def is_selected(self):
        return self.button.isChecked()

    def get_params(self):
        return {name: widget.value() for name, widget in self.param_widgets.items()}
    
    def call_method(self, image):
        return super().call_method(image)


class AugmentationMethodGroup(QWidget):
    """
    Контейнер: объединяет несколько методов и позволяет выбрать один.
    """
    def __init__(self, methods: list):
        """
        :param title: Название блока (например: "Цветовые аугментации")
        :param methods: список объектов AugmentationMethodRadio
        """
        super().__init__()
        self.methods = methods
        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        self.setLayout(layout)


        self.none = AugmentationMethodRadio("None", None)
        self.none.button.setChecked(True)
        layout.addWidget(self.none)
        self.group.addButton(self.none.button)

        # Добавляем методы
        for m in self.methods:
            layout.addWidget(m)
            self.group.addButton(m.button)
    def is_enabled(self):
        if self.none.button.isChecked():
            return False
        return True
    
    def setEnabled(self, bool):
        self.none.setEnabled(bool)
        for method in self.methods:
            method.setEnabled(bool)
    
    def get_name(self):
        for method in self.methods:
            if method.button.isChecked():
                return method.name
        return "None"

    def get_selected_method(self):
        for method in self.methods:
            if method.is_selected():
                return method
        return None

    def call_method(self, image):
        method = self.get_selected_method()
        if method is None:
            return image
        return method.call_method(image)