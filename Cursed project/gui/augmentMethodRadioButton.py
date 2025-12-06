from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QRadioButton, QPushButton, 
    QDialog, QFormLayout, QDoubleSpinBox, QLabel, QButtonGroup
)
from PyQt5.QtCore import Qt

class AugmentationMethodRadio(QWidget):
    """
    Один метод внутри группы.
    """
    def __init__(self, name: str, method_callable, parameters: dict = None):
        super().__init__()
        self.method = method_callable
        self.parameters = parameters or {}

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.radio = QRadioButton(name)
        self.layout.addWidget(self.radio)

        if self.parameters:
            self.settings_button = QPushButton("^")
            self.settings_button.setFixedWidth(25)
            self.settings_button.clicked.connect(self.open_settings)
            self.layout.addWidget(self.settings_button)

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
        form = QFormLayout(self.dialog)

        for name, widget in self.param_widgets.items():
            form.addRow(QLabel(name), widget)

    def open_settings(self):
        """Открывает попап для редактирования параметров."""
        if self.dialog is None:
            raise("Окно не создано")
            
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()

    def is_selected(self):
        return self.radio.isChecked()

    def get_params(self):
        return {name: widget.value() for name, widget in self.param_widgets.items()}


class AugmentationMethodGroup(QWidget):
    """
    Контейнер: объединяет несколько методов и позволяет выбрать один.
    """
    def __init__(self, title: str, methods: list):
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


        none = AugmentationMethodRadio("None", None)
        layout.addWidget(none)
        self.group.addButton(none.radio)

        # Добавляем методы
        for m in self.methods:
            layout.addWidget(m)
            self.group.addButton(m.radio)

    def get_selected_method(self):
        """
        Возвращает (метод_функция, параметры) выбранного варианта.
        Если ничего не выбрано → None, {}.
        """
        for item in self.methods:
            if item.is_selected():
                return item.method, item.get_params()
        return None, {}

    def call_method(self, image):
        """
        Применяет выбранный метод к изображению.
        """
        method, params = self.get_selected_method()
        if method is None:
            return image
        return method(image, **params)
