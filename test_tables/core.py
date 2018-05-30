from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableView,
    QHeaderView,
    QSizePolicy,
    QFrame,
    QAbstractItemView,
)
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, QSize, QPoint
from commun.ui.public.mondon_widget import MondonWidget



class Table(MondonWidget):
    def __init__(self, model, parent=None):
        super(Table, self).__init__(parent=parent)

        table_view = QTableView()
        table_view.verticalHeader().hide()
        table_view.horizontalHeader().hide()
        table_view.setShowGrid(False)
        table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_view.setSelectionMode(QAbstractItemView.SingleSelection)

        self.header_view = TestHeaderView(model, table_view)
        self.header_view.setFixedHeight(model.get_column_height())

        table_view.setModel(model)
        for i, column in enumerate(model.get_columns()):
            table_view.setColumnWidth(i, model.get_column_width(column))

        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.addWidget(self.header_view, 0)
        vbox.addWidget(table_view, 1)
        self.setLayout(vbox)


class TestHeaderView(QWidget):
    def __init__(self, model, parent):
        super(TestHeaderView, self).__init__(parent)
        column_height = model.get_column_height()
        column_x = 0
        for column in model.get_columns():
            column_width = model.get_column_width(column)
            column_widget = model.get_column_widget(column)
            if column_widget:
                column_widget.setParent(self)
                column_widget.setGeometry(column_x, 0, column_width, column_height)
            column_x += column_width


class TableModel(QAbstractTableModel):
    def __init__(self):
        super(TableModel, self).__init__()

    def get_elements(self):
        return []

    def get_columns(self):
        return []

    def get_column_widget(self, column):
        return None

    def get_column_width(self, column):
        return 100

    def get_column_height(self):
        return 24

    def rowCount(self, parent):
        return len(self.get_elements())

    def columnCount(self, parent):
        return len(self.get_columns())

    def get_text(self, element, column):
        return ""

    def get_icon(self, element, column):
        return None

    def get_font(self, element, column):
        return None

    def get_alignment(self, element, column):
        return None

    def get_background_color(self, element, column):
        return None

    def get_color(self, element, column):
        return None

    def data(self, index, role):
        if not index.isValid():
            print('invalid index {}'.format(index))
            return QVariant()
        element = self.get_elements()[index.row()]
        column = self.get_columns()[index.column()]

        if role == Qt.DisplayRole:
            return QVariant(self.get_text(element, column))

        if role == Qt.DecorationRole:
            return QVariant(self.get_icon(element, column))

        if role == Qt.FontRole:
            return QVariant(self.get_font(element, column))

        if role == Qt.TextAlignmentRole:
            return QVariant(self.get_alignment(element, column))

        if role == Qt.BackgroundRole:
            return QVariant(self.get_background_color(element, column))

        if role == Qt.ForegroundRole:
            return QVariant(self.get_color(element, column))

        if role in (Qt.EditRole, Qt.ToolTipRole, Qt.StatusTipRole, Qt.WhatsThisRole, Qt.CheckStateRole):
            return QVariant()

        print('invalid role {}'.format(role))
        return QVariant()

    def headerData(self, section, orientation, role):
        if orientation == Qt.Vertical:
            return QVariant()
        column = self.get_columns()[section]
        if role == Qt.DisplayRole:
            return column
        print('headerData(section={}, role={})'.format(section, orientation, role))
        return None
