import sys
from PyQt5 import QtCore, QtGui, QtWidgets

import vi.grid
import vi.search.grid

class GridWidget(QtWidgets.QFrame):

    def __init__(self, parent):
        super(GridWidget, self).__init__(parent)
        self.spriteImage = QtGui.QImage("zelda.png")

        self.problem = vi.search.grid.Problem.from_grid_file(
            '/home/pveierland/permve-ntnu-tdt4136/assignment-3/problem/boards/board-2-3.txt')
        
        self.sprites = {
            '#':        QtCore.QRect(114, 111, 16, 16),
            'g':        QtCore.QRect(306, 569, 16, 16),
            'r':        QtCore.QRect(109, 263, 16, 16),
            'goal':     QtCore.QRect(102, 659, 16, 16),
            'flowers1': QtCore.QRect(323, 535, 16, 16),
            'land_border_water_south': QtCore.QRect(730, 253, 16, 16),
            'land_border_water_west': QtCore.QRect(690, 228, 16, 16),
            'land_border_water_east': QtCore.QRect(754, 229, 16, 16),
            'land_border_water_north': QtCore.QRect(730, 189, 16, 16)
        }

    def minimumSize(self):
        return QtCore.QSize(16 * self.problem.grid.width, 16 * self.problem.grid.height)

    def minimumSizeHint(self):
        return QtCore.QSize(16 * self.problem.grid.width, 16 * self.problem.grid.height)

    def lookup(self, coordinate):
        cell_types = {
            100: 'w', 50: 'm', 10: 'f', 5: 'g', 1: 'r', -1: 's'
        }

        if coordinate.x >= 0 and coordinate.x < self.problem.grid.width and \
           coordinate.y >= 0 and coordinate.y < self.problem.grid.height:
            #print(cell_types.get(self.problem.grid.values[coordinate.y][coordinate.x], None))
            return cell_types.get(self.problem.grid.values[coordinate.y][coordinate.x], None)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        color = QtGui.QColor(0x33333333)
        
        for y in range(self.problem.grid.height):
            for x in range(self.problem.grid.width):
                coordinate = vi.grid.Coordinate(x, y)
                element    = self.lookup(coordinate)
                sprite     = element

                if element == 'g':
                    if self.lookup(coordinate[1][0]) == 'w':
                        print(self.lookup(coordinate[1][0]))
                        sprite = 'land_border_water_north'
                    elif self.lookup(coordinate[0][-1]) == 'w':
                        sprite = 'land_border_water_west'
                    elif self.lookup(coordinate[0][1]) == 'w':
                        sprite = 'land_border_water_east'
                    elif self.lookup(coordinate[-1][0]) == 'w':
                        sprite = 'land_border_water_south'

                    painter.drawImage(
                        QtCore.QRect(x * 16, (self.problem.grid.height - y - 1) * 16, 16, 16),
                        self.spriteImage,
                        self.sprites[sprite])

        #painter.drawImage(
        #    QtCore.QRect(self.problem.grid.start.y * 16, self.problem.grid.start.x * 16, 16, 16),
        #    self.spriteImage,
        #    self.sprites['goal'])

class SearchApplication(QtWidgets.QMainWindow):
    def __init__(self):
        super(SearchApplication, self).__init__()

        self.grid_widget = GridWidget(self)
        #self.resize(200, 200)
        self.setWindowTitle('VI Search Algorithms')
        self.setCentralWidget(self.grid_widget)
        self.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    search_application = SearchApplication()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
