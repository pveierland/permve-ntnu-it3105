import os
import re
import sys
import time
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import vi.app.astar_gac_vertex_coloring
import vi.csp
import vi.graph
import vi.search.graph
import vi.search.gac

class VertexColoringWidget(QWidget):
    def __init__(self,
                 parent=None,
                 search_state_listener=None,
                 play_state_listener=None,
                 k_state_listener=None):

        super(VertexColoringWidget, self).__init__(parent)

        self.search_state_listener = search_state_listener
        self.play_state_listener   = play_state_listener
        self.k_state_listener      = k_state_listener

        self.setSizePolicy(QSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.play_thread = None
        self.is_playing  = False

        self.search  = None
        self.graph = None

        self.vertex_radii = 3.0
        self.frequency    = 1
        self.k            = 4

        self.drawing_lock = threading.Lock()

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
            'solution_outline':      QColor(255, 255, 0),
            1:                       QColor(246, 64, 174),  # pink
            2:                       QColor(248, 14, 39),   # red
            3:                       QColor(248, 152, 31),  # orange
            4:                       QColor(138, 215, 73),  # green
            5:                       QColor(13, 159, 216),  # blue
            6:                       QColor(133, 105, 207), # purple
            7:                       QColor(244, 244, 0),   # yellow
            8:                       QColor(255, 255, 255), # white
            9:                       QColor(0, 0, 0),       # black
            'uncolored':             QColor(120, 118, 121)  # dark grey
        }

        self.color_to_text = {
            1: "PINK",
            2: "RED",
            3: "ORANGE",
            4: "GREEN",
            5: "BLUE",
            6: "PURPLE",
            7: "YELLOW",
            8: "WHITE",
            9: "BLACK"
        }

    def __init_problem(self, k=None):
        if self.filename:
            self.problem, self.k, self.boundaries = \
                vi.app.astar_gac_vertex_coloring.build_vertex_coloring_problem_from_file(
                    self.filename, k)

    def __init_search(self):
        self.search = vi.search.graph.AStar(self.problem)

        if self.search_state_listener:
            self.search_state_listener(self.search)

        if self.k_state_listener:
            self.k_state_listener(self.k)

        self.updateGeometry()
        self.update()

    def load(self, filename):
        self.filename = filename
        self.__init_problem()
        self.__init_search()

    def paintEvent(self, event):
        if self.search:
            with self.drawing_lock:
                painter = QPainter(self)
                painter.setRenderHint(QPainter.Antialiasing, True)

                painter.setBrush(QBrush(Qt.white))
                painter.drawRect(event.rect())

                painter.setPen(QPen(Qt.black, 0))
                painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))

                size = self.size()
                s_x = 0.9 * size.width() / self.boundaries.diff.x
                s_y = 0.9 * size.height() / self.boundaries.diff.y

                painter.translate(size.width() * 0.05, size.height() * 0.05)
                painter.scale(s_x, s_y)
                painter.translate(0.0, self.boundaries.diff.y)
                painter.scale(1.0, -1.0)
                painter.translate(-self.boundaries.min.x, -self.boundaries.min.y)

                network = self.search.node.state

                for constraint in network.constraints:
                    vertex_a = constraint.variables[0].identity.value
                    vertex_b = constraint.variables[1].identity.value

                    painter.drawLine(QPointF(vertex_a.x, vertex_a.y),
                                     QPointF(vertex_b.x, vertex_b.y))

                # Sort vertices before drawing for prettiness:
                for variable, domain in sorted(network.domains.items(), key=lambda x: x[0].identity):
                    vertex = variable.identity

                    has_color = len(domain) == 1

                    color = self.colors[domain[0] if has_color else 'uncolored']
                    radii = self.vertex_radii * 2 if has_color else self.vertex_radii

                    painter.setBrush(QBrush(color))

                    painter.drawEllipse(QPointF(vertex.value.x, vertex.value.y),
                                        radii / s_x,
                                        radii / s_y)

    def play(self):
        while self.is_playing and not self.search.is_complete():
            self.step()
            time.sleep(1 / self.frequency)
        self.set_playing(False)

    def set_frequency(self, frequency):
        self.frequency = frequency

    def set_playing(self, state):
        self.is_playing = state
        if self.play_state_listener:
            self.play_state_listener(state)

    def set_k(self, k):
        self.__init_problem(k)
        self.__init_search()

    def sizeHint(self):
        return QSize(750, 750) if self.search else QSize(0, 0)

    def solve(self):
        self.stop()

        if self.search:
            with self.drawing_lock:
                while not self.search.is_complete():
                    self.search.step()

            if self.search_state_listener:
                self.search_state_listener(self.search)

            self.update()

    def step(self):
        if self.problem:
            if self.search and not self.search.is_complete():
                with self.drawing_lock:
                    self.search.step()

                if self.search_state_listener:
                    self.search_state_listener(self.search)

                self.update()
            else:
                self.__init_search()

    def stop(self):
        self.set_playing(False)
        if self.play_thread:
            self.play_thread.join()

    def toggle_play(self):
        if not self.is_playing:
            if self.search.is_complete():
                self.__init_search()

            self.set_playing(True)
            self.play_thread = threading.Thread(target=self.play)
            self.play_thread.start()
        else:
            self.set_playing(False)

class VertexColoringApplication(QMainWindow):
    def __init__(self):
        super(VertexColoringApplication, self).__init__()

        self.vertex_coloring_widget = VertexColoringWidget(
            self,
            self.update_search_state,
            self.update_play_state,
            self.update_k_state)

        self.label_search_state = QLabel()
        self.label_search_nodes = QLabel()
        self.initialize_group_box_control()

        top_layout = QVBoxLayout()
        top_layout.addWidget(self.group_box_control)
        top_layout.addStretch(1)

        middle_layout = QHBoxLayout()
        middle_layout.addWidget(self.vertex_coloring_widget)
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

        self.label_k = QLabel("K:")

        self.spinbox_k = QSpinBox()
        self.spinbox_k.setMinimum(1)
        self.spinbox_k.setMaximum(9)
        self.spinbox_k.setValue(4)
        self.spinbox_k.valueChanged.connect(self.vertex_coloring_widget.set_k)

        layout_input = QHBoxLayout()
        layout_input.addWidget(self.combo_box_file_selector)
        layout_input.addWidget(self.label_k)
        layout_input.setAlignment(self.label_k, Qt.AlignRight)
        layout_input.addWidget(self.spinbox_k)

        self.slider_frequency = QSlider(Qt.Horizontal)
        self.slider_frequency.setRange(5, 1000)
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
        layout.addLayout(layout_input)
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

    def update_k_state(self, k):
        self.spinbox_k.setValue(k)

    def update_search_state(self, search):
        def format_node(n):
            if not n.action:
                return "NO ASSUMPTIONS"
            else:
                return "ASSUMPTION Vertex{0} is {1}".format(
                    n.action[0].identity.value[0],
                    self.vertex_coloring_widget.color_to_text[n.action[1]])

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

    def update_play_state(self, is_playing):
        self.button_play.setText("Play" if not is_playing else "Stop")

def main():
    app = QApplication(sys.argv)
    search_application = VertexColoringApplication()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
