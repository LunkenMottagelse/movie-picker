import sys
import storage
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QWidget, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView

# - CentralWidget
# |- layout
#  |- button1
#  |- button2
#  |- table
#   |-


class ScrollableTextWindow(QMainWindow):
    # Private variables:
    # _movieDict
    # _tableData
    
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        # Create a central widget to hold the layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout to arrange the elements
        self._layout = QVBoxLayout()

        # Create headline
        headline_edit = QTextEdit()

        # Create buttons and add them to the layout
        button1 = QPushButton("Reset All")
        button1.clicked.connect(self.resetButtonClicked)
        button2 = QPushButton("Button 2")
        self._layout.addWidget(button1)
        self._layout.addWidget(button2)

        # Create a QTableWidget with 4 columns
        table = self.tableFactory()

        self._layout.addWidget(table)
        

        # Set the layout for the central widget
        central_widget.setLayout(self._layout)

        self.setWindowTitle("Movie Picker")
        self.setGeometry(100, 100, 800, 600)

    def resetButtonClicked(self):
        print("Refreshing database from IMDB")
        storage.updateDataFile()
        self.refreshTable()
    
    def viewedButtonClicked(self, movieTitle, rowNum):
        print(f"Button pressed for {movieTitle}")
        print(f"Button clicked in row {rowNum}")

        self._movieDict[movieTitle]['seen'] = True # Setting Movie to seen in the dictionary
        self.store_movieDict()
        self.refreshTable()

    def populateMovieListFromDict(self):
        self.update_movieDict()
        tableColumns = 3
        
        # movieDict = storage.requestDataFile()
        self._tableData = []
        for movieTitle, movieItem in self._movieDict.items():
            if movieItem['seen'] == False:
                movieListItem = ['']*tableColumns
                movieListItem[0] = movieTitle
                movieListItem[1] = movieItem['rating']
                movieListItem[2] = movieItem['year']
                self._tableData.append(movieListItem)

    def refreshTable(self):
        # The quest to find the tableWidget
        widget = self.centralWidget()
        tableWidget = None

        for child in widget.findChildren(QWidget):
            if isinstance(child, QTableWidget):
                tableWidget = child
                break
        if tableWidget == None:
            print("Could not find TableWidget!")
        else:
            # Making a new Table
            # Create a QTableWidget with 4 columns
            table = self.tableFactory(refresh=True, prevTable=tableWidget) # Flag indicates we try to restore previous scroll position and sorting order
            
            self._layout.removeWidget(tableWidget)
            self._layout.addWidget(table)

            sortingOrder = tableWidget.horizontalHeader().sortIndicatorOrder()
            sortColumn = tableWidget.horizontalHeader().sortIndicatorSection()
            verticalScrollPosition = tableWidget.verticalScrollBar().value()
            
            table.horizontalHeader().setSortIndicatorShown(True)
            table.horizontalHeader().setSortIndicator(sortColumn, sortingOrder)
            table.verticalScrollBar().setValue(verticalScrollPosition)

    def tableFactory(self, refresh=False, prevTable=None):
        table = QTableWidget()
        table.setColumnCount(4)
        table.setSortingEnabled(True)

        # Set the table headers
        table.setHorizontalHeaderLabels(["Name", "Rating", "Year", ""])

        # Add rows and data to the table
        self.populateMovieListFromDict()
        for row in range(len(self._tableData)):
            table.insertRow(row)
            for col in range(3):
                item = QTableWidgetItem(self._tableData[row][col])
                table.setItem(row, col, item)
            viewedButton = QPushButton("Seen")
            viewedButton.clicked.connect(lambda state, row=row: self.viewedButtonClicked(self._tableData[row][0], row))
            table.setCellWidget(row, 3, viewedButton)

        # Configure the table to expand horizontally and display column headers
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)

        table_style = """
                        QTableWidget {
                            background-color: #f0f0f0; /* Table background color */
                            border: 1px solid #ccc; /* Border around the table */
                        }
                        
                        QTableWidget QHeaderView::section {
                            background-color: #333; /* Header background color */
                            color: #fff; /* Header text color */
                        }
                        
                        QTableWidget::item {
                            background-color: #fff; /* Cell background color */
                            color: #333; /* Cell text color */
                            border: 1px solid #ccc; /* Cell border */
                        }
                        
                        QTableWidget::item:selected {
                            background-color: #66c2ff; /* Selected cell background color */
                            color: #fff; /* Selected cell text color */
                        }
                        
                        QTableWidget::item:hover {
                            background-color: #f2f2f2; /* Hovered cell background color */
                        }
                    """

        table.setStyleSheet(table_style)

        return table

    def update_movieDict(self):
        self._movieDict = storage.requestDataFile()

    def store_movieDict(self):
        storage.storeDataFile(self._movieDict)
    

if __name__ == '__main__':
    # storage.updateDataFile()
    app = QApplication(sys.argv)
    app.setStyle("WindowsVista")
    window = ScrollableTextWindow()
    window.show()
    sys.exit(app.exec_())