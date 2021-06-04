import sys
import PyQt5 as pq
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random
import math

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        # Set window size, title, and icon
        self.setWindowTitle("Mine Sweeper")
        self.setWindowIcon(QIcon('Images/icon.png'))
        self.setGeometry(50, 50, 800, 800)

        # Create central widget
        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)

        # Set menu as central widget
        self.menuWidget = Menu(self)
        self.centralWidget.addWidget(self.menuWidget)
        self.gameWidget = None

        # init game creation vars
        self.rows = 0
        self.cols = 0
        self.bombs = 0

    def StartGame(self):
        # Set game creation vars from menu
        self.rows = self.menuWidget.GetRows()
        self.cols = self.menuWidget.GetCols()
        self.bombs = self.menuWidget.GetBombs()

        # Cleanup
        if self.gameWidget != None:
            self.centralWidget.removeWidget(self.gameWidget)
            self.gameWidget.deleteLater()
            self.gameWidget = None

        # Set game widget as central widget
        self.gameWidget = Game(self)
        self.centralWidget.addWidget(self.gameWidget)
        self.centralWidget.setCurrentWidget(self.gameWidget)

    def SetMenu(self):
        # Cleanup
        if self.menuWidget != None:
            self.centralWidget.removeWidget(self.menuWidget)
            self.menuWidget.deleteLater()
            self.menuWidget = None

        # Set menu widget as central widget
        self.menuWidget = Menu(self)
        self.centralWidget.addWidget(self.menuWidget)
        self.centralWidget.setCurrentWidget(self.menuWidget)

    def Exit(self):
        sys.exit()

