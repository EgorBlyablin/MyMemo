import subprocess
import sys

try:
    import datetime
    import pickle
    import time

    import PyQt5
    from PyQt5 import QtGui, QtWidgets, uic
    from PyQt5.QtCore import QEvent
    from PyQt5.QtGui import QKeyEvent
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
except:
    for library in ["datetime", "pickle", "PyQt5", "time"]:
        subprocess.run(["pip install", library])
        
    import datetime
    import pickle
    import time

    import PyQt5
    from PyQt5 import QtGui, QtWidgets, uic
    from PyQt5.QtCore import QEvent
    from PyQt5.QtGui import QKeyEvent
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/forms/main_window.ui", self)
        self.about_window = AboutWindow(self)
        self.about_quit = AboutQuit(self)
        self.unsaved = False
        self.notes_dict = {}

        self.redraw_list_menu()
        self.noteTitleEdit.textEdited.connect(lambda: self.note_changed())
        self.noteTextEdit.textChanged.connect(lambda: self.note_changed())
        self.saveButton.clicked.connect(lambda: self.about_quit.save_changes())
        self.deleteButton.clicked.connect(lambda: self.delete_note())
        self.notesList.itemClicked.connect(self.load_note)
        self.actionSaveNote.triggered.connect(
            lambda: self.about_quit.save_changes()
            )
        self.actionRemoveNote.triggered.connect(
            lambda: self.about_quit.delete_changes()
            )
        self.actionAbout.triggered.connect(
            lambda: self.about_window.help_show()
            )
        self.actionQuit.triggered.connect(lambda: self.close_app())
    
    def note_changed(self): # [note] if note title changes - 
                            # window title changes too
        if self.get_note_title().strip() != "":
            self.setWindowTitle("MyMemo - " + self.get_note_title().strip())
        else:
            self.setWindowTitle("MyMemo - untitled")
        self.note_unsaved()
        if self.get_note_title().strip() == "":
            self.saveButton.setDisabled(True)
        else:
            self.saveButton.setEnabled(True)
    
    def add_notes_list_menu(self, element):
        self.last = QtWidgets.QTreeWidgetItem(self.notesList, [element["title"], element["date"]])
        self.notesList.setCurrentItem(self.last)
    
    def redraw_list_menu(self):
        self.notesList.clear()
        pprint.pprint(self.notes_dict)
        for element in list(self.notes_dict.keys()):
            QtWidgets.QTreeWidgetItem(self.notesList, 
                                      [self.notes_dict[element]["title"],
                                       self.notes_dict[element]["date"]]
                                      )
        
    def note_unsaved(self, status=True):
        if status:
            if self.windowTitle()[-1] != "*":
                self.setWindowTitle(self.windowTitle() + "*")
            self.unsaved = True
        else:
            if self.windowTitle()[-1] == "*":
                self.setWindowTitle(self.windowTitle()[:-1])
            self.unsaved = False
    
    def load_note(self, item, column):
        self.last = item
        self.deleteButton.setEnabled(True)
        self.saveButton.setDisabled(True)
        current_note_name = item.text(0)
        current_note_date = item.text(1)
        current_note = self.notes_dict[current_note_date]
        self.noteTitleEdit.setText(current_note["title"])
        self.noteTextEdit.setPlainText(current_note["text"])
        self.setWindowTitle("MyMemo - " + current_note_name)
        self.note_unsaved(False)

    def delete_note(self):
        self.notesList.takeTopLevelItem(
            self.notesList.indexOfTopLevelItem(
                self.notesList.selectedItems()[0]
                )
            )
        self.noteTitleEdit.setText("")
        self.noteTextEdit.setPlainText("")
        self.setWindowTitle("MyMemo")
        self.note_unsaved(False)
        self.redraw_list_menu()
    
    def get_note_title(self):
        return str(self.noteTitleEdit.text())
    
    def get_note_text(self):
        return self.noteTextEdit.toPlainText() # [note] returns [' ', '\t', '\n']
    
    def closeEvent(self, event: QtGui.QCloseEvent):
        if self.unsaved == False:
            app.closeAllWindows()
            event.accept()
        else:
            self.close_app()
            event.ignore()
    
    def close_app(self):
        if self.about_window.isVisible():
            self.about_window.close()
        elif self.unsaved:
            self.about_quit.save_changes_window()
        else:
            app.closeAllWindows()        

class AboutWindow(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi("src/forms/about_window.ui", self)
    
    def help_show(self):
        if self.isVisible():
            self.close()
        else:
            self.move(
                mainWin.x() + (mainWin.width() // 2 - self.width() // 2), mainWin.y() + (mainWin.height() // 2 - self.height() // 2)
                )
            self.show()
    
    def closeEvent(self, event: QtGui.QCloseEvent):
        self.close()


class AboutQuit(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi("src/forms/about_quit.ui", self)
        self.saveButton.clicked.connect(lambda: self.save_changes())
        self.deleteButton.clicked.connect(lambda: self.delete_changes())
        self.cancelButton.clicked.connect(lambda: self.cancel_changes())

    def save_changes_window(self): # [note] if note isn't saved - ask to save
        self.move(
            mainWin.x() + (mainWin.width() // 2 - self.width() // 2),
            mainWin.y() + (mainWin.height() // 2 - self.height() // 2)
            )
        self.show()
    
    def save_changes(self):
        if mainWin.get_note_title() in list(mainWin.notes_dict.keys()):
            time_now = datetime.datetime.now()
            current_date_seconds_from_start = time_now.timestamp()
            current_date = str(time_now.strftime("%H:%M %d.%m.%Y"))
            mainWin.notes_dict[current_date] = {
            "title": mainWin.get_note_title(),
            "date": current_date,
            "text": mainWin.get_note_text(),
            "date_to_seconds": current_date_seconds_from_start
            }
        else:
            time_now = datetime.datetime.now()
            current_date_seconds_from_start = time_now.timestamp()
            current_date = str(time_now.strftime("%H:%M %d.%m.%Y"))
            mainWin.notes_dict[current_date] = {
                "title": mainWin.get_note_title(),
                "date": current_date,
                "text": mainWin.get_note_text(),
                "date_to_seconds": current_date_seconds_from_start
                }
        mainWin.redraw_list_menu()
        mainWin.note_unsaved(False)
        time.sleep(0.00001)
        if self.isVisible():
            mainWin.close_app()
    
    def delete_changes(self):
        mainWin.note_unsaved(False)
        app.closeAllWindows()
        
    def cancel_changes(self):
        self.close()

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.cancel_changes()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
