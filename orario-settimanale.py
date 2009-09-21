#!/usr/bin/env python
# -*- coding: utf-*-
#
# orario-settimanale.py
#
# Copyright 2009 Francesco Frassinelli <fraph24@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

""" This program allows you to get a nice weekly agenda :) """

# Default settings (italian language)
#  * dbfilename -> Where orario-settimanale.py should take its datas
#  * days       -> The days of the week
#  * hours      -> The hours that are important in your days
#  * shift      -> It adds its value to every hour
settings = {
    "dbfilename":"agenda.db",
    "days":"Lunedì Martedì Mercoledì Giovedì Venerdì Sabato",
    "hours":"8 9 10 11 12 13 14 15 16 17 18",
    "shift":".15",
}

# Managing settings
dbfilename = settings["dbfilename"]
days = settings["days"].decode("utf-8").split()
hours = [hour+settings["shift"] for hour in settings["hours"].split()]

# Importing QT4 graphical toolkit and some built-in python libs
from PyQt4 import QtGui, QtCore
import itertools, shelve, sys

# Lambdas made for import/export of text from/to QTableWidget
fromQtToPlain = lambda data: str(data.text().toUtf8())
fromPlainToQt = lambda data: QtGui.QTableWidgetItem(data.decode("utf-8"))

class MainWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        
        # Indexes of columns and rows, in order to iterate them quickly
        self.columnIndex, self.rowIndex = range(len(days)), range(len(hours))
        
        # Initialization and population of self.table
        self.table = QtGui.QTableWidget(len(hours), len(days))
        self.table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.table.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(QtCore.QStringList(days))
        self.table.setVerticalHeaderLabels(QtCore.QStringList(hours))
        for column, row in itertools.product(self.columnIndex, self.rowIndex):
            self.table.setItem(row, column, QtGui.QTableWidgetItem())
        
        # Inizialization of self.notes
        self.notes = QtGui.QTextEdit()
        
        # Setting up layout
        layout = QtGui.QGridLayout()
        layout.addWidget(self.table, 0, 0)
        layout.addWidget(self.notes, 0, 1)
        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 1)
        self.setLayout(layout)
    
    def load(self):
        """ It reads the information from the database """
        db = shelve.open(dbfilename, "r")
        table = db["table"]
        notes = db["notes"]
        db.close()
        for column, row in itertools.product(self.columnIndex, self.rowIndex):
            self.table.setItem(row, column, fromPlainToQt(table[column][row]))
        self.notes.setHtml(notes)
    
    def save(self):
        """ It writes the information on the database """
        table = [[fromQtToPlain(self.table.item(row, column))
                 for row in self.rowIndex] for column in self.columnIndex]
        notes = self.notes.toHtml()
        db = shelve.open(dbfilename, "n")
        db["table"] = table
        db["notes"] = notes
        db.close()

class Agenda(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        # Setting up title and geometry of the window
        self.setWindowTitle("Orario settimanale")
        screen = QtGui.QDesktopWidget().screenGeometry()
        width, height = 1000, 400
        self.setGeometry((screen.width()-width)/2, (screen.height()-height)/2,
                         width, height)
        
        # Setting up MainWidget
        self.mainWidget = MainWidget(self)
        self.setCentralWidget(self.mainWidget)
        
        # Setting up actions toolbar
        self.toolbar = QtGui.QToolBar("Actions")
        self.addToolButton("Apri", "document-open", self.mainWidget.load)
        self.addToolButton("Salva", "document-save", self.mainWidget.save)
        self.toolbar.addSeparator()
        self.addToolButton("Esci", "application-exit",
                           QtGui.qApp, QtCore.SLOT("quit()"))
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
    
    def addToolButton(self, text, icon, *args):
        """ It adds the generated button to the toolbar """
        button = QtGui.QToolButton()
        button.setText(text)
        button.setIcon(QtGui.QIcon("icons/%s.png" % icon))
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.connect(button, QtCore.SIGNAL("clicked()"), *args)
        self.toolbar.addWidget(button)

def main():
    """ Setting up the program """
    application = QtGui.QApplication(sys.argv)
    agenda = Agenda()
    agenda.show()
    sys.exit(application.exec_())

if __name__ == "__main__":
    main()

