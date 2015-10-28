from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *

def render_output(output_filename, puzzle):
    app = QApplication([ '-platform', 'offscreen'])

    cell_size   = 50.0
    margin_size =  5.0
    thick_line  =  4.0
    thin_line   =  0.0

    colors = {
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

    for y in range(10):
        thickness = thick_line if y % 3 == 0 else thin_line
        painter.setPen(QPen(colors['line'], thickness))

        painter.drawLine(0,
                         cell_size * y,
                         cell_size * 9,
                         cell_size * y)

    for x in range(10):
        thickness = thick_line if x % 3 == 0 else thin_line
        painter.setPen(QPen(colors['line'], thickness))

        painter.drawLine(cell_size * x,
                         0,
                         cell_size * x,
                         cell_size * 9)

    for row in range(9):
        for column in range(9):
            painter.drawText(
                QRectF(cell_size * column,
                       cell_size * row,
                       cell_size,
                       cell_size),
                Qt.AlignCenter,
                str(puzzle[row, column]))

    painter.end()
