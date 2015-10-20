from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *

def render_output(output_filename, puzzle):
    app = QApplication([ '-platform', 'offscreen'])

    cell_size     = 50
    text_size     = 10
    symbol_size   = 25
    margin_size   = 5

    colors = {
        'egg':  QColor(175, 238, 238),
        'line': QColor(51, 51, 51)
    }

    printer = QPrinter()
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName(output_filename)
    printer.setPageMargins(0, 0, 0, 0, QPrinter.Inch)
    printer.setPageSize(QPageSize(
        QSizeF(float(9 * cell_size + 2 * margin_size) / printer.resolution(),
               float(9 * cell_size + 2 * margin_size) / printer.resolution()),
        QPageSize.Inch))

    painter = QPainter(printer)
    painter.translate(margin_size, margin_size)
    painter.setPen(QPen(colors['line'], 0))

    for y in range(10):
        painter.drawLine(0,
                         cell_size * 9,
                         cell_size * 9,
                         cell_size * y)

    for x in range(10):
        painter.drawLine(cell_size * x,
                         0,
                         cell_size * x,
                         cell_size * 9)

    painter.setBrush(QBrush(colors['egg']))

    painter.end()
