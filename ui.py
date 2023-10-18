import sys
import storage
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QWidget, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView

class ScrollableTextWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create a central widget to hold the layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout to arrange the elements
        layout = QVBoxLayout()

        # Create headline
        headline_edit = QTextEdit()

        # Create buttons and add them to the layout
        button1 = QPushButton("Button 1")
        button2 = QPushButton("Button 2")
        layout.addWidget(button1)
        layout.addWidget(button2)

        # Create a QTableWidget with 4 columns
        table = QTableWidget()
        table.setColumnCount(4)

        # Set the table headers
        table.setHorizontalHeaderLabels(["Name", "Rating", "Year", ""])

        # Add rows and data to the table
        tableData = populateMovieListFromDict()
        for row in range(len(tableData)):
            table.insertRow(row)
            for col in range(3):
                item = QTableWidgetItem(tableData[row][col])
                table.setItem(row, col, item)
            viewedButton = QPushButton("Seen")
            viewedButton.clicked.connect(self.viewedButtonClicked)
            table.setCellWidget(row, 3, viewedButton)

        # Configure the table to expand horizontally and display column headers
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)

        layout.addWidget(table)
        

        # Set the layout for the central widget
        central_widget.setLayout(layout)

        self.setWindowTitle("Movie Picker")
        self.setGeometry(100, 100, 800, 600)
    
    def viewedButtonClicked(self):
        sender = self.sender()
        if isinstance(sender, QPushButton):
            # Find the row of the button that was clicked
            row = -1
            for r in range(self.centralWidget().layout().itemAt(2).layout().count()):
                if sender == self.centralWidget().layout().itemAt(2).layout().itemAt(r).itemAt(3).widget():
                    row = r
                    break
            if row != -1:
                print(f"Button clicked in row {row}")

def populateMovieListFromDict():
    tableColumns = 3
    
    movieDict = storage.requestDataFile()
    movieList = []
    for movieItem in movieDict.values():
        movieListItem = ['']*tableColumns
        movieListItem[0] = movieItem['name']
        movieListItem[1] = movieItem['rating']
        movieListItem[2] = movieItem['year']
        movieList.append(movieListItem)
    return movieList
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScrollableTextWindow()
    window.show()
    sys.exit(app.exec_())