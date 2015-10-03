import os
import re
import sys
import time
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import vi.app.navigation
import vi.grid
import vi.search.graph
import vi.search.grid

class SearchProblemWidget(QWidget):
    def __init__(self,
                 parent=None,
                 search_state_listener=None,
                 play_state_listener=None):
        super(SearchProblemWidget, self).__init__(parent)

        self.search_state_listener = search_state_listener
        self.play_state_listener = play_state_listener

        self.setSizePolicy(QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.drawing_lock = threading.Lock()

        self.cell_size   = 42
        self.margin_size = 2

        self.play_thread = None
        self.is_playing  = False

        self.problem = None
        self.search  = None

        self.frequency = 1
        self.search_strategy = vi.search.graph.BestFirst.Strategy.astar

        self.cell_colors = {
            -1: QColor(51, 51, 51),
             1: QColor(255, 255, 255)
        }

        self.colors = {
            'start':                 QColor(0, 221, 0),
            'goal':                  QColor(238, 68, 0),
            'line':                  QColor(51, 51, 51),
            'expand_node_outline':   QColor(2, 120, 120),
            'generate_node_outline': QColor(243, 115, 56),
            'closed_node':           QColor(175, 238, 238),
            'open_node':             QColor(152, 251, 152),
            'solution_outline':      QColor(255, 255, 0)
        }

    def load(self, filename):
        with open(filename, 'r') as f:
            self.problem = vi.app.navigation.parse_grid_problem(f.read())
            self.search  = vi.search.graph.BestFirst(self.problem, self.search_strategy)

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
            painter.fillRect(size * coordinate.x,
                             size * (self.problem.grid.height - coordinate.y - 1),
                             size, size,
                             color)

        def draw_outline(coordinate, color):
            painter.save()
#            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setPen(QPen(QBrush(color), 5, Qt.SolidLine, Qt.SquareCap, Qt.BevelJoin))
            painter.drawRect(size * coordinate.x, size * (self.problem.grid.height - coordinate.y - 1),
                             size, size)
            painter.restore()

        def draw_text(coordinate, text):
            painter.drawText(QRectF(size * coordinate.x,
                             size * (self.problem.grid.height - coordinate.y - 1),
                             size, size),
                             Qt.AlignCenter,
                             text)

        if not self.problem:
            return

        with self.drawing_lock:
            size = self.cell_size

            painter = QPainter(self)
            painter.translate(self.margin_size, self.margin_size)

            painter.setPen(QPen(QBrush(self.colors['line']), size / 25))
            painter.setFont(QFont('Arial', 8))

            for y in range(self.problem.grid.height):
                for x in range(self.problem.grid.width):
                    cell_value = self.problem.grid.values[y][x]
                    draw_square(vi.grid.Coordinate(x, y), self.cell_colors[cell_value])

            draw_square(self.problem.start, self.colors['start'])
            draw_text(self.problem.start,   'START')
            draw_square(self.problem.goal,  self.colors['goal'])
            draw_text(self.problem.goal,    'GOAL')

            if self.search and self.search.state != vi.search.graph.State.start:
                for closed_node in self.search.closed_list():
                    draw_square(closed_node.state, self.colors['closed_node'])

                for open_node in self.search.open_list():
                    draw_square(open_node.state, self.colors['open_node'])

            if self.search and self.search.state == vi.search.graph.State.success:
                for action, state in self.search.info[1].path:
                    draw_square(state, self.colors['solution_outline'])

            if self.search and self.search.state != vi.search.graph.State.start:
                for closed_node in self.search.closed_list():
                    draw_text(closed_node.state, 'g={0}\nh={1:.1f}'.format(closed_node.path_cost, closed_node.heuristic_value))

                for open_node in self.search.open_list():
                    draw_text(open_node.state, 'g={0}\nh={1:.1f}'.format(open_node.path_cost, open_node.heuristic_value))

            for y in range(self.problem.grid.height + 1):
                painter.drawLine(0, size * (self.problem.grid.height - y), size * self.problem.grid.width, size * (self.problem.grid.height - y))

            for x in range(self.problem.grid.width + 1):
                painter.drawLine(size * x, 0, size * x, size * self.problem.grid.height)

            if self.search:
                if self.search.state == vi.search.graph.State.expand_node_begin or \
                   self.search.state == vi.search.graph.State.generate_nodes or \
                   self.search.state == vi.search.graph.State.expand_node_complete:
                    draw_outline(self.search.info[0].state, self.colors['expand_node_outline'])
                if self.search.state == vi.search.graph.State.generate_nodes:
                    draw_outline(self.search.info[1].state, self.colors['generate_node_outline'])

    def set_playing(self, state):
        self.is_playing = state
        if self.play_state_listener:
            self.play_state_listener(state)

    def set_frequency(self, frequency):
        self.frequency = frequency

    def set_search_strategy(self, is_set, strategy):
        if is_set:
            self.search_strategy = strategy

            if self.search:
                self.search.set_strategy(strategy)
                self.update()

    def sizeHint(self):
        if self.problem:
            offset = 2 * self.margin_size
            return QSize(offset + self.cell_size * self.problem.grid.width,
                         offset + self.cell_size * self.problem.grid.height)
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

class SearchApplication(QMainWindow):
    def __init__(self):
        super(SearchApplication, self).__init__()

        self.search_problem_widget = SearchProblemWidget(
            self, self.update_search_state, self.update_play_state)

        self.label_search_state = QLabel()
        self.label_search_nodes = QLabel()
        self.initialize_group_box_control()
        self.initialize_group_box_algorithm()

        top_layout = QVBoxLayout()
        top_layout.addWidget(self.group_box_algorithm)
        top_layout.addWidget(self.group_box_control)
        top_layout.addStretch(1)

        middle_layout = QHBoxLayout()
        middle_layout.addWidget(self.search_problem_widget)
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

        self.radio_button_astar.setChecked(True)
        self.slider_frequency.setValue(50)

        self.setWindowTitle('NTNU IT3105 2015 M1: Navigation -- permve@stud.ntnu.no')
        self.setCentralWidget(widget)
        self.show()

    def event(self, e):
        if e.type() == QEvent.LayoutRequest:
            self.setFixedSize(self.sizeHint())

        return super(SearchApplication, self).event(e)

    def initialize_group_box_algorithm(self):
        layout = QVBoxLayout()

        self.radio_button_bfs      = QRadioButton("BFS")
        self.radio_button_dfs      = QRadioButton("DFS")
        self.radio_button_dijkstra = QRadioButton("Dijkstra")
        self.radio_button_astar    = QRadioButton("A*")

        self.radio_button_bfs.toggled.connect(
            lambda is_set: self.search_problem_widget.set_search_strategy(
                is_set, vi.search.graph.BestFirst.Strategy.breadth_first))

        self.radio_button_dfs.toggled.connect(
            lambda is_set: self.search_problem_widget.set_search_strategy(
                is_set, vi.search.graph.BestFirst.Strategy.depth_first))

        self.radio_button_dijkstra.toggled.connect(
            lambda is_set: self.search_problem_widget.set_search_strategy(
                is_set, vi.search.graph.BestFirst.Strategy.dijkstra))

        self.radio_button_astar.toggled.connect(
            lambda is_set: self.search_problem_widget.set_search_strategy(
                is_set, vi.search.graph.BestFirst.Strategy.astar))

        self.button_group_algorithms = QButtonGroup()
        self.button_group_algorithms.addButton(self.radio_button_bfs)
        self.button_group_algorithms.addButton(self.radio_button_dfs)
        self.button_group_algorithms.addButton(self.radio_button_astar)
        self.button_group_algorithms.addButton(self.radio_button_dijkstra)

        layout = QVBoxLayout()
        layout.addWidget(self.radio_button_bfs)
        layout.addWidget(self.radio_button_dfs)
        layout.addWidget(self.radio_button_dijkstra)
        layout.addWidget(self.radio_button_astar)

        self.group_box_algorithm = QGroupBox("Algorithm")
        self.group_box_algorithm.setLayout(layout)

    def initialize_group_box_control(self):
        self.combo_box_file_selector = QComboBox()
        self.combo_box_file_selector.activated[str].connect(self.search_problem_widget.load)
        self.combo_box_file_selector_load_values()

        self.slider_frequency = QSlider(Qt.Horizontal)
        self.slider_frequency.setRange(5, 500)
        self.slider_frequency.setTracking(True)
        self.slider_frequency.valueChanged.connect(self.handle_set_frequency)

        self.label_frequency = QLabel()

        layout_slider = QHBoxLayout()
        layout_slider.addWidget(self.slider_frequency)
        layout_slider.addWidget(self.label_frequency)

        self.button_step  = QPushButton("Step")
        self.button_step.clicked.connect(self.search_problem_widget.step)

        self.button_play  = QPushButton("Play")
        self.button_play.clicked.connect(self.search_problem_widget.toggle_play)

        self.button_solve = QPushButton("Solve")
        self.button_solve.clicked.connect(self.search_problem_widget.solve)

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
        self.search_problem_widget.stop()

    def combo_box_file_selector_load_values(self):
        for f in sorted(filter(os.path.isfile, os.listdir('.'))):
            if f.endswith('.txt'):
                self.combo_box_file_selector.addItem(f)

    def handle_set_frequency(self, value):
        frequency = value / 10.0
        self.label_frequency.setText("{0:.1f} Hz".format(frequency))
        self.search_problem_widget.set_frequency(frequency)

    def update_play_state(self, is_playing):
        self.button_play.setText("Play" if not is_playing else "Stop")

    def update_search_state(self, search):
        open_node_count   = sum(1 for _ in search.open_list())
        closed_node_count = sum(1 for _ in search.closed_list())
        total_node_count  = open_node_count + closed_node_count

        self.label_search_nodes.setText(
            "Open nodes: {0}\tClosed nodes: {1}\t Total nodes: {2}".format(
                open_node_count, closed_node_count, total_node_count))

        if search.state == vi.search.graph.State.start:
            self.label_search_state.setText(
                "Starting search node has state ({0},{1}).".format(
                    search.info[0].state.x, search.info[0].state.y))
        elif search.state == vi.search.graph.State.success:
            self.label_search_state.setText(
                "Success! Solution path to goal state ({0},{1}) with cost {2} was found.".format(
                    search.info[0].state.x, search.info[0].state.y,
                    search.info[1].cost))
        elif search.state == vi.search.graph.State.failed:
            self.label_search_state.setText(
                "Failure! No solution could be found.")
        elif search.state == vi.search.graph.State.expand_node_begin:
            self.label_search_state.setText(
                "Expanding node with state ({0},{1}).".format(
                    search.info[0].state.x, search.info[0].state.y))
        elif search.state == vi.search.graph.State.generate_nodes:
            node, successor, is_unique = search.info
            self.label_search_state.setText(
                "Generated {0} successor state ({1},{2}) from node with state ({3},{4}).".format(
                    "unique" if is_unique else "existing",
                    successor.state.x, successor.state.y,
                    node.state.x, node.state.y))
        elif search.state == vi.search.graph.State.expand_node_complete:
            self.label_search_state.setText(
                "Expansion of node with state ({0},{1}) completed.".format(
                    search.info[0].state.x, search.info[0].state.y))

def main():
    app = QApplication(sys.argv)
    search_application = SearchApplication()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
