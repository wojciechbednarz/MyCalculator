import sys
import re
from Calculator.calc import Calculations
from functools import partial
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

ERROR_MSG = "ERROR"
ZERO_DIVISON_ERROR = "YOU CANNOT DIVIDE BY ZERO"
OVERFLOW_ERROR = "RESULT IS TOO LARGE TO BE REPRESENTED"
WINDOW_SIZE = 335
DISPLAY_HEIGHT = 55
BUTTON_SIZE = 40


class MyCalculatorWindow(QMainWindow):
    """MyCalculator main window."""

    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("MyCalculator")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()
        self._createMenu()
        # self._createLayout()

    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QGridLayout()
        keyBoard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "="]
        ]

        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                buttonsLayout.addWidget(self.buttonMap[key], row, col)

        self.generalLayout.addLayout(buttonsLayout)

    def _createMenu(self):
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close())

    def setDisplayText(self, text):
        """Set the display's text."""
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        """Get the display's text."""
        return self.display.text()

    def clearDisplay(self):
        """Clear the display."""
        self.setDisplayText("")

    # def _createLayout(self):
    #     layout = QGridLayout()
    #     layout.addWidget(QPushButton("1"), 2, 0)
    #     layout.addWidget(QPushButton("2"), 2, 1)
    #     layout.addWidget(QPushButton("3"), 2, 2)
    #     layout.addWidget(QPushButton("4"), 1, 0)
    #     layout.addWidget(QPushButton("5"), 1, 1)
    #     layout.addWidget(QPushButton("6"), 1, 2)
    #     layout.addWidget(QPushButton("7"), 0, 0)
    #     layout.addWidget(QPushButton("8"), 0, 1)
    #     layout.addWidget(QPushButton("9"), 0, 2)
    #     self.setLayout(layout)
    #     self.generalLayout.addLayout(layout)


def evaluateExpression(expression):
    """Evaluate an expression (Model)."""
    # calc = Calculations()
    # result = 0
    #
    # operator_plus = re.search(r"\+", expression)
    # operator_minus = re.search("-", expression)
    # operator_multiply = re.search(r"\*", expression)
    # operator_divide = re.search("/", expression)
    #
    # values = [x for x in expression if re.search(r"\d", x)]
    # try:
    #     for value in values:
    #         if operator_plus:
    #             result = calc.add(int(value))
    #         elif operator_multiply:
    #             result = calc.multiplication(int(value))
    #         elif operator_divide:
    #             result = calc.division(int(value))
    #     if operator_minus:
    #         result = calc.subtract(values)
    #
    #         # elif operator == "**":
    #         #     result = calc.power(value, value)
    # except ZeroDivisionError:
    #     result = "ZERO_DIVISON_ERROR"
    # except OverflowError:
    #     result = "OVERFLOW_ERROR"
    # return str(result)
    try:
        result = str(eval(expression, {}, {}))
    except ZeroDivisionError:
        result = "ZERO_DIVISON_ERROR"
    except OverflowError:
        result = "OVERFLOW_ERROR"
    return result

class MyCalculator:
    """MyCalculator's controller class."""

    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()

    def _calculateResult(self):
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, subExpression):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText() + subExpression
        self._view.setDisplayText(expression)

    def _connectSignalsAndSlots(self):
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {"=", "C"}:
                button.clicked.connect(
                    partial(self._buildExpression, keySymbol)
                )
        self._view.buttonMap["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)

def main():
    myCalculator = QApplication([])
    myCalaculatorWindow = MyCalculatorWindow()
    myCalaculatorWindow.show()
    MyCalculator(model=evaluateExpression, view=myCalaculatorWindow)
    sys.exit(myCalculator.exec())


if __name__ == "__main__":
    main()