class Menu(QWidget):
    def __init__(self, parent = None):
        super(Menu, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(0)

        self.numRows = 8
        self.numCols = 8
        self.numBombs = 10

        # Title
        label = QLabel()
        label.setText("Mine Sweeper")
        self.layout.addWidget(label)
        label.setAlignment(Qt.AlignCenter)

        # Setup sliders for game settings
        rowSlider = QSlider(Qt.Horizontal)
        colSlider = QSlider(Qt.Horizontal)
        self.bombSlider = QSlider(Qt.Horizontal)

        rowSlider.setMaximum(35)
        colSlider.setMaximum(50)
        self.bombSlider.setMaximum(450)

        rowSlider.setMinimum(8)
        colSlider.setMinimum(8)
        self.bombSlider.setMinimum(int(self.numRows * self.numCols * 0.1))
        self.bombSlider.setMaximum(int(self.numRows * self.numCols * 0.25))
        self.bombSlider.setValue(10)

        rowSlider.setSingleStep(1)
        colSlider.setSingleStep(1)
        self.bombSlider.setSingleStep(1)

        rowSlider.valueChanged.connect(lambda: self.SetRows(rowSlider.value()))
        colSlider.valueChanged.connect(lambda: self.SetCols(colSlider.value()))
        self.bombSlider.valueChanged.connect(lambda: self.SetBombs(self.bombSlider.value()))

        # Labels for game vars
        self.rowLabel = QLabel()
        self.colLabel = QLabel()
        self.bombLabel = QLabel()
        
        self.rowLabel.setText("Rows: " + str(self.numRows))
        self.colLabel.setText("Columns: " + str(self.numCols))
        self.bombLabel.setText("Bombs: " + str(self.numBombs))

        # Add sliders and labels to layout
        self.layout.addWidget(self.rowLabel)
        self.layout.addWidget(rowSlider)
        self.layout.addWidget(self.colLabel)
        self.layout.addWidget(colSlider)
        self.layout.addWidget(self.bombLabel)
        self.layout.addWidget(self.bombSlider)

        # Button to start game
        buttonStart = QPushButton(self)
        buttonStart.setText("Start Game")
        buttonStart.clicked.connect(self.parent().StartGame)
        self.layout.addWidget(buttonStart)

        # Button to exit game
        buttonExit = QPushButton(self)
        buttonExit.setText("Quit")
        buttonExit.clicked.connect(self.parent().Exit)
        self.layout.addWidget(buttonExit)

    def SetRows(self, num):
        self.numRows = num
        self.rowLabel.setText("Rows: " + str(self.numRows))
        self.SetBombs(int(self.numRows * self.numCols * 0.15))
        self.bombSlider.setValue(int(self.GetBombs()))
        self.bombSlider.setMinimum(int(self.numRows * self.numCols * 0.1))
        self.bombSlider.setMaximum(int(self.numRows * self.numCols * 0.25))

    def SetCols(self, num):
        self.numCols = num
        self.colLabel.setText("Columns: " + str(self.numCols))
        self.SetBombs(int(self.numRows * self.numCols * 0.15))
        self.bombSlider.setValue(int(self.GetBombs()))
        self.bombSlider.setMinimum(int(self.numRows * self.numCols * 0.1))
        self.bombSlider.setMaximum(int(self.numRows * self.numCols * 0.25))

    def SetBombs(self, num):
        self.numBombs = num
        self.bombLabel.setText("Bombs: " + str(self.numBombs))

    def GetRows(self):
        return self.numRows

    def GetCols(self):
        return self.numCols

    def GetBombs(self):
        return self.numBombs

class Game(QWidget):
    def __init__(self, parent = None):
        super(Game, self).__init__(parent)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(0)

        size = screen.size().height() - 200
        self.layout.maximumSize().setHeight(size)
        self.layout.maximumSize().setWidth(size)
        self.layout.setSizeConstraint(QLayout.SetMaximumSize)

        # Create toolbar
        toolBar = QToolBar()
        self.layout.setMenuBar(toolBar)

        # Add items to toolbar
        toolButton = QToolButton()
        toolButton.setText("Menu")
        toolButton.setCheckable(True)
        toolButton.setAutoExclusive(True)
        toolButton.clicked.connect(self.parent().SetMenu)
        toolBar.addWidget(toolButton)

        toolButton = QToolButton()
        toolButton.setText("Restart")
        toolButton.setCheckable(True)
        toolButton.setAutoExclusive(True)
        toolButton.clicked.connect(self.parent().StartGame)
        toolBar.addWidget(toolButton)

        bombLabel = QLabel()
        bombLabel.setText("Mines Left: ")
        toolBar.addWidget(bombLabel)

        self.bombLeft = QLabel()
        self.bombLeft.setText(str(0))
        toolBar.addWidget(self.bombLeft)

        # Create Board
        self.rows = self.parent().rows
        self.cols = self.parent().cols
        self.bombs = self.parent().bombs

        self.tiles = [[0 for i in range(self.cols)] for j in range(self.rows)]

        # Matrix for checking flags
        self.flags = [[0 for i in range(self.cols)] for j in range(self.rows)]

        # List for buttons
        self.Buttons = [[0 for i in range(self.cols)] for j in range(self.rows)]

        # Create Buttons
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                temp = QPushButton("")
                temp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                temp.setFixedSize(25,25)
                temp.clicked.connect(self.ButtonClick)
                temp.installEventFilter(self)
                temp.setIcon(QIcon('Images/normal.png'))
                self.Buttons[i][j] = temp
                self.layout.addWidget(temp, i, j)

        # Set Bombs
        for x in range(self.bombs):
            i = random.randint(0, self.rows - 1)
            j = random.randint(0, self.cols - 1)
            while(self.tiles[i][j] == 9):
                i = random.randint(0, self.rows - 1)
                j = random.randint(0, self.cols - 1)

            self.tiles[i][j] = 9

            # Increase each number by 1 for each surrounding tile of a bomb
            if i - 1 >= 0 and j + 1 < self.cols and self.tiles[i-1][j+1] != 9:
                self.tiles[i-1][j+1] += 1

            if i + 1 < self.rows and j - 1 >= 0 and self.tiles[i+1][j-1] != 9:
                self.tiles[i+1][j-1] += 1

            if j + 1 < self.cols and self.tiles[i][j+1] != 9:
                self.tiles[i][j+1] += 1

            if i + 1 < self.rows and j + 1 < self.cols and self.tiles[i+1][j+1] != 9:
                self.tiles[i+1][j+1] += 1

            if i - 1 >= 0 and j - 1 >= 0 and self.tiles[i-1][j-1] != 9:
                self.tiles[i-1][j-1] += 1

            if j - 1 >= 0 and self.tiles[i][j-1] != 9:
                self.tiles[i][j-1] += 1

            if i - 1 >= 0 and self.tiles[i-1][j] != 9:
                self.tiles[i-1][j] += 1

            if i + 1 < self.rows and self.tiles[i+1][j] != 9:
                self.tiles[i+1][j] += 1

        # Number of tiles that are not bombs
        self.winTiles = (self.rows * self.cols) - self.bombs
        self.winCounter = 0
        self.bombValue = self.bombs
        self.bombLeft.setText(str(self.bombValue))

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                self.PlaceFlag(obj)
        return QObject.event(obj, event)

    def GameOver(self):
        # Reveal all bombs and set all tiles to inactive
        for i in range(self.rows):
            for j in range(self.cols):
                if self.tiles[i][j] == 9:
                    self.Buttons[i][j].setIcon(QIcon('Images/' + str(self.tiles[i][j]) + '.png'))
                self.tiles[i][j] = -1

        msgBox = QMessageBox()
        msgBox.setText("You detonated a mine!")
        msgBox.setWindowTitle("Game Over")
        msgBox.setStandardButtons(QMessageBox.Retry)

        if msgBox.exec() == QMessageBox.Retry:
            self.parent().parent().StartGame()

    def Victory(self):
        msgBox = QMessageBox()
        msgBox.setText("You Win!")
        msgBox.setWindowTitle("Victory!")
        msgBox.setStandardButtons(QMessageBox.Ok)

        if msgBox.exec() == QMessageBox.Ok:
            self.parent().parent().StartGame()

    def PlaceFlag(self, obj):
        # Get button index
        button = obj
        idx = self.layout.indexOf(button)
        location = self.layout.getItemPosition(idx)
        i = location[0]
        j = location[1]

        if self.tiles[i][j] != -1:
            if self.flags[i][j] == 1:
                # If already flagged remove flag
                self.flags[i][j] = 0
                button.setIcon(QIcon('Images/normal.png'))
                self.bombValue += 1
                self.bombLeft.setText(str(self.bombValue))
            elif self.bombValue > 0:
                # Set it to a flag
                self.flags[i][j] = 1
                button.setIcon(QIcon('Images/flag.png'))
                self.bombValue -= 1
                self.bombLeft.setText(str(self.bombValue))

    def ButtonClick(self):
        # Get button index
        button = self.sender()
        idx = self.layout.indexOf(button)
        location = self.layout.getItemPosition(idx)
        i = location[0]
        j = location[1]

        if self.tiles[i][j] != -1:
            # Display button number
            button.setIcon(QIcon('Images/' + str(self.tiles[i][j]) + '.png'))
            
            if self.tiles[i][j] != 9:
                self.winCounter += 1

                # If was flagged remove flag and increase mine counter
                if self.flags[i][j] == 1:
                    self.bombValue += 1
                    self.bombLeft.setText(str(self.bombValue))

                # Check if the player won
                if self.winCounter == self.winTiles:
                    self.Victory()
            else:
                self.GameOver()

            # If zero display all surrounding tiles
            if self.tiles[i][j] == 0:
                self.tiles[i][j] = -1

                if i - 1 >= 0 and j + 1 < self.cols and self.tiles[i-1][j+1] != -1:
                    self.Buttons[i-1][j+1].click()

                if i + 1 < self.rows and j - 1 >= 0 and self.tiles[i+1][j-1] != -1:
                    self.Buttons[i+1][j-1].click()

                if j + 1 < self.cols and self.tiles[i][j+1] != -1:
                    self.Buttons[i][j+1].click()

                if i + 1 < self.rows and j + 1 < self.cols and self.tiles[i+1][j+1] != -1:
                    self.Buttons[i+1][j+1].click()

                if i - 1 >= 0 and j - 1 >= 0 and self.tiles[i-1][j-1] != -1:
                    self.Buttons[i-1][j-1].click()

                if j - 1 >= 0 and self.tiles[i][j-1] != -1:
                    self.Buttons[i][j-1].click()

                if i - 1 >= 0 and self.tiles[i-1][j] != -1:
                    self.Buttons[i-1][j].click()

                if i + 1 < self.rows and self.tiles[i+1][j] != -1:
                    self.Buttons[i+1][j].click()
            else:
                self.tiles[i][j] = -1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = MainWindow()
    screen.show()
    sys.exit(app.exec_())