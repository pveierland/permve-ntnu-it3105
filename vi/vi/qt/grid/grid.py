from PyQt5.QtCore import *
from PyQt5.QtGui import *

import vi.grid

def build_cell_rect(grid, cell_size, coordinate):
    return QRectF(cell_size * coordinate.x,
                  cell_size * (grid.height - coordinate.y - 1),
                  cell_size,
                  cell_size)

def draw_cell(painter, color, grid, cell_size, coordinate):
    painter.fillRect(build_cell_rect(grid, cell_size, coordinate), color)

def draw_cell_text(painter, grid, cell_size, coordinate, text):
    painter.drawText(build_cell_rect(grid, cell_size, coordinate),
                     Qt.AlignCenter,
                     text)

def draw_grid(painter, colors, grid, cell_size):
    for y in range(grid.height):
        for x in range(grid.width):
            color = colors[grid.values[y][x]]
            draw_cell(painter, color, grid, cell_size, vi.grid.Coordinate(x, y))

def draw_grid_lines(painter, grid, cell_size):
    for y in range(grid.height + 1):
        painter.drawLine(0,
                         cell_size * (grid.height - y),
                         cell_size * grid.width,
                         cell_size * (grid.height - y))

    for x in range(grid.width + 1):
        painter.drawLine(cell_size * x,
                         0,
                         cell_size * x,
                         cell_size * grid.height)
