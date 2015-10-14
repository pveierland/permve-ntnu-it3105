#!/usr/bin/python3

import argparse
import numpy
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *

from vi.app.egg_carton import Problem
from vi.search import simulated_annealing
import vi.qt.grid

def render_output(args, solution):
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
    printer.setOutputFileName(args.pdf)
    printer.setPageMargins(0, 0, 0, 0, QPrinter.Inch)
    printer.setPageSize(QPageSize(
        QSizeF(float(args.N * cell_size + 2 * margin_size) / printer.resolution(),
               float(args.M * cell_size + 2 * margin_size) / printer.resolution()),
        QPageSize.Inch))

    painter = QPainter(printer)
    painter.translate(margin_size, margin_size)
    painter.setPen(QPen(colors['line'], 0))

    for y in range(args.M + 1):
        painter.drawLine(0,
                         cell_size * y,
                         cell_size * args.N,
                         cell_size * y)

    for x in range(args.N + 1):
        painter.drawLine(cell_size * x,
                         0,
                         cell_size * x,
                         cell_size * args.M)

    painter.setBrush(QBrush(colors['egg']))

    for row in range(args.M):
        for column in range(args.N):
            if solution[row, column]:
                painter.drawEllipse(
                    QPointF(cell_size * (column + 0.5),
                            cell_size * (row + 0.5)),
                    float(cell_size) / 4,
                    float(cell_size) / 4)

    painter.end()

parser = argparse.ArgumentParser()
parser.add_argument('M', type=int)
parser.add_argument('N', type=int)
parser.add_argument('K', type=int)
parser.add_argument('--max_epochs', type=int)
parser.add_argument('--pdf', metavar='output_filename')
args = parser.parse_args()

problem = Problem(args.M, args.N, args.K)
solution, epochs = simulated_annealing(problem, None, args.max_epochs)

print(solution.sum())

if args.pdf:
    render_output(args, solution)
