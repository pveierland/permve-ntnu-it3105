import os
import sys
import time
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import vi.graph
import vi.app.astar_gac_vertex_coloring

class VertexColoringWidget(QWidget):
    def __init__(self,
                 parent=None,
                 algorithm_state_listener=None,
                 play_state_listener=None):
        super(VertexColoringWidget, self).__init__(parent)

        self.algorithm_state_listener = algorithm_state_listener
        self.play_state_listener = play_state_listener

        self.setSizePolicy(QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.play_thread = None
        self.is_playing  = False

        self.search  = None

        self.graph = None

        self.vertex_radii = 3.0

        self.frequency = 1

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
            self.graph = vi.app.astar_gac_vertex_coloring.parse_graph_file(f.readlines())

            self.min_x = min(v.value[1][0] for v in self.graph.vertices)
            self.max_x = max(v.value[1][0] for v in self.graph.vertices)
            self.min_y = min(v.value[1][1] for v in self.graph.vertices)
            self.max_y = max(v.value[1][1] for v in self.graph.vertices)

            self.diff_x = self.max_x - self.min_x
            self.diff_y = self.max_y - self.min_y

            self.updateGeometry()
            self.update()

    def play(self):
        while self.is_playing and not self.search.is_complete():
            self.step()
            time.sleep(1 / self.frequency)
        self.set_playing(False)

    def step(self):
        pass #TODO
        #if self.search and \
        #   self.search.state[0] != vi.search.graph.State.success and \
        #   self.search.state[0] != vi.search.graph.State.failed:
        #    self.search.step()
        #    if self.search_state_listener:
        #        self.search_state_listener(self.search.state)
        #    self.update()

    def paintEvent(self, event):
        if self.graph:
            size = self.size()
        
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            
            painter.setBrush(QBrush(Qt.white))
            painter.drawRect(event.rect())

            painter.setPen(QPen(Qt.red, 0))
            painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))

            s_x = 0.9 * size.width() / self.diff_x
            s_y = 0.9 * size.height() / self.diff_y

            painter.translate(size.width() * 0.05, size.height() * 0.05)
            painter.scale(s_x, s_y)
            painter.translate(0.0, self.diff_y)
            painter.scale(1.0, -1.0)
            painter.translate(-self.min_x, -self.min_y)

            for edge in self.graph.edges:
                painter.drawLine(
                    QPointF(edge.a.value[1][0], edge.a.value[1][1]),
                    QPointF(edge.b.value[1][0], edge.b.value[1][1]))

            for vertex in self.graph.vertices:
                painter.drawEllipse(
                    QPointF(vertex.value[1][0], vertex.value[1][1]),
                    self.vertex_radii / s_x, self.vertex_radii / s_y)

        #def draw_text(coordinate, text):
        #    painter.drawText(QRectF(size * coordinate.x,
        #                     size * (self.problem.grid.height - coordinate.y - 1),
        #                     size, size),
        #                     Qt.AlignCenter,
        #                     text)

        #if not self.problem:
        #    return

        #size = self.cell_size

        #painter = QPainter(self)
        #painter.translate(self.margin_size, self.margin_size)

        #painter.setPen(QPen(QBrush(self.colors['line']), size / 25))
        #painter.setFont(QFont('Arial', 8))

        #for y in range(self.problem.grid.height):
        #    for x in range(self.problem.grid.width):
        #        cell_value = self.problem.grid.values[y][x]
        #        draw_square(vi.grid.Coordinate(x, y), self.cell_colors[cell_value])

        #draw_square(self.problem.start, self.colors['start'])
        #draw_text(self.problem.start,   'START')
        #draw_square(self.problem.goal,  self.colors['goal'])
        #draw_text(self.problem.goal,    'GOAL')

        #if self.search and self.search.state[0] != vi.search.graph.State.start:
        #    for closed_node in self.search.closed_list():
        #        draw_square(closed_node.state, self.colors['closed_node'])

        #    for open_node in self.search.open_list():
        #        draw_square(open_node.state, self.colors['open_node'])

        #if self.search and self.search.state[0] == vi.search.graph.State.success:
        #    for action, state in self.search.state[2].path:
        #        draw_square(state, self.colors['solution_outline'])

        #if self.search and self.search.state[0] != vi.search.graph.State.start:
        #    for closed_node in self.search.closed_list():
        #        draw_text(closed_node.state, 'g={0}\nh={1:.1f}'.format(closed_node.path_cost, closed_node.heuristic_value))

        #    for open_node in self.search.open_list():
        #        draw_text(open_node.state, 'g={0}\nh={1:.1f}'.format(open_node.path_cost, open_node.heuristic_value))

        #for y in range(self.problem.grid.height + 1):
        #    painter.drawLine(0, size * (self.problem.grid.height - y), size * self.problem.grid.width, size * (self.problem.grid.height - y))

        #for x in range(self.problem.grid.width + 1):
        #    painter.drawLine(size * x, 0, size * x, size * self.problem.grid.height)

        #if self.search:
        #    if self.search.state[0] == vi.search.graph.State.expand_node_begin or \
        #       self.search.state[0] == vi.search.graph.State.generate_nodes or \
        #       self.search.state[0] == vi.search.graph.State.expand_node_complete:
        #        draw_outline(self.search.state[1].state, self.colors['expand_node_outline'])
        #    if self.search.state[0] == vi.search.graph.State.generate_nodes:
        #        draw_outline(self.search.state[2].state, self.colors['generate_node_outline'])

    def set_playing(self, state):
        self.is_playing = state
        if self.play_state_listener:
            self.play_state_listener(state)

    def set_frequency(self, frequency):
        self.frequency = frequency

    def sizeHint(self):
        return QSize(750, 750) if self.graph else QSize(0, 0)

    def solve(self):
        pass

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

