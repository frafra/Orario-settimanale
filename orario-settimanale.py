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

""" Questo programma permette di avere sottomano un orario settimanale """

from PyQt4 import QtGui, QtCore
from sys import argv, exit

class Tabella(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        
        days = (u"Lunedì", u"Martedì", u"Mercoledì",
                u"Giovedì", u"Venerdì", u"Sabato")
        hours = ("8.15", "9.15", "10.15", "11.15", "12.15", "13.15",
                 "14.15", "15.15", "16.15", "17.15", "18.15")
        
        self.tabella = QtGui.QTableWidget(len(hours), len(days))
        self.tabella.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tabella.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tabella.setHorizontalHeaderLabels(QtCore.QStringList(days))
        self.tabella.setVerticalHeaderLabels(QtCore.QStringList(hours))
        
        self.notes = QtGui.QTextEdit()
        
        layout = QtGui.QGridLayout()
        layout.addWidget(self.tabella, 0, 0)
        layout.addWidget(self.notes, 0, 1)
        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 1)
        self.setLayout(layout)

class Orario(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.setWindowTitle("Orario settimanale")
        
        screen = QtGui.QDesktopWidget().screenGeometry()
        width, height = 1000, 400
        self.setGeometry((screen.width() - width) / 2,
            (screen.height() - height) / 2, width, height)
        
        self.tabella = Tabella(self)
        self.setCentralWidget(self.tabella)

if __name__ == "__main__":
    APP = QtGui.QApplication(argv)
    ORARIO = Orario()
    ORARIO.show()
    exit(APP.exec_())
