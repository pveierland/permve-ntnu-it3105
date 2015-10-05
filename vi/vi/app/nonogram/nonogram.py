import os
import sys
import time
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import vi.grid
import vi.search.graph
import vi.search.grid

class NonogramWidget(QWidget):
    def __init__(self,
                 parent=None,
                 search_state_listener=None,
                 play_state_listener=None):
        super(NonogramWidget, self).__init__(parent)

        self.search_state_listener = search_state_listener
        self.play_state_listener = play_state_listener

        self.setSizePolicy(QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.drawing_lock = threading.Lock()

        self.cell_size   = 20
        self.margin_size = 2
        self.frequency   = 1

        self.play_thread = None
        self.is_playing  = False

        self.dimensions = None
        self.problem    = None
        self.search     = None

        self.colors = {
            'start':                 QColor(0, 221, 0),
            'goal':                  QColor(238, 68, 0),
            'line':                  QColor(51, 51, 51),
            'expand_node_outline':   QColor(2, 120, 120),
            'generate_node_outline': QColor(243, 115, 56),
            'solution_outline':      QColor(255, 255, 0),
            'bad_times':             QColor(248, 14, 39),
            'filled':                QColor(51, 51, 51),
            'unfilled':              QColor(255, 255, 255)
        }

    def load(self, filename):
        with open(filename, 'r') as f:
            self.problem, self.dimensions = vi.app.nonogram.build_problem(f.read())
            self.search  = vi.search.graph.BestFirst(
                self.problem, vi.search.graph.BestFirst.Strategy.astar)

            if self.search_state_listener:
                self.search_state_listener(self.search)

            self.updateGeometry()
            self.update()

    def play(self):
        while self.is_playing and not self.search.is_complete():
            self.step()
            time.sleep(1 / self.frequency)

        self.set_playing(False)

    def step(self):
        if self.search and not self.search.is_complete():

            with self.drawing_lock:
                self.search.step()

            if self.search_state_listener:
                self.search_state_listener(self.search)

            self.update()

    def paintEvent(self, event):
        def draw_square(coordinate, color):
            painter.fillRect(self.cell_size * coordinate.x,
                             self.cell_size * (self.dimensions[1] - coordinate.y - 1),
                             self.cell_size, self.cell_size,
                             color)

        def draw_outline(variable_identity, color):
            painter.save()
            painter.setPen(QPen(QBrush(color), 5, Qt.SolidLine, Qt.SquareCap, Qt.BevelJoin))

            if variable_identity[0] is vi.app.nonogram.Dimension.column:
                # Drawing column outline
                painter.drawRect(self.cell_size * variable_identity[1], 0,
                                 self.cell_size, self.cell_size * self.dimensions[1])
            else:
                # Drawing row outline
                painter.drawRect(0, self.cell_size * (self.dimensions[1] - variable_identity[1] - 1),
                                 self.cell_size * self.dimensions[0], self.cell_size)

            painter.restore()

        if not self.search:
            return

        with self.drawing_lock:
            size = self.size()

            painter = QPainter(self)
            painter.setPen(QPen(QBrush(self.colors['line']), 0))
            painter.drawRect(0, 0, size.width() - 1, size.height() - 1)

            painter.translate(self.margin_size, self.margin_size)
            painter.setPen(QPen(QBrush(self.colors['line']), self.cell_size / 25))
            painter.setFont(QFont('Arial', 8))

            domains = self.search.node.state.domains

            for row in range(self.dimensions[1]):
                row_domain = domains[(vi.app.nonogram.Dimension.row, row)]

                for column in range(self.dimensions[0]):
                    row_agree = all(value & (1 << self.dimensions[0] - column - 1) != 0
                                     for value in row_domain) or \
                                 not any(value & (1 << self.dimensions[0] - column - 1) != 0 \
                                     for value in row_domain)

                    row_value = (row_domain[0] & (1 << self.dimensions[0] - column - 1)) != 0

                    column_domain = domains[(vi.app.nonogram.Dimension.column, column)]

                    column_agree = all(value & (1 << row) != 0
                                     for value in column_domain) or \
                                 not any(value & (1 << row) != 0 \
                                     for value in column_domain)

                    column_value = (column_domain[0] & (1 << row)) != 0

                    agree = row_agree and column_agree and (row_value == column_value)
                    value = row_value and column_value

                    if agree:
                        if value:
                            draw_square(vi.grid.Coordinate(column, row), self.colors['filled'])
                        else:
                            draw_square(vi.grid.Coordinate(column, row), self.colors['unfilled'])
                    else:
                        draw_square(vi.grid.Coordinate(column, row), self.colors['bad_times'])

            if self.search.state == vi.search.graph.State.expand_node_begin or \
               self.search.state == vi.search.graph.State.generate_nodes or \
               self.search.state == vi.search.graph.State.expand_node_complete:
                action = self.search.info[0].action
                if action:
                    draw_outline(action[0].identity, self.colors['expand_node_outline'])
            if self.search.state == vi.search.graph.State.generate_nodes:
                action = self.search.info[1].action
                draw_outline(action[0].identity, self.colors['generate_node_outline'])

    def set_playing(self, state):
        self.is_playing = state
        if self.play_state_listener:
            self.play_state_listener(state)

    def set_frequency(self, frequency):
        self.frequency = frequency

    def sizeHint(self):
        if self.problem:
            offset = 2 * self.margin_size
            return QSize(offset + self.cell_size * self.dimensions[0],
                         offset + self.cell_size * self.dimensions[1])
        else:
            return QSize(0, 0)

    def solve(self):
        self.stop()

        if self.search:
            with self.drawing_lock:
                while not self.search.is_complete():
                    self.search.step()

            if self.search_state_listener:
                self.search_state_listener(self.search)

            self.update()

    def stop(self):
        self.set_playing(False)
        if self.play_thread:
            self.play_thread.join()

    def toggle_play(self):
        if not self.is_playing:
            self.set_playing(True)
            self.play_thread = threading.Thread(target=self.play)
            self.play_thread.start()
        else:
            self.set_playing(False)

class NonogramApplication(QMainWindow):
    def __init__(self):
        super(NonogramApplication, self).__init__()

        self.nonogram_widget = NonogramWidget(
            self, self.update_search_state, self.update_play_state)

        self.label_search_state = QLabel()
        self.label_search_nodes = QLabel()

        self.label_search_state.setWordWrap(True)
        self.label_search_nodes.setWordWrap(True)

        self.initialize_group_box_control()

        top_layout = QVBoxLayout()
        top_layout.addWidget(self.group_box_control)
        top_layout.addStretch(1)

        middle_layout = QHBoxLayout()
        middle_layout.addWidget(self.nonogram_widget)
        middle_layout.addLayout(top_layout)

        layout = QVBoxLayout()
        layout.addLayout(middle_layout)
        layout.addWidget(self.label_search_state)
        layout.addWidget(self.label_search_nodes)

        widget = QWidget()
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)
        widget.setSizePolicy(sizePolicy)
        widget.setLayout(layout)

        self.setSizePolicy(sizePolicy)

        self.slider_frequency.setValue(50)

        self.setWindowTitle('NTNU IT3105 2015 M3: Nonogram Solver -- permve@stud.ntnu.no')
        self.setCentralWidget(widget)
        self.show()

    def event(self, e):
        if e.type() == QEvent.LayoutRequest:
            self.setFixedSize(self.sizeHint())

        return super(NonogramApplication, self).event(e)

    def initialize_group_box_control(self):
        self.combo_box_file_selector = QComboBox()
        self.combo_box_file_selector.activated[str].connect(self.nonogram_widget.load)
        self.combo_box_file_selector_load_values()

        self.slider_frequency = QSlider(Qt.Horizontal)
        self.slider_frequency.setRange(1, 100)
        self.slider_frequency.setTracking(True)
        self.slider_frequency.valueChanged.connect(self.handle_set_frequency)

        self.label_frequency = QLabel()

        layout_slider = QHBoxLayout()
        layout_slider.addWidget(self.slider_frequency)
        layout_slider.addWidget(self.label_frequency)

        self.button_step  = QPushButton("Step")
        self.button_step.clicked.connect(self.nonogram_widget.step)

        self.button_play  = QPushButton("Play")
        self.button_play.clicked.connect(self.nonogram_widget.toggle_play)

        self.button_solve = QPushButton("Solve")
        self.button_solve.clicked.connect(self.nonogram_widget.solve)

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.button_step)
        layout_buttons.addWidget(self.button_play)
        layout_buttons.addWidget(self.button_solve)

        layout = QVBoxLayout()
        layout.addWidget(self.combo_box_file_selector)
        layout.addLayout(layout_slider)
        layout.addLayout(layout_buttons)

        self.group_box_control = QGroupBox("Control")
        self.group_box_control.setLayout(layout)

    def closeEvent(self, e):
        self.nonogram_widget.stop()

    def combo_box_file_selector_load_values(self):
        for f in sorted(filter(os.path.isfile, os.listdir('.'))):
            if f.endswith('.txt'):
                self.combo_box_file_selector.addItem(f)

    def handle_set_frequency(self, frequency):
        self.label_frequency.setText("{0} Hz".format(frequency))
        self.nonogram_widget.set_frequency(frequency)

    def update_play_state(self, is_playing):
        self.button_play.setText("Play" if not is_playing else "Stop")

    def update_search_state(self, search):
        def format_node(n):
            if not n.action:
                return "NO ASSUMPTIONS"
            else:
                variable_identity = n.action[0].identity
                assumed_value     = n.action[1]
                is_column         = variable_identity[0] is vi.app.nonogram.Dimension.column
                index             = variable_identity[1]
                dimension         = self.nonogram_widget.dimensions[1] if is_column else \
                                    self.nonogram_widget.dimensions[0]

                return "ASSUMPTION {0}{1} is {2}".format(
                    'Column' if is_column else 'Row',
                    index,
                    '{0:b}'.format(assumed_value).zfill(dimension))

        open_node_count   = sum(1 for _ in search.open_list())
        closed_node_count = sum(1 for _ in search.closed_list())
        total_node_count  = open_node_count + closed_node_count

        self.label_search_nodes.setText(
            "Open nodes: {0}\tClosed nodes: {1}\t Total nodes: {2}".format(
                open_node_count, closed_node_count, total_node_count))

        if search.state == vi.search.graph.State.start:
            self.label_search_state.setText(
                "Starting search node has {0}.".format(
                    format_node(search.info[0])))
        elif search.state == vi.search.graph.State.success:
            self.label_search_state.setText(
                "Success! Solution path with path cost {0} was found.".format(
                    search.info[1].cost))
        elif search.state == vi.search.graph.State.failed:
            self.label_search_state.setText(
                "Failure! No solution could be found.")
        elif search.state == vi.search.graph.State.expand_node_begin:
            self.label_search_state.setText(
                "Expanding node with {0}.".format(
                    format_node(search.info[0])))
        elif search.state == vi.search.graph.State.generate_nodes:
            node, successor, is_unique = search.info
            self.label_search_state.setText(
                "Generated {0} successor with {1} from node with {2}.".format(
                    "unique" if is_unique else "existing",
                    format_node(successor),
                    format_node(node)))
        elif search.state == vi.search.graph.State.expand_node_complete:
            self.label_search_state.setText(
                "Expansion of node with {0} completed.".format(
                    format_node(search.info[0])))

def main():
    app = QApplication(sys.argv)
    search_application = NonogramApplication()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
