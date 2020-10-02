import sys
import datetime
import pickle
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/forms/main_window.ui", self)
        
        self.noteTitleEdit.textChanged.connect(lambda: self.note_title_changed())
        self.actionAbout.triggered.connect(lambda: self.help_show())
    
    def note_title_changed(self): # if note title changes - window title changes too
        if self.get_note_title().strip() != "":
            self.setWindowTitle("NoteMap - " + self.get_note_title().strip())
        else:
            self.setWindowTitle("NoteMap")
        self.note_unsaved()
        
    def note_unsaved(self):
        if self.windowTitle() != "NoteMap":
            self.setWindowTitle(self.windowTitle() + "*")
    
    def get_note_title(self):
        return str(self.noteTitleEdit.text())
    
    def get_note_text(self):
        return self.noteTextEdit.toPlainText() # returns [' ', '\t', '\n']
    
    def help_show(self):
        self.about_window = AboutWindow(self)
        self.about_window.move(self.x() + (self.width() // 2 - self.about_window.width() // 2), self.y() + (self.height() // 2 - self.about_window.height() // 2))
        self.about_window.show()


class AboutWindow(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi("src/forms/about_window.ui", self)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())