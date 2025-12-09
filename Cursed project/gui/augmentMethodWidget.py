from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QPushButton, QDialog, QFormLayout, QDoubleSpinBox, QLabel
from PyQt5.QtCore import Qt

class AugmentationMethodWidget(QWidget):
    def __init__(self, name: str, method_callable, parameters: dict = None, on_change_callable=None):
        super().__init__()
        self.method = method_callable
        self.parameters = parameters or {}
        
        self.on_change_callable = on_change_callable
        
        self.name = name
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        self.button = QCheckBox(name)
        self.button.setEnabled(False)
        self.button.stateChanged.connect(self._trigger)
        self.layout.addWidget(self.button)
        
        # Кнопка для открытия настроек
        self.settings_button = QPushButton("^")
        self.settings_button.setEnabled(False)
        self.settings_button.setFixedWidth(25)
        self.settings_button.clicked.connect(self.open_settings)
        if self.parameters:
            self.layout.addWidget(self.settings_button)

        self.create_param_window()
        
    def setEnabled(self, bool):
        self.button.setEnabled(bool)
        self.settings_button.setEnabled(bool)

    def create_param_window(self):
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
        self.form = QFormLayout(self.dialog)

        for name, widget in self.param_widgets.items():
            self.form.addRow(QLabel(name), widget)

    def get_name(self) -> str:
        return self.name

    def open_settings(self):
        if self.dialog is None:
            raise("Окно не создано")
            
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()

    def is_enabled(self):
        return self.button.isChecked()

    def get_params(self):
        return {name: widget.value() for name, widget in self.param_widgets.items()}

    def call_method(self, image):
        if self.is_enabled():
            params = self.get_params()
            return self.method(image, **params)
        return image
    
    def _trigger(self):
        if self.on_change_callable:
            self.on_change_callable()