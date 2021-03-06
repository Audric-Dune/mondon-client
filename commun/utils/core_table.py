from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QAbstractItemView
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant, pyqtSignal


class Table(QWidget):
    mouse_double_click_signal = pyqtSignal(int)

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

        self.table_view = TableView(parent=self)
        self.table_view.mouse_double_click_signal.connect(self.handle_mouse_double_click)
        self.table_view.verticalHeader().hide()
        self.table_view.horizontalHeader().hide()
        self.table_view.setShowGrid(False)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.table_view.setModel(self.model)
        for i, column in enumerate(self.model.get_columns()):
            self.table_view.setColumnWidth(i, self.model.get_column_width(column))

        vbox.setSpacing(0)
        vbox.addWidget(self.table_view, 1)
        self.setLayout(vbox)

    def refresh(self):
        self.model.refresh()
        self.table_view.refresh_ui()

    def handle_mouse_double_click(self, index):
        self.mouse_double_click_signal.emit(index)


class TableView(QTableView):
    mouse_double_click_signal = pyqtSignal(int)

    def __init__(self, parent):
        super(TableView, self).__init__(parent=parent)

    def refresh_ui(self):
        self.update()
        self.setVisible(False)
        self.setVisible(True)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        index_double_click = self.selectionModel().currentIndex().row()
        self.mouse_double_click_signal.emit(index_double_click)
        self.refresh_ui()


class TableModel(QAbstractTableModel):
    def __init__(self):
        super(TableModel, self).__init__()
        self.elements = []

    # Fonction à redéfinir dans les classe enfantes

    def get_elements(self):
        return self.elements

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
        return len(self.elements)

    def columnCount(self, parent):
        return len(self.get_columns())

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        element = self.elements[index.row()]
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
