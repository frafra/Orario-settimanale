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
import shelve

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
        
        for c in xrange(self.tabella.columnCount()):
            for r in xrange(self.tabella.rowCount()):
                self.tabella.setItem(r, c, QtGui.QTableWidgetItem())
        
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
        
        self.toolbar = QtGui.QToolBar("Actions")
        button_style = QtCore.Qt.ToolButtonTextBesideIcon
        
        apri = QtGui.QToolButton()
        apri.setText("Apri")
        apri.setIcon(QtGui.QIcon("icons/document-open.png"))
        apri.setToolButtonStyle(button_style)
        self.connect(apri, QtCore.SIGNAL("clicked()"), self.apri_action)
        self.toolbar.addWidget(apri)
        
        salva = QtGui.QToolButton()
        salva.setText("Salva")
        salva.setIcon(QtGui.QIcon("icons/document-save.png"))
        salva.setToolButtonStyle(button_style)
        self.connect(salva, QtCore.SIGNAL("clicked()"), self.salva_action)
        self.toolbar.addWidget(salva)
        
        self.toolbar.addSeparator()
        
        esci = QtGui.QToolButton()
        esci.setText("Esci")
        esci.setIcon(QtGui.QIcon("icons/application-exit.png"))
        esci.setToolButtonStyle(button_style)
        self.connect(esci, QtCore.SIGNAL("clicked()"),
                     QtGui.qApp, QtCore.SLOT("quit()"))
        self.toolbar.addWidget(esci)
        
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        
        self.tabella = Tabella(self)
        self.setCentralWidget(self.tabella)
    
    def apri_action(self):
        db = shelve.open("orario.db", "r")
        data = db["data"]
        notes = db["notes"]
        self.tabella.notes.setHtml(notes)
        db.close()
        for c, column in enumerate(data):
            for r, row in enumerate(column):
                self.tabella.tabella.item(r, c).setText(row.decode("utf-8"))
    
    def salva_action(self):
        data = []
        for column in xrange(self.tabella.tabella.columnCount()):
            data.append([])
            for row in xrange(self.tabella.tabella.rowCount()):
                item = self.tabella.tabella.item(row, column)
                data[-1].append(str(item.text().toUtf8()))
        db = shelve.open("orario.db", "c")
        db["data"] = data
        db["notes"] = self.tabella.notes.toHtml()
        db.close()

if __name__ == "__main__":
    APP = QtGui.QApplication(argv)
    ORARIO = Orario()
    ORARIO.show()
    exit(APP.exec_())