class VertexColoringApplication(QMainWindow):
    def __init__(self):
        super(VertexColoringApplication, self).__init__()

        self.vertex_coloring_widget = VertexColoringWidget(
            self, self.update_algorithm_state, self.update_play_state)

        self.label_algorithm_state = QLabel()
        self.initialize_group_box_control()

        top_layout = QVBoxLayout()
        top_layout.addWidget(self.group_box_control)
        top_layout.addStretch(1)

        middle_layout = QHBoxLayout()
        middle_layout.addWidget(self.vertex_coloring_widget)
        middle_layout.addLayout(top_layout)

        layout = QVBoxLayout()
        layout.addLayout(middle_layout)
        layout.addWidget(self.label_algorithm_state)

        widget = QWidget()
        sizePolicy = QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)
        widget.setSizePolicy(sizePolicy)
        widget.setLayout(layout)

        self.setSizePolicy(sizePolicy)

        self.slider_frequency.setValue(50)

        self.setWindowTitle('NTNU IT3105 2015 M2: Vertex Coloring -- permve@stud.ntnu.no')
        self.setCentralWidget(widget)
        self.show()

    def event(self, e):
        if e.type() == QEvent.LayoutRequest:
            self.setFixedSize(self.sizeHint())

        return super(VertexColoringApplication, self).event(e)

    def initialize_group_box_control(self):
        self.combo_box_file_selector = QComboBox()
        self.combo_box_file_selector.activated[str].connect(self.vertex_coloring_widget.load)
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
        self.button_play  = QPushButton("Play")
        self.button_solve = QPushButton("Solve")

        self.button_step.clicked.connect(self.vertex_coloring_widget.step)
        self.button_play.clicked.connect(self.vertex_coloring_widget.toggle_play)
        self.button_solve.clicked.connect(self.vertex_coloring_widget.solve)

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

    def combo_box_file_selector_load_values(self):
        for f in sorted(filter(os.path.isfile, os.listdir('.'))):
            if f.endswith('.txt'):
                self.combo_box_file_selector.addItem(f)

    def handle_set_frequency(self, value):
        frequency = value / 10.0
        self.label_frequency.setText("{0:.1f} Hz".format(frequency))
        self.vertex_coloring_widget.set_frequency(frequency)

    def update_algorithm_state(self, state):
        pass

    def update_play_state(self, is_playing):
        self.button_play.setText("Play" if not is_playing else "Stop")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    search_application = VertexColoringApplication()
    sys.exit(app.exec_())
