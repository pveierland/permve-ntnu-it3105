#!/usr/bin/python3

import argparse
import numpy
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *

from vi.app.switchboard import Point, Problem
from vi.search import simulated_annealing

#def render_output(output_filename, N, M, K, solution):
#    app = QApplication([ '-platform', 'offscreen'])
#
#    cell_size     = 50
#    text_size     = 10
#    symbol_size   = 25
#    margin_size   = 5
#
#    colors = {
#        'egg':  QColor(175, 238, 238),
#        'line': QColor(51, 51, 51)
#    }
#
#    printer = QPrinter()
#    printer.setOutputFormat(QPrinter.PdfFormat)
#    printer.setOutputFileName(output_filename)
#    printer.setPageMargins(0, 0, 0, 0, QPrinter.Inch)
#    printer.setPageSize(QPageSize(
#        QSizeF(float(N * cell_size + 2 * margin_size) / printer.resolution(),
#               float(M * cell_size + 2 * margin_size) / printer.resolution()),
#        QPageSize.Inch))
#
#    painter = QPainter(printer)
#    painter.translate(margin_size, margin_size)
#    painter.setPen(QPen(colors['line'], 0))
#
#    for y in range(M + 1):
#        painter.drawLine(0,
#                         cell_size * y,
#                         cell_size * N,
#                         cell_size * y)
#
#    for x in range(N + 1):
#        painter.drawLine(cell_size * x,
#                         0,
#                         cell_size * x,
#                         cell_size * M)
#
#    painter.setBrush(QBrush(colors['egg']))
#
#    for row in range(M):
#        for column in range(N):
#            if solution[row, column]:
#                painter.drawEllipse(
#                    QPointF(cell_size * (column + 0.5),
#                            cell_size * (row + 0.5)),
#                    float(cell_size) / 4,
#                    float(cell_size) / 4)
#
#    painter.end()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('M', type=int)
    parser.add_argument('N', type=int)
    parser.add_argument('D', type=int)
    parser.add_argument('W', type=int)
    parser.add_argument('S_X', type=int)
    parser.add_argument('S_Y', type=int)
    parser.add_argument('E_X', type=int)
    parser.add_argument('E_Y', type=int)
    parser.add_argument('--max_epochs', type=int)
    parser.add_argument('--start_temperature', type=float)
    parser.add_argument('--delta_temperature', type=float)
    parser.add_argument('--pdf', metavar='output_filename')
    args = parser.parse_args()

    problem = Problem(args.M,
                      args.N,
                      args.D,
                      args.W,
                      Point(args.S_X, args.S_Y),
                      Point(args.E_X, args.E_Y))

    solution, epochs = simulated_annealing(
        problem, args.start_temperature, args.delta_temperature, args.max_epochs)

    print(solution.sum())

    #if args.pdf:
    #    render_output(args.pdf, N, M, K, solution)

if __name__ == '__main__':
    main()
