from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileSystemModel, QTreeView
import sys, os
from PyQt5.QtCore import pyqtSignal, pyqtSlot

import qtwindow
from model import WT_processing_pipeline

# convert ui file to py if using qt designer
# pyuic5 qtwindow.ui -o qtwindow.py

# Add to spec file and run spec file
#import sys
#sys.setrecursionlimit(5000)


class ExampleApp(QtWidgets.QMainWindow, qtwindow.Ui_MainWindow):
	
    def __init__(self, parent=None):

        super(self.__class__, self).__init__()
        self.setupUi(self)

        # file selection
        self.fileNamePath = 'refrence.dbf'
        self.pushButton.clicked.connect(self.loadFile)

        # wall thickness list
        self.wtlistitems = [3.05,3.18,3.58,3.96,4.37,4.78,5.49,6.35,7.14,7.62,11.13,15.24]
        
        for wt in self.wtlistitems:
            self.wallThicknessList.addItem(str(wt))
        # make list values editable by adding the flag
        for index in range(self.wallThicknessList.count()):
            item = self.wallThicknessList.item(index)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        
        self.wallThicknessList.clicked.connect(self.edit_current)
    
        # pipe size spin box, when changed repopulate WT list
        self.spinBox.valueChanged.connect(self.valuechange)
        # remove double clicked item
        self.wallThicknessList.itemDoubleClicked.connect(self.item_dclick)

        # radio button
        self.radioButton.setChecked(False)
        self.radioButton.toggled.connect(lambda:self.btnstate(self.radioButton))

        # double spin box
        self.spinButton.clicked.connect(self.clickspinbox)
        
        # check box
        self.checkBox.stateChanged.connect(self.clickBox)
        self.make_copy = True

        # run model button
        self.runButton.setToolTip('push to run WT model')
        self.runButton.clicked.connect(self.clickrun)
    
    def loadFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select DBF", "", "(*.dbf);;All Files (*)") # Ask for file    
        if fileName:
            self.fileNamePath = fileName
            print(fileName)
    
    def wallthickcalc(self):
        spinval = self.spinBox.value()

        wts = {
            '3':[3.05,3.18,3.58,3.96,4.37,4.78,5.49,6.35,7.14,7.62,11.13,15.24],
            '4':[2.11,2.77,3.05,3.18,3.58,3.96,4.37,4.78,5.74,6.35,7.14,8.08]}

        cycle = True
        count = 0
        while cycle:
            print(wts.keys()[0])
            cycle(False)

    def valuechange(self):

        # change WT list
        self.wallThicknessList.clear()

        wts = {
                '3':[3.05,3.18,3.58,3.96,4.37,4.78,5.49,6.35,7.14,7.62,11.13,15.24],
                '4':[2.11,2.77,3.05,3.18,3.58,3.96,4.37,4.78,5.16,5.56,6.02,6.35,7.14,7.92],
                '5':[0,0,0,0],
                '6':[2.11,2.77,3.18,3.40,3.58,3.96,4.37,4.78,5.16,5.56,6.35,7.11,7.92,8.74,9.53,10.97,12.7,14.27,15.88],
                '8':[0,0,0,0],
                '10':[5.74,6.35,7.14,8.08],
                '12':[],
                '14':[5.74,6.35,7.14,8.08],
                '16':[],
                '18':[5.74,6.35,7.14,8.08],
                '20':[],
                '22':[5.74,6.35,7.14,8.08],
                '24':[],
                '26':[5.74,6.35,7.14,8.08],
                '28':[],
                '30':[5.74,6.35,7.14,8.08],
                '32':[],
                '34':[5.74,6.35,7.14,8.08],
                '36':[],
                '38':[5.74,6.35,7.14,8.08],
                '40':[],
                '42':[5.74,6.35,7.14,8.08],
                '44':[],
                '46':[5.74,6.35,7.14,8.08],
                '48':[],
                '52':[5.74,6.35,7.14,8.08],
                '55':[],
                '60':[5.74,6.35,7.14,8.08],
                }

        while 1:
            for key in wts.keys():
                if int(key) == self.spinBox.value():
                    self.wtlistitems = wts[key]
                    break
            break

        for wt in self.wtlistitems:
            self.wallThicknessList.addItem(str(wt))
        
        for index in range(self.wallThicknessList.count()):
            item = self.wallThicknessList.item(index)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
    
    def item_dclick(self,item):
        # get item double clicked and remove it from list
        self.wallThicknessList.takeItem(self.wallThicknessList.row(item))

    def edit_current(self,event):
        index = self.wallThicknessList.currentIndex()
        if index.isValid():
            item = self.wallThicknessList.itemFromIndex(index)
            if not item.isSelected():
                item.setSelected(True)
            self.wallThicknessList.edit(index)
    
    def btnstate(self,b):
        if b.isChecked() == True:
            print(b.text()+" is selected")
        else:
            print(b.text()+" is deselected")

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        print(self.radioButton.isChecked())
    
    def clickspinbox(self):
        addToList = self.doubleSpinBox.value()
        self.wallThicknessList.addItem(str(addToList))

    def clickBox(self, state):
        if state == QtCore.Qt.Checked:
            self.make_copy = True
        else:
            self.make_copy = False

    @pyqtSlot()
    def clickrun(self):
        print('runnning')

        path = self.fileNamePath
        pipe_WT_TBD = []
        for i in range(self.wallThicknessList.count()):
            pipe_WT_TBD.append(float(self.wallThicknessList.item(i).text()))

        assign_types_ = self.radioButton.isChecked()

        print(path, pipe_WT_TBD, assign_types_,self.make_copy)
  
        WT_processing_pipeline(path, pipe_WT_TBD, assign_types_, self.make_copy)

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec()

if __name__ == '__main__':
    main()