from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox,
    QPushButton, QWidget, QSizePolicy, QFrame, QDateEdit
)
from PyQt6.QtGui import QIcon, QDoubleValidator, QIntValidator
from PyQt6.QtCore import Qt, QSize, QDate
from pyqt6_multiselect_combobox import MultiSelectComboBox

class BaseEditWidget(QDialog):
    def __init__(self, mainTitle: str, iconPath: str = None, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon("assets/logos/logoIcon.png"))
        self.setWindowTitle("UtiliTrack - Edit Item")
        self.setModal(True)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.fields = {}

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(15)
        self.setObjectName("BaseEditWidget")

        self.setupTitleBar(mainTitle, iconPath)

        self.sections = {}
        self.fields = {}
        self.fieldsLayout = QHBoxLayout()
        self.fieldsLayout.setSpacing(10)
        self.mainLayout.addLayout(self.fieldsLayout)

        self.setupBaseStyle()

        self.addButton = QPushButton(f"Edit {mainTitle.split()[1]}")
        self.addButton.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                        stop:0.4 #3A0CA3, stop:1 #F72585);;
                color: white;
                font-family: "Urbanist";
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.4 #5A30D6, stop:1 #FF5FB2);
            }
        """)
        self.addButton.clicked.connect(self.onEditClicked)
        self.addButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mainLayout.addWidget(self.addButton)

        self.messageLabel = QLabel("")
        self.messageLabel.setStyleSheet("color: red; font-size: 14px; font-family: 'Urbanist';")
        self.messageLabel.setWordWrap(True)
        self.messageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.messageLabel)

    def setupTitleBar(self, mainTitle, iconPath):
        titleLayout = QHBoxLayout()
        titleLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        titleLayout.setSpacing(10)

        iconButton = QPushButton()
        iconButton.setFixedSize(30, 30)
        iconButton.setObjectName("iconButton")
        iconButton.setCursor(Qt.CursorShape.PointingHandCursor)

        if iconPath:
            icon = QIcon(iconPath)
            iconButton.setIcon(icon)
            iconButton.setIconSize(QSize(24, 24))
        else:
            iconButton.setText("")

        titleLabel = QLabel(mainTitle)
        titleLabel.setObjectName("mainTitle")
        titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        exitButton = QPushButton(icon=QIcon("assets/icons/exit.png"))
        exitButton.setFixedSize(45, 45)
        exitButton.setObjectName("exitButton")
        exitButton.setCursor(Qt.CursorShape.PointingHandCursor)
        exitButton.clicked.connect(self.handleExitClicked)

        titleLayout.addWidget(iconButton)
        titleLayout.addWidget(titleLabel)
        titleLayout.addStretch()
        titleLayout.addWidget(exitButton)

        self.mainLayout.addLayout(titleLayout)

    def setupBaseStyle(self):
        self.setStyleSheet("""
            QWidget#BaseEditWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #1C1C1C, 
                    stop: 1 #0A0A0A
                );
                padding: 15px;
            }
            QLabel#mainTitle {
                font-family: "Urbanist";
                font-size: 28px;
                font-weight: bold;
                color: white;
            }
            QLabel#heading {
                font-family: "Urbanist";
                font-size: 20px;
                font-weight: bold;
                color: white;
            }
            QLabel#label {
                font-family: "Urbanist";
                font-size: 15px;
                color: white;
            }
            QLabel#value {
                font-family: "Urbanist";
                font-size: 15px;
                color: white;
                font-weight: bold;
            }
            QFrame#card {
                background-color: #1C1C1C;
                border-radius: 15px;
                padding: 15px;
            }
            #iconButton {
                border: none;
                background-color: transparent;
            }
            QPushButton#exitButton {
                background-color: #2b2b2b;
                border: none;
                color: white;
                font-size: 30px;
                font-weight: bold;
                border-radius: 6px;
                padding: 5px;
            }
            QPushButton#exitButton:hover {
                background-color: #3b3b3b;
            }
            QLabel {
                font-family: "Urbanist";
                font-size: 16px;
                color: white;
            }
            QLineEdit {
                background-color: #1C1C1C;
                color: white;
                font-family: "Urbanist";
                font-size: 16px;
                border: 1px solid #2b2b2b;
                border-radius: 6px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #3b3b3b;
                font-family: "Urbanist";
                font-size: 16px;
            }
            QComboBox {
                background-color: #1C1C1C;
                color: white;
                border: 1px solid #2b2b2b;
                border-radius: 6px;
                padding: 5px;
                font-family: "Urbanist";
                font-size: 16px;
            }
            QComboBox:focus {
                border: 1px solid #3b3b3b;
            }
            QComboBox QAbstractItemView {
                background-color: #1C1C1C;
                color: white;
                font-family: "Urbanist";
                font-size: 16px;
                selection-background-color: #3b3b3b;
                selection-color: white;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #3b3b3b;
                color: white;
            }
            QListView::item:hover {
                background-color: #3b3b3b;
                color: white;
            }
            QSpinBox {
                background-color: #1C1C1C;
                color: white;
                font-family: "Urbanist";
                font-size: 16px;
                border: 1px solid #2b2b2b;
                border-radius: 6px;
                padding: 5px;
            }
            QSpinBox:focus {
                border: 1px solid #3b3b3b;
            }
            QPushButton {
                background-color: #1C1C1C;
                color: white;
                font-family: "Urbanist";
                font-size: 16px;
                border: 1px solid #2b2b2b;
                border-radius: 6px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #2b2b2b;
            }
                           
            QDateEdit {
                background-color: #1C1C1C;
                color: white;
                font-family: "Urbanist";
                font-size: 16px;
                border: 1px solid #2b2b2b;
                border-radius: 6px;
                padding: 5px;
            }
            QDateEdit:focus {
                border: 1px solid #3b3b3b;
            }

            QDateEdit QCalendarWidget {
                background-color: #1C1C1C;
                font-family: "Urbanist";
                font-size: 16px;
                color: white;
                border: 1px solid #2b2b2b;
            }
            QDateEdit QCalendarWidget QAbstractItemView {
                background-color: #1C1C1C;
                color: white;
            }
            QDateEdit QCalendarWidget QAbstractItemView:focus {
                border: 1px solid #3b3b3b;
            }
            QDateEdit QCalendarWidget QAbstractItemView:disabled {
                color: #888888;
            }
        """)
    
    def addSection(self, title: str):
        sectionContainer = QWidget()
        sectionLayout = QVBoxLayout(sectionContainer)
        sectionLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sectionLayout.setSpacing(10)
        sectionContainer.setMinimumWidth(300)

        titleLabel = QLabel(title)
        titleLabel.setStyleSheet("font-weight: bold; font-size: 16px;")  # Optional styling
        sectionLayout.addWidget(titleLabel)

        self.fieldsLayout.addWidget(sectionContainer)
        self.sections[title] = sectionLayout
        return sectionLayout
        
    def _addField(self, label: str, widget: QWidget, sectionTitle: str | None = None, isVisible: bool = True):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(5)

        labelWidget = QLabel(label)
        labelWidget.setVisible(isVisible)
        layout.addWidget(labelWidget)
        layout.addWidget(widget)

        if sectionTitle and sectionTitle in self.sections:
            self.sections[sectionTitle].addWidget(container)
        else:
            self.fieldsLayout.addWidget(container)

        self.fields[label] = (labelWidget, widget)
        widget.setVisible(isVisible)
        return widget
    
    def addFloatInput(self, label: str, minValue=0, maxValue=999999999, sectionTitle: str | None = None, defaultValue: float = 0.0):
        lineEdit = QLineEdit()
        lineEdit.setValidator(QDoubleValidator(float(minValue), float(maxValue), 2))
        lineEdit.setPlaceholderText(label)
        lineEdit.setText(str(defaultValue))
        lineEdit.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        return self._addField(label, lineEdit, sectionTitle)

    def addIntInput(self, label: str, minValue=0, maxValue=999999999, sectionTitle: str | None = None, defaultValue: int = 0):
        lineEdit = QLineEdit()
        lineEdit.setValidator(QIntValidator(minValue, maxValue))
        lineEdit.setPlaceholderText(label)
        lineEdit.setText(str(defaultValue))
        lineEdit.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        return self._addField(label, lineEdit, sectionTitle)

    def addTextInput(self, label: str, placeholder: str = "", sectionTitle: str | None = None, defaultValue: str = ""):
        lineEdit = QLineEdit()
        lineEdit.setPlaceholderText(placeholder)
        lineEdit.setText(defaultValue)
        return self._addField(label, lineEdit, sectionTitle)

    def addComboBox(self, label: str, options: list[str], sectionTitle: str | None = None, defaultValue: str = ""):
        combo = QComboBox()
        combo.addItems(options)

        if defaultValue:
            combo.setCurrentText(defaultValue)
        
        combo.setPlaceholderText(label)
        return self._addField(label, combo, sectionTitle)

    def addMultiselectComboBox(self, label: str, options: list[str], sectionTitle: str | None = None, isVisible: bool = True):
        combo = MultiSelectComboBox()
        combo.addItems(options)
        return self._addField(label, combo, sectionTitle, isVisible)

    def addSpinBox(self, label: str, minValue=0, maxValue=100, sectionTitle: str | None = None, defaultValue: int = 0):
        spin = QSpinBox()
        spin.setRange(minValue, maxValue)
        spin.setValue(defaultValue)
        return self._addField(label, spin, sectionTitle)

    def addDateInput(self, label: str, defaultDate: QDate = QDate.currentDate(), sectionTitle: str | None = None, placeholder: str = ""):
        dateEdit = QDateEdit(defaultDate)
        dateEdit.setDisplayFormat("yyyy-MM-dd")
        dateEdit.setCalendarPopup(True)
        return self._addField(label, dateEdit, sectionTitle)

    def getFormData(self) -> dict:
        data = {}
        for label, (labelWidget, widget) in self.fields.items():
            if isinstance(widget, QLineEdit):
                data[label] = widget.text()
            elif isinstance(widget, MultiSelectComboBox):
                data[label] = widget.currentData()
            elif isinstance(widget, QComboBox):
                data[label] = widget.currentText()
            elif isinstance(widget, QSpinBox):
                data[label] = widget.value()
            elif isinstance(widget, QDateEdit):
                data[label] = widget.date()
        return data

    def onEditClicked(self):
        self.accept()

    def handleExitClicked(self):
        self.close()
    
    def setErrorMessage(self, message: str):
        self.messageLabel.setText(message)

    def clearMessage(self):
        self.messageLabel.setText("")