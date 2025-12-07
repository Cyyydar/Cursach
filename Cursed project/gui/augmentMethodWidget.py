from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QPushButton, QDialog, QFormLayout, QDoubleSpinBox, QLabel
from PyQt5.QtCore import Qt

class AugmentationMethodWidget(QWidget):
    def __init__(self, name: str, method_callable, parameters: dict = None):
        super().__init__()
        self.method = method_callable
        self.parameters = parameters or {}
        
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        self.checkbox = QCheckBox(name)
        self.layout.addWidget(self.checkbox)
        
        # Кнопка для открытия настроек
        if self.parameters:
            self.settings_button = QPushButton("^")
            self.settings_button.setFixedWidth(25)
            self.settings_button.clicked.connect(self.open_settings)
            self.layout.addWidget(self.settings_button)

        self.create_param_window()
        

    def create_param_window(self):
        self.param_widgets = {}
        for param_name, (default, min_val, max_val, step) in self.parameters.items():
            spin = QDoubleSpinBox()
            spin.setRange(min_val, max_val)
            spin.setSingleStep(step)
            spin.setValue(default)
            self.param_widgets[param_name] = spin

        self.dialog = QDialog(self)
        flags = Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint
        self.dialog.setWindowFlags(flags)
        
        self.dialog.setWindowTitle("Параметры")
        self.form = QFormLayout(self.dialog)

        for name, widget in self.param_widgets.items():
            self.form.addRow(QLabel(name), widget)


    def open_settings(self):
        """Открывает попап для редактирования параметров."""
        if self.dialog is None:
            raise("Окно не создано")
            
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()

    def is_enabled(self):
        return self.checkbox.isChecked()

    def get_params(self):
        return {name: widget.value() for name, widget in self.param_widgets.items()}

    def call_method(self, image):
        if self.is_enabled():
            params = self.get_params()
            return self.method(image, **params)
        return image