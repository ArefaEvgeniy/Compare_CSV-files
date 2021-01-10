#!/usr/bin/env python3
"""
File compare.py merges two csv files into one, depending on the user's
settings.
"""


import sys
import os

from PyQt5.QtWidgets import (  # pylint: disable=E0611
    QMainWindow, QWidget, QAction, QDesktopWidget, QApplication, QMessageBox,
    QFileDialog, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLabel,
    QGridLayout, QGroupBox, QStyleFactory, QTableView, QComboBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QAbstractTableModel  # pylint: disable=E0611
from PyQt5.QtGui import QIcon  # pylint: disable=E0611

import utils
import const


class Main(QMainWindow):
    """
    Class to show main window with Status Bar space for workspace and Tool Bar
    """
    def __init__(self):
        super().__init__()
        self.board = None
        self.statusbar = None
        self.clear_first_file = None
        self.clear_second_file = None
        self.generate_action = None
        self.undo_action = None
        self.redo_action = None
        self.initUI()

    def initUI(self):  # pylint: disable=C0103
        """
        Init UI of dialog window to select fields from CSV-file
        """
        self.board = Compare()
        self.setCentralWidget(self.board)

        self.statusbar = self.statusBar()
        self.board.compareStatusbar[str].connect(self.statusbar.showMessage)

        exit_action = QAction(QIcon(const.IMAGE_EXIT), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)

        open_first_file = QAction(QIcon(const.IMAGE_OPEN),
                                  'Open ' + const.BUTTONS[0], self)
        open_first_file.triggered.connect(self.board.btn_if1.clicked)

        open_second_file = QAction(QIcon(const.IMAGE_OPEN),
                                   'Open ' + const.BUTTONS[1], self)
        open_second_file.triggered.connect(self.board.btn_if2.clicked)

        self.clear_first_file = QAction(QIcon(const.IMAGE_CLEAR),
                                        const.CLEAR_BUTTONS[0], self)
        self.clear_first_file.triggered.connect(self.board.clear_data)
        self.clear_first_file.setDisabled(True)

        self.clear_second_file = QAction(QIcon(const.IMAGE_CLEAR),
                                         const.CLEAR_BUTTONS[1], self)
        self.clear_second_file.triggered.connect(self.board.clear_data)
        self.clear_second_file.setDisabled(True)

        self.generate_action = QAction(QIcon(const.IMAGE_GENERATE),
                                       const.BUTTONS[2], self)
        self.generate_action.triggered.connect(self.board.btn_gen.clicked)
        self.generate_action.setDisabled(True)

        self.undo_action = QAction(QIcon(const.IMAGE_UNDO),
                                   const.UNDO_REDO[0], self)
        self.undo_action.setShortcut('Ctrl+Z')
        self.undo_action.triggered.connect(self.board.set_settings)
        self.undo_action.setDisabled(True)

        self.redo_action = QAction(QIcon(const.IMAGE_REDO),
                                   const.UNDO_REDO[1], self)
        self.redo_action.setShortcut('Ctrl+Shift+Z')
        self.redo_action.triggered.connect(self.board.set_settings)
        self.redo_action.setDisabled(True)

        toolbar = self.addToolBar('Main Menu')
        toolbar.addAction(open_first_file)
        toolbar.addAction(self.clear_first_file)
        toolbar.addAction(open_second_file)
        toolbar.addAction(self.clear_second_file)
        toolbar.addAction(self.generate_action)
        toolbar.addAction(self.undo_action)
        toolbar.addAction(self.redo_action)
        toolbar.addAction(exit_action)

        screen = QDesktopWidget().screenGeometry()
        width = screen.width() / 5 * 4
        height = screen.height() / 5 * 4
        self.resize(width, height)
        self.move(width / 8, height / 8)

        self.setWindowTitle('Compare files')
        self.show()

    def closeEvent(self, event):  # pylint: disable=C0103
        """
        Before close main window ask 'Are you sure to quit?'
        """
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class TableModel(QAbstractTableModel):
    """
    Class to show data as table view
    """

    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        """
        See below for the nested-list data structure.
        .row() indexes into the outer list,
        .column() indexes into the sub-list
        """
        result = None
        if role == Qt.DisplayRole:
            result = self._data[index.row()][index.column()]
        return result

    def rowCount(self, index):  # pylint: disable=C0103, W0613
        """
        The length of the outer list.
        """
        return len(self._data)

    def columnCount(self, index):  # pylint: disable=C0103, W0613
        """
        The following takes the first sub-list, and returns
        the length (only works if all rows are an equal length)
        """
        return len(self._data[0])


class ChoiceFields(QDialog):
    """
    Class to select key-field and other fields from CSV-file for further
    processing in dialog window
    """

    def __init__(self, parent, data, index, path, key_field):
        super().__init__()
        self.parent = parent
        self.data = data
        self.index = index
        self.path = path
        self.buttons_field = []
        self.key = None
        self.is_close = None
        self.choice_key = None
        self.btn_accept = None
        self.btn_cancel = None
        self.key_field = key_field
        self.initUI()

    def initUI(self):  # pylint: disable=C0103
        """
        Init UI of dialog window to select fields from CSV-file
        """
        if self.key_field and self.key_field not in self.data[0]:
            self.is_close = False
            self.close()

        key_label = QLabel('Choice key field:')
        self.choice_key = QComboBox(self)
        if self.key_field is None:
            for item in self.data[0]:
                self.choice_key.addItem(item)
            self.choice_key.activated[str].connect(self.on_activated)
        else:
            self.choice_key.addItem(self.key_field)
            self.choice_key.setDisabled(True)

        fields_label = QLabel('Choice field for report (default - all:')
        for item in self.data[0]:
            btn = QPushButton(item, self)
            if item == self.choice_key.currentText():
                btn.setDisabled(True)
            btn.setCheckable(True)
            btn.setChecked(True)
            self.buttons_field.append(btn)

        self.btn_accept = QPushButton('Accept', self)
        self.btn_accept.clicked.connect(self.accept_clicked)

        self.btn_cancel = QPushButton('Cancel', self)
        self.btn_cancel.clicked.connect(self.close)

        hbox_top = QHBoxLayout()
        hbox_top.addStretch(1)
        hbox_top.addWidget(key_label)
        hbox_top.addWidget(self.choice_key)
        hbox_top.addStretch(1)

        hbox_central = QHBoxLayout()
        hbox_central.addStretch(1)
        hbox_central.addWidget(fields_label)
        hbox_central.addStretch(1)

        hbox_down = QHBoxLayout()
        hbox_down.addStretch(1)
        hbox_down.addWidget(self.btn_accept)
        hbox_down.addWidget(self.btn_cancel)
        hbox_down.addStretch(1)

        grid = QGridLayout()
        rows = int(len(self.data[0]) / 6) + 1
        positions = [(i, j) for i in range(rows) for j in range(6)]
        for position, button in zip(positions, self.buttons_field):
            grid.addWidget(button, *position)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_top)
        vbox.addStretch(50)
        vbox.addStretch(1)
        vbox.addLayout(hbox_central)
        vbox.addLayout(grid)
        vbox.addStretch(1)
        vbox.addStretch(50)
        vbox.addLayout(hbox_down)

        self.setLayout(vbox)

        self.setWindowTitle('Choice fields from input data')
        self.show()

    def closeEvent(self, event):  # pylint: disable=C0103
        """
        Before close dialog window ask 'Are you sure to quit?'.
        If self.is_close==True, dialog window close without this question
        """
        if self.is_close:
            event.accept()

        elif self.is_close is None:
            reply = QMessageBox.question(
                self, 'Message', 'Are you sure to quit?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

        else:
            QMessageBox.information(
                self, 'Message', 'There is not field of key in input data',
                QMessageBox.Ok
            )
            event.accept()

    def accept_clicked(self):
        """
        Accept selected fields and close dialog window
        """
        if self.key_field is None:
            self.parent.key_field = self.choice_key.currentText()

        lists_fields = [self.choice_key.currentText()]
        for item in self.buttons_field:
            if (item.isChecked() and
                    item.text() != self.choice_key.currentText()):
                lists_fields.append(item.text())
        self.parent.lists_fields[self.index] = lists_fields

        self.parent.dicts[self.index], error = utils.convert_csv_to_dict(
            self.data, self.choice_key.currentText(), lists_fields
        )
        self.parent.handle_error(error)
        if error is None:
            self.parent.generate_table(self.index, self.path)

        self.is_close = True
        self.close()

    def on_activated(self, text):
        """
        Choose one field as key-field
        """
        for item in self.buttons_field:
            if item.text() == text:
                item.setChecked(True)
                item.setDisabled(True)
            else:
                item.setDisabled(False)


class Compare(QWidget):
    """
    Class to show all data in workspace and processing all main actions
    """
    compareStatusbar = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.dicts = [None, None]
        self.small_dicts = [None, None]
        self.lists_fields = [None, None]
        self.key_field = None
        self.top_group_box = None
        self.btn_if1 = None
        self.btn_if2 = None
        self.btn_gen = None
        self.right_group_box = None
        self.item_combo_box = None
        self.different_fields = None
        self.value_combo_box = None
        self.delimiter_combo_box = None
        self.value_match_combo_box = None
        self.key_absent_combo_box = None
        self.columns_combo_box = None
        self.choice_window = None
        self.current_dir = os.curdir
        self.output_data = []
        self.group_boxes = []
        self.tables = []
        self.models = []
        self.settings = {}
        self.cache_settings = utils.CacheData()
        self.initUI()

    def initUI(self):  # pylint: disable=C0103
        """
        Init UI of workspace
        """
        QApplication.setStyle(QStyleFactory.create('Windows'))
        QApplication.setPalette(QApplication.style().standardPalette())

        self.create_top_group_box()
        self.create_tables_group_box()
        self.create_right_group_box()

        grid = QGridLayout()
        grid.addWidget(self.top_group_box, 0, 0, 1, 4)
        grid.addWidget(self.right_group_box, 0, 4, 3, 1)
        grid.addWidget(self.group_boxes[0], 1, 0, 1, 4)
        grid.addWidget(self.group_boxes[1], 2, 0, 1, 4)
        grid.addWidget(self.group_boxes[2], 3, 0, 1, 5)

        self.setLayout(grid)

        self.setWindowTitle('Compare files')
        self.show()

    def create_top_group_box(self):
        """
        Create group box with 3 buttons "Open First File", "Open Second File"
        and "Generate report"
        """
        self.top_group_box = QGroupBox('Input / Output')

        self.btn_if1 = QPushButton('&' + const.BUTTONS[0], self)
        self.btn_if2 = QPushButton('&' + const.BUTTONS[1], self)
        self.btn_gen = QPushButton('&' + const.BUTTONS[2], self)
        self.btn_gen.setDisabled(True)

        for btn in (self.btn_if1, self.btn_if2, self.btn_gen):
            btn.clicked.connect(self.button_clicked)

        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_if1)
        hbox.addWidget(self.btn_if2)
        hbox.addWidget(self.btn_gen)
        self.top_group_box.setLayout(hbox)

    def create_tables_group_box(self):
        """
        Create tables group box with 11 items from dictionaries or result
        for example on workspace
        """
        for index in range(0, 3):
            group_box = QGroupBox('')
            table = QTableView()
            model = TableModel([[]])

            if index == 2:
                group_box.setTitle('Result')
            table.verticalHeader().setDefaultSectionSize(5)
            table.setModel(model)
            hbox = QHBoxLayout()
            hbox.addWidget(table)
            group_box.setLayout(hbox)

            self.group_boxes.append(group_box)
            self.tables.append(table)
            self.models.append(model)

    def create_right_group_box(self):
        """
        Create right group box - 'Settings' on workspace
        """
        self.right_group_box = QGroupBox('Settings')

        item_label = QLabel('Include Item to Result if Item present in:')
        self.item_combo_box = QComboBox()
        self.item_combo_box.addItems(const.VARIANTS_ITEMS)
        self.item_combo_box.activated.connect(self.change_settings)

        self.different_fields = QPushButton("Include field 'different_fields'",
                                           self)
        self.different_fields.setCheckable(True)
        self.different_fields.setChecked(True)
        self.different_fields.clicked.connect(self.change_settings)

        value_label = QLabel('Action if values are different:')
        self.value_combo_box = QComboBox()
        self.value_combo_box.addItems(const.VARIANTS_VAL)
        self.value_combo_box.activated.connect(self.change_settings)

        delimiter_label = QLabel('Delimiter between different values:')
        self.delimiter_combo_box = QComboBox()
        self.delimiter_combo_box.addItems(const.VARIANTS_DELIMIT)
        self.delimiter_combo_box.activated.connect(self.change_settings)

        value_match_label = QLabel('Action if values are match:')
        self.value_match_combo_box = QComboBox()
        self.value_match_combo_box.addItems(const.VARIANTS_VAL_MATH)
        self.value_match_combo_box.activated.connect(self.change_settings)

        key_absent_label = QLabel('Action if key is absent for current item:')
        self.key_absent_combo_box = QComboBox()
        self.key_absent_combo_box.addItems(const.VARIANTS_KEY_ABSENT)
        self.key_absent_combo_box.activated.connect(self.change_settings)

        columns_label = QLabel('Columns include to report from:')
        self.columns_combo_box = QComboBox()
        self.columns_combo_box.addItems(const.VARIANTS_COLUMNS)
        self.columns_combo_box.activated.connect(self.change_settings)

        vbox = QVBoxLayout()
        vbox.addWidget(item_label)
        vbox.addWidget(self.item_combo_box)
        vbox.addStretch(1)
        vbox.addWidget(self.different_fields)
        vbox.addStretch(1)
        vbox.addWidget(value_label)
        vbox.addWidget(self.value_combo_box)
        vbox.addStretch(1)
        vbox.addWidget(delimiter_label)
        vbox.addWidget(self.delimiter_combo_box)
        vbox.addStretch(1)
        vbox.addWidget(value_match_label)
        vbox.addWidget(self.value_match_combo_box)
        vbox.addStretch(1)
        vbox.addWidget(key_absent_label)
        vbox.addWidget(self.key_absent_combo_box)
        vbox.addStretch(1)
        vbox.addWidget(columns_label)
        vbox.addWidget(self.columns_combo_box)

        self.right_group_box.setLayout(vbox)
        self.change_settings()

    def set_settings(self):
        """
        Set settings from Cache Settings if selected Undo or Redo operation.
        Call set_result() to generate table with 11 items from result if
        there are data in both dictionaries
        """
        sender = self.sender()

        if sender.text() == const.UNDO_REDO[0]:
            new_settings = self.cache_settings.undo()
        else:
            new_settings = self.cache_settings.redo()

        if new_settings:
            self.settings = new_settings

            self.item_combo_box.setCurrentIndex(
                self.settings[const.ITEMS])
            self.different_fields.setChecked(
                self.settings[const.DIFFERENT_FIELDS])
            self.value_combo_box.setCurrentIndex(
                self.settings[const.VALUES_DIFFERENT])
            self.delimiter_combo_box.setCurrentIndex(
                self.settings[const.DELIMITER])
            self.value_match_combo_box.setCurrentIndex(
                self.settings[const.VALUES_MATH])
            self.key_absent_combo_box.setCurrentIndex(
                self.settings[const.ABSENT])
            self.columns_combo_box.setCurrentIndex(
                self.settings[const.COLUMNS])

            if self.small_dicts[0] and self.small_dicts[1]:
                self.set_result()

            if sender.text() == const.UNDO_REDO[0]:
                self.parent().redo_action.setDisabled(False)
                if self.cache_settings.is_undo():
                    self.parent().undo_action.setDisabled(False)
                else:
                    self.parent().undo_action.setDisabled(True)

            else:
                self.parent().undo_action.setDisabled(False)
                if self.cache_settings.is_redo():
                    self.parent().redo_action.setDisabled(False)
                else:
                    self.parent().redo_action.setDisabled(True)

    def change_settings(self):
        """
        Get all settings and append there in Cache Settings.
        Call set_result() to generate table with 11 items from result if
        there are data in both dictionaries
        """
        self.settings = {
            const.ITEMS: self.item_combo_box.currentIndex(),
            const.DIFFERENT_FIELDS: self.different_fields.isChecked(),
            const.VALUES_DIFFERENT: self.value_combo_box.currentIndex(),
            const.DELIMITER: self.delimiter_combo_box.currentIndex(),
            const.VALUES_MATH: self.value_match_combo_box.currentIndex(),
            const.ABSENT: self.key_absent_combo_box.currentIndex(),
            const.COLUMNS: self.columns_combo_box.currentIndex(),
            const.FIELDS: self.lists_fields
        }

        self.cache_settings.append(self.settings)
        if self.parent():
            self.parent().undo_action.setDisabled(False)
            self.parent().redo_action.setDisabled(True)

        if self.small_dicts[0] and self.small_dicts[1]:
            self.set_result()

    def file_dialog(self, directory='', for_open=True, fmt=''):
        """
        Show and serving dialog window to work with files.
        Return path of selected file
        """
        path = ''

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons
        dialog = QFileDialog()
        dialog.setOptions(options)

        # OPENING OR SAVING
        if for_open:
            dialog.setAcceptMode(QFileDialog.AcceptOpen)
        else:
            dialog.setAcceptMode(QFileDialog.AcceptSave)

        # SET FORMAT, IF SPECIFIED
        if fmt != '':
            if len(fmt.split(', ')) > 1:
                file_filter = [f'{x} (*.{x})' for x in fmt.split(', ')]
            else:
                file_filter = [f'{fmt} (*.{fmt})']
            dialog.setDefaultSuffix(fmt)
            dialog.setNameFilters(file_filter)

        # SET THE STARTING DIRECTORY
        if directory != '':
            dialog.setDirectory(str(directory))
        else:
            dialog.setDirectory(str(self.current_dir))

        if dialog.exec_() == QDialog.Accepted:
            path = dialog.selectedFiles()[0]  # returns a list

            self.current_dir = os.path.dirname(path)

        return path

    def set_result(self, data=None):
        """
        Generate table on workspace with 11 items from result
        """
        if data is None:
            data = utils.generate_report(self.small_dicts, self.settings,
                                         self.key_field)
        self.models[-1] = TableModel(data)
        self.tables[-1].setModel(self.models[-1])

    def handle_error(self, error=None, no_error=const.COMPLETED):
        """
        Show error in Status Bar on main window after action if there is an
        error or show 'Completed'
        """
        if error is not None:
            self.compareStatusbar.emit(error)
        else:
            self.compareStatusbar.emit(no_error)

    def generate_table(self, index, path):
        """
        Generate table on workspace 11 items from one of the dictionaries and
        call set_result() to generate table with 11 items from result if
        there are data in both dictionaries
        """
        if path:
            self.small_dicts = utils.create_small_dicts(self.dicts)
            data = utils.dict_to_table(self.small_dicts[index],
                                       self.lists_fields[index])
            if index == 0:
                self.parent().clear_first_file.setDisabled(False)
            else:
                self.parent().clear_second_file.setDisabled(False)
        else:
            self.small_dicts[index] = None
            data = [[]]
            if index == 0:
                self.parent().clear_first_file.setDisabled(True)
            else:
                self.parent().clear_second_file.setDisabled(True)

        self.group_boxes[index].setTitle(path)
        self.models[index] = TableModel(data)
        self.tables[index].setModel(self.models[index])

        if self.small_dicts[0] and self.small_dicts[1]:
            self.set_result()
            self.btn_gen.setDisabled(False)
            self.parent().generate_action.setDisabled(False)
        else:
            self.set_result([[]])
            self.btn_gen.setDisabled(True)
            self.parent().generate_action.setDisabled(True)

    def button_clicked(self):
        """
        Serving one of the events: "Open First File", "Open Second File" or
        "Generate report"
        """
        sender = self.sender()

        if sender.text().strip('&') in (const.BUTTONS[0], const.BUTTONS[1]):
            index = 0 if sender.text().strip('&') == const.BUTTONS[0] else 1
            path = self.file_dialog(fmt=f'{const.CSV}')
            input_data, error = utils.load_data(path)
            self.handle_error(error)

            if input_data:
                self.choice_window = ChoiceFields(self, input_data, index,
                                                  path, self.key_field)

        elif sender.text().strip('&') == const.BUTTONS[2]:
            path = self.file_dialog(for_open=False, fmt=const.CSV)
            if not path:
                self.handle_error(const.ERROR_PATH)
                return

            self.output_data = utils.generate_report(
                self.dicts, self.settings, self.key_field
            )
            if len(self.output_data) > 1:
                error = utils.save_data(path, self.output_data)
                self.handle_error(error)
                QMessageBox.information(
                  self, 'Message', 'Generate complete', QMessageBox.Ok
                )
            else:
                QMessageBox.information(
                  self, 'Message', 'Output data is empty', QMessageBox.Ok
                )

        if self.group_boxes[0].title() and self.group_boxes[1].title():
            self.btn_gen.setDisabled(False)
            self.parent().generate_action.setDisabled(False)

            if self.small_dicts[0] and self.small_dicts[1]:
                self.set_result()

    def clear_data(self):
        """
        Clear one of the dictionaries and show empty table on workspace
        """
        sender = self.sender()

        index = 0 if sender.text() == const.CLEAR_BUTTONS[0] else 1
        self.dicts[index] = None
        self.generate_table(index, '')

        if not (self.dicts[0] or self.dicts[1]):
            self.key_field = None


if __name__ == '__main__':
    app = QApplication([])
    compare = Main()
    sys.exit(app.exec_())
