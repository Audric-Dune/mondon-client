from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QAbstractItemView
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from commun.ui.public.mondon_widget import MondonWidget


class Table(MondonWidget):
    def __init__(self, model, parent=None):
        """
        Crée une nouvelle table
        :param model: Un object héritant de TableModel
        :param parent: Parent du widget
        :return: Un widget qui affiche des données définit par `model`
        """
        super(Table, self).__init__(parent=parent)
        self.model = model
        vbox = QVBoxLayout()

        self.table_view = QTableView(parent=self)
        self.table_view.verticalHeader().hide()
        self.table_view.horizontalHeader().hide()
        self.table_view.setShowGrid(False)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)

        self.header_view = TestHeaderView(self.model, parent=self)
        self.header_view.setFixedHeight(self.model.get_column_height())

        self.table_view.setModel(self.model)
        for i, column in enumerate(self.model.get_columns()):
            self.table_view.setColumnWidth(i, self.model.get_column_width(column))

        vbox.setSpacing(0)
        vbox.addWidget(self.header_view, 0)
        vbox.addWidget(self.table_view, 1)
        self.setLayout(vbox)

    def set_filter(self, filter_fn):
        """
        Filtre les éléments affichés dans la table
        :param filter_fn: Fonction prenant en paramêtre un élément et retourne si il doit être
          affiché (True) ou caché (False)
        """
        for index, element in enumerate(self.model.get_elements()):
            self.table_view.setRowHidden(index, not filter_fn(element))


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


    # Fonction à redéfinir dans les classe enfantes

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


    # Fonction interne utilisé par la QTableView

    def rowCount(self, parent):
        return len(self.get_elements())

    def columnCount(self, parent):
        return len(self.get_columns())

    def data(self, index, role):
        if not index.isValid():
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
        return QVariant()
