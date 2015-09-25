import os
import re
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import vi.grid
import vi.search.graph
import vi.search.grid

class SearchProblemWidget(QWidget):
    def __init__(self, parent=None):
        super(SearchProblemWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed))

        # Use for calculating default size
        self.grid_size   = (5, 5)

        self.cell_size   = 45
        self.margin_size = 10

        self.problem = None
        self.search  = None

        self.cell_colors = {
            -1: QColor(51, 51, 51),
             1: QColor(255, 255, 255)
        }

        self.colors = {
            'start':                 QColor(0, 221, 0),
            'goal':                  QColor(238, 68, 0),
            'line':                  QColor(51, 51, 51),
            'expand_node_outline':   QColor(255, 0, 255),
            'generate_node_outline': QColor(0, 255, 0),
            'closed_node':           QColor(175, 238, 238),
            'open_node':             QColor(152, 251, 152)
        }

    def load(self, filename):
        with open(filename, 'r') as f:
            parts = filter(None, re.split('[()]+\\s*[()]*', f.read()))

            dimensions = vi.grid.Coordinate.from_string(parts[0])
            start      = vi.grid.Coordinate.from_string(parts[1])
            goal       = vi.grid.Coordinate.from_string(parts[2])
            obstacles  = [vi.grid.Rectangle.from_string(p) for p in parts[3:]]

            grid = vi.grid.Grid(width=dimensions.x, height=dimensions.y)

            for obstacle in obstacles:
                for y in range(obstacle.y, obstacle.y + obstacle.height):
                    for x in range(obstacle.x, obstacle.x + obstacle.width):
                        grid.values[y][x] = vi.grid.obstructed

            self.problem = vi.search.grid.Problem(grid, start, goal)
            self.grid_size = (self.problem.grid.width, self.problem.grid.height)

            self.search = vi.search.graph.AStar(self.problem)

            self.updateGeometry()
            self.update()

    def step(self):
        if self.search:
            self.search.step()
            self.update()

    def paintEvent(self, event):
        def draw_square(x, y, color):
            painter.fillRect(size * x, size * (self.problem.grid.height - y - 1),
                             size, size,
                             color)

        def draw_outline(x, y, color):
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing, True);
            painter.setPen(QPen(QBrush(color), 7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawRect(size * x, size * (self.problem.grid.height - y - 1),
                             size, size)
            painter.restore()

        def draw_text(x, y, text):
            painter.drawText(QRectF(size * x, size * (self.problem.grid.height - y - 1), size, size),
                             Qt.AlignCenter,
                             text)

        if not self.problem:
            return

        #size = self.size().width() / self.problem.grid.width

        size = self.cell_size

        painter = QPainter(self)
        painter.translate(self.margin_size, self.margin_size)

        painter.setPen(QPen(QBrush(self.colors['line']), size / 25))
        painter.setFont(QFont('Arial', 8))

        for y in range(self.problem.grid.height):
            for x in range(self.problem.grid.width):
                cell_value = self.problem.grid.values[y][x]
                draw_square(x, y, self.cell_colors[cell_value])

        draw_square(self.problem.start.x, self.problem.start.y, self.colors['start'])
        draw_text(self.problem.start.x,   self.problem.start.y, 'S')
        draw_square(self.problem.goal.x,  self.problem.goal.y,  self.colors['goal'])
        draw_text(self.problem.goal.x,    self.problem.goal.y,  'G')

        if self.search:
            for closed_state, closed_node in self.search.closed_hash_table.iteritems():
                draw_square(closed_state.x, closed_state.y, self.colors['closed_node'])
                draw_text(closed_state.x, closed_state.y, 'g={0}\nh={1:.1f}'.format(closed_node.path_cost, closed_node.heuristic_value))

            for open_state, open_node in self.search.open_hash_table.iteritems():
                draw_square(open_state.x, open_state.y, self.colors['open_node'])
                draw_text(open_state.x, open_state.y, 'g={0}\nh={1:.1f}'.format(open_node.path_cost, open_node.heuristic_value))
        
        for y in range(self.problem.grid.height + 1):
            painter.drawLine(0, size * (self.problem.grid.height - y), size * self.problem.grid.width, size * (self.problem.grid.height - y))

        for x in range(self.problem.grid.width + 1):
            painter.drawLine(size * x, 0, size * x, size * self.problem.grid.height)

        if self.search:
            if self.search.state[0] == vi.search.graph.State.expand_node_begin or \
               self.search.state[0] == vi.search.graph.State.generate_nodes or \
               self.search.state[0] == vi.search.graph.State.expand_node_complete:
                draw_outline(self.search.state[1].state.x, self.search.state[1].state.y, self.colors['expand_node_outline'])
            if self.search.state[0] == vi.search.graph.State.generate_nodes:
                draw_outline(self.search.state[2].state.x, self.search.state[2].state.y, self.colors['generate_node_outline'])


    def sizeHint(self):
        return QSize(2 * self.margin_size + self.cell_size * self.grid_size[0],
                     2 * self.margin_size + self.cell_size * self.grid_size[1])

class SearchApplication(QMainWindow):
    def __init__(self):
        super(SearchApplication, self).__init__()

        self.combo_box_file_selector = QComboBox()
        self.combo_box_file_selector.activated[str].connect(self.handle_string)
        self.combo_box_file_selector_load_values()

        self.search_problem_widget = SearchProblemWidget(self)

        layout = QVBoxLayout()
        layout.addWidget(self.combo_box_file_selector)
        layout.addWidget(self.search_problem_widget)
        layout.setSizeConstraint(QLayout.SetFixedSize);

        widget = QWidget()
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)
        widget.setSizePolicy(sizePolicy)
        widget.setLayout(layout)

        self.setSizePolicy(sizePolicy)

        self.setWindowTitle('VI Search Algorithms')
        self.setCentralWidget(widget)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Right:
            self.search_problem_widget.step()

    def combo_box_file_selector_load_values(self):
        for f in sorted(filter(os.path.isfile, os.listdir('.'))):
            if f.endswith('.txt'):
                self.combo_box_file_selector.addItem(f)

    def handle_string(self, text):
        self.search_problem_widget.load(text)

def main():
    app = QApplication(sys.argv)
    search_application = SearchApplication()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
