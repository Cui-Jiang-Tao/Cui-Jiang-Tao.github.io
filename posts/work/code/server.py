from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMenu, QLabel
import sys
import sqlite3
import uuid

from PyQt5.QtGui import QBrush, QColor, QStandardItem
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox


class NewTableWidget(QtWidgets.QWidget):

    def __init__(self, lst):
        super().__init__()
        self.sql = simpleToolSql("test")
        self.order_flag = True
        self.oldVal = ''
        self.cur_update_row = -1
        self.change_value_flag = True

        self.resize(1500, 800)
        # 全局布局：垂直
        self.wlayout = QtWidgets.QVBoxLayout(self)
        self.lst = lst
        self.newTableWidget()

    # 表格控件
    def newTableWidget(self):
        self.tableWidget_cn = QtWidgets.QTableWidget()
        self.tableWidget_en = QtWidgets.QTableWidget()
        self.tableWidget_add_cn = QtWidgets.QTableWidget()
        self.tableWidget_add_en = QtWidgets.QTableWidget()
        self.tableWidget_cn_show = QtWidgets.QTableWidget()
        self.tableWidget_en_show = QtWidgets.QTableWidget()

        self.initTableWidget(self.tableWidget_cn, True)
        self.initTableWidget(self.tableWidget_en, False)
        self.initOperateTableWidget(self.tableWidget_add_cn, self.tableWidget_cn, True)
        self.initOperateTableWidget(self.tableWidget_add_en, self.tableWidget_en, False)
        self.initSearchTableWidget(self.tableWidget_cn_show, True)
        self.initSearchTableWidget(self.tableWidget_en_show, False)

        menu_Hlayout = QtWidgets.QHBoxLayout()
        label_cn = QLabel('中文菜单')
        label_cn.setAlignment(Qt.AlignCenter)
        label_en = QLabel('英文菜单')
        label_en.setAlignment(Qt.AlignCenter)
        menu_Hlayout.addWidget(label_cn)
        menu_Hlayout.addWidget(label_en)

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(self.tableWidget_cn)
        hlayout.addWidget(self.tableWidget_en)

        addHlayout = QtWidgets.QHBoxLayout()
        addHlayout.addWidget(self.tableWidget_add_cn)
        addHlayout.addWidget(self.tableWidget_add_en)

        hlayout_show = QtWidgets.QHBoxLayout()
        hlayout_show.addWidget(self.tableWidget_cn_show)
        hlayout_show.addWidget(self.tableWidget_en_show)

        self.wlayout.addLayout(menu_Hlayout)
        self.wlayout.addLayout(hlayout)
        self.wlayout.addLayout(addHlayout)
        self.wlayout.addLayout(hlayout_show)
        self.wlayout.setStretch(0, 1)
        self.wlayout.setStretch(1, 30)
        self.wlayout.setStretch(2, 2)
        self.wlayout.setStretch(3, 10)

    def initTableWidget(self, tableWidget, isCN: bool):
        tableWidget.setColumnCount(len(self.lst))
        tableWidget.setHorizontalHeaderLabels(self.lst)
        tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # 使列表自适应宽度
        tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
        tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Interactive)

        tableWidget.verticalHeader().setHidden(True)
        # tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 设置tablewidget不可编辑
        # tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)  # 设置tablewidget不可选中
        # for i in range(100):
        #     tableWidget.setCellWidget(i, len(self.lst) - 1, self.buttonForRow(self.tableWidget))  # 在最后一个单元格中加入修改、删除按钮

        tableWidget.setShowGrid(False)

        tableWidget.cellChanged.connect(lambda: self.change_value(tableWidget))
        tableWidget.doubleClicked.connect(lambda: self.get_value(tableWidget))
        tableWidget.horizontalHeader().sectionClicked.connect(lambda: self.order(tableWidget))

        tableWidget.horizontalHeader().setStyleSheet(
            'color: rgb(0, 83, 128); border:1px solid rgb(210, 210, 210);')
        tableWidget.setStyleSheet('border: 1px solid #72e8dd; color: rgb(0, 83, 128);')

        if isCN:
            self.scrollBar_cn = tableWidget.verticalScrollBar()
            self.scrollBar_cn.valueChanged.connect(self.verticalScrollBarChanged)
        else:
            self.scrollBar_en = tableWidget.verticalScrollBar()
            self.scrollBar_en.valueChanged.connect(self.verticalScrollBarChanged)

        sql_str = "select * from IMMO_Menu_en order by id;"
        if isCN:
            sql_str = sql_str.replace('IMMO_Menu_en', 'IMMO_Menu_cn')
        res = self.sql.query(sql_str)
        for row in res:
            tableWidget.insertRow(tableWidget.rowCount())  # 先增加一列
            i = 0
            for clo in row:
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                if i == 0:
                    item.setData(Qt.DisplayRole, int(clo))
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                else:
                    item.setText(str(clo))
                tableWidget.setItem(tableWidget.rowCount() - 1, i, item)
                i += 1
            tableWidget.setCellWidget(tableWidget.rowCount() - 1, len(self.lst) - 1,
                                      self.buttonForRow(tableWidget, isCN))  # 在最后一个单元格中加入修改、删除按钮

    def initOperateTableWidget(self, tableWidget_operate, tableWidget, isCN: bool):
        new_list = ['uuid(默认为空即可)', '菜单名称', '操作']
        tableWidget_operate.setRowCount(1)
        tableWidget_operate.setColumnCount(len(new_list))
        tableWidget_operate.setHorizontalHeaderLabels(new_list)
        tableWidget_operate.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # 使列表自适应宽度
        tableWidget_operate.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Interactive)
        tableWidget_operate.verticalHeader().setHidden(True)
        for i in range(1):
            tableWidget_operate.setCellWidget(i, len(new_list) - 1,
                                              self.new_buttonForRow(tableWidget_operate,
                                                                    tableWidget,
                                                                    isCN))  # 在最后一个单元格中加入修改、删除按钮

        tableWidget_operate.horizontalHeader().setStyleSheet(
            'color: rgb(0, 83, 128); border:1px solid rgb(210, 210, 210);')
        tableWidget_operate.setStyleSheet('border: 1px solid #72e8dd; color: rgb(0, 83, 128);')

    def initSearchTableWidget(self, tableWidget, isCN: bool):
        new_list = ['id', 'uuid', '菜单名称']
        tableWidget.setColumnCount(len(new_list))
        tableWidget.setHorizontalHeaderLabels(new_list)
        tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # 使列表自适应宽度
        tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
        # tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Interactive)

        tableWidget.verticalHeader().setHidden(True)
        # tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 设置tablewidget不可编辑
        # tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)  # 设置tablewidget不可选中
        # for i in range(100):
        #     tableWidget.setCellWidget(i, len(self.lst) - 1, self.buttonForRow(self.tableWidget))  # 在最后一个单元格中加入修改、删除按钮

        tableWidget.setShowGrid(False)

        tableWidget.cellChanged.connect(lambda: self.change_value(tableWidget))
        tableWidget.doubleClicked.connect(lambda: self.get_value(tableWidget))
        tableWidget.horizontalHeader().sectionClicked.connect(lambda: self.order(tableWidget))

        tableWidget.horizontalHeader().setStyleSheet(
            'color: rgb(0, 83, 128); border:1px solid rgb(210, 210, 210);')
        tableWidget.setStyleSheet('border: 1px solid #72e8dd; color: rgb(0, 83, 128);')

        if isCN:
            self.scrollBar_show_cn = tableWidget.verticalScrollBar()
            self.scrollBar_show_cn.valueChanged.connect(self.verticalScrollBarChanged_show)
        else:
            self.scrollBar_show_en = tableWidget.verticalScrollBar()
            self.scrollBar_show_en.valueChanged.connect(self.verticalScrollBarChanged_show)

    def buttonForRow(self, tableWidget, isCN: bool):
        widget = QtWidgets.QWidget()
        # 修改
        self.updateBtn = QtWidgets.QPushButton('修改')
        self.updateBtn.setStyleSheet(''' text-align : center;
                                          background-color : NavajoWhite;
                                          height : 30px;
                                          border-style: outset;
                                          font : 13px  ''')
        self.updateBtn.clicked.connect(lambda: self.updateButton(tableWidget, isCN))

        # 删除
        self.deleteBtn = QtWidgets.QPushButton('删除')
        self.deleteBtn.setStyleSheet(''' text-align : center;
                                    background-color : LightCoral;
                                    height : 30px;
                                    border-style: outset;
                                    font : 13px; ''')
        self.deleteBtn.clicked.connect(lambda: self.delBtn(tableWidget, isCN))

        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(self.updateBtn)
        hLayout.addWidget(self.deleteBtn)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget

    def new_buttonForRow(self, tableWidget_add, tableWidget, isCN: bool):
        widget = QtWidgets.QWidget()
        # 增加
        self.addBtn = QtWidgets.QPushButton('增加')
        self.addBtn.setStyleSheet(''' text-align : center;
                                          background-color : NavajoWhite;
                                          height : 30px;
                                          border-style: outset;
                                          font : 13px  ''')
        self.addBtn.clicked.connect(lambda: self.addVal(tableWidget_add, tableWidget, isCN))

        # 增加
        self.searchBtn = QtWidgets.QPushButton('搜索')
        self.searchBtn.setStyleSheet(''' text-align : center;
                                                  background-color : NavajoWhite;
                                                  height : 30px;
                                                  border-style: outset;
                                                  font : 13px  ''')
        self.searchBtn.clicked.connect(lambda: self.search(tableWidget_add, isCN))

        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(self.addBtn)
        hLayout.addWidget(self.searchBtn)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget

    def verticalScrollBarChanged(self, e):
        self.scrollBar_cn.setValue(e)
        self.scrollBar_en.setValue(e)

    def verticalScrollBarChanged_show(self, e):
        self.scrollBar_show_cn.setValue(e)
        self.scrollBar_show_en.setValue(e)

    def delBtn(self, tableWidget, isCN: bool):
        button = self.sender()

        if button:
            # 确定位置的时候这里是关键
            row = tableWidget.indexAt(button.parent().pos()).row()
            clum = tableWidget.indexAt(button.parent().pos()).column()

            rs = QMessageBox.question(self, "提示", "是否删除该列？  id: " + tableWidget.item(row, 0).text())
            if rs == QMessageBox.StandardButton.No:
                return

            uuid_ = tableWidget.item(row, 1).text()
            tableWidget.removeRow(row)

            sql_str = "delete from IMMO_Menu_cn where uuid=?;"
            if not isCN:
                sql_str = sql_str.replace('IMMO_Menu_cn', 'IMMO_Menu_en')
            res = self.sql.execute(sql_str, (uuid_,))
            print(res)

            # print(clum)
            # QMessageBox.about(self, "提示", "删除成功！！！")

    def updateButton(self, tableWidget, isCN: bool):
        button = self.sender()
        col_num = tableWidget.columnCount()  # 获取当前表格共有多少列
        # self.tableWidget.rowCount()  # 获取当前表格共有多少行

        if button:
            row = tableWidget.indexAt(button.parent().pos()).row()
            rs = QMessageBox.question(self, "提示", "是否修改该行？  id: " + tableWidget.item(row, 0).text())
            if rs == QMessageBox.StandardButton.No:
                return

            self.change_value_flag = False
            self.cur_update_row = row

            line_content = list()
            # 确定位置的时候这里是关键
            for col in range(0, col_num - 1):
                line_content.append(tableWidget.item(row, col).text())

            if len(line_content[0]) <= 0 or len(line_content[1]) != 36 or len(line_content[2]) <= 0:
                QMessageBox.about(self, "错误",
                                  '字段信息错误：' + 'id: ' + line_content[0] + ' uuid: ' + line_content[
                                      1] + ' menu_name: ' + line_content[2])
                return

            for col in range(0, col_num - 1):
                if tableWidget.item(row, col):
                    tableWidget.item(row, col).setForeground(QBrush(QColor(0, 83, 128)))
            sql_str = "update IMMO_Menu_cn set uuid=?, menu_name=? where id=?;"
            if not isCN:
                sql_str = sql_str.replace('IMMO_Menu_cn', 'IMMO_Menu_en')
            res = self.sql.execute(sql_str, (line_content[1], line_content[2], line_content[0]))
            print(res)

    def change_value(self, tableWidget):
        if self.change_value_flag:
            for item in tableWidget.selectedItems():
                if self.cur_update_row == item.row():
                    # print(item.row(), item.column(), item.text())
                    if item.column() == 1:  # uuid列
                        uuid_ = item.text()
                        if len(uuid_) != 36:
                            QMessageBox.about(self, "错误", '字段信息错误：uuid: ' + uuid_)
                            tableWidget.item(item.row(), item.column()).setText(self.oldVal)
                            return

                    if tableWidget.item(item.row(), item.column()).text() != self.oldVal:
                        tableWidget.item(item.row(), item.column()).setForeground(QBrush(QColor(255, 0, 0)))

        self.change_value_flag = True

    def get_value(self, tableWidget):
        for item in tableWidget.selectedItems():
            self.oldVal = item.text()
            self.cur_update_row = item.row()

    def order(self, tableWidget):
        for item in tableWidget.selectedItems():
            print(item.text())
            if self.order_flag:
                tableWidget.sortItems(item.column(), Qt.DescendingOrder)
            else:
                tableWidget.sortItems(item.column(), Qt.AscendingOrder)
            self.order_flag = bool(1 - self.order_flag)
            break

    def addVal(self, tableWidget_add, tableWidget, isCN: bool):
        button = self.sender()
        col_num = tableWidget.columnCount()  # 获取当前表格共有多少列
        row_num = tableWidget.rowCount()  # 获取当前表格共有多少行

        if button:
            rs = QMessageBox.question(self, "提示", "是否增加该菜单字段？")
            if rs == QMessageBox.StandardButton.No:
                return

            # 确定位置的时候这里是关键
            row = tableWidget_add.indexAt(button.parent().pos()).row()
            tableWidget.insertRow(row_num)  # 先增加一行

            sql_str = 'select max(id) from IMMO_Menu_cn;'
            if not isCN:
                sql_str = sql_str.replace('IMMO_Menu_cn', 'IMMO_Menu_en')
            id_ = '1'
            try:
                id_ = str(int(self.sql.query(sql_str)[0][0]) + 1)
            except BaseException as e:
                print(e)
            uuid_ = ''
            menu_name = ''

            for col in range(0, tableWidget_add.columnCount() - 1):
                if tableWidget_add.item(row, col) and len(tableWidget_add.item(row, col).text().strip()) > 0:
                    if col == 0:
                        uuid_ = tableWidget_add.item(row, col).text()
                    else:
                        menu_name = tableWidget_add.item(row, col).text()

                    item = QTableWidgetItem(tableWidget_add.item(row, col))
                    item.setTextAlignment(Qt.AlignCenter)
                    tableWidget.setItem(row_num, col + 1, item)
                    tableWidget_add.item(row, col).setText('')
                elif col == 0:
                    uuid_ = str(uuid.uuid1())
                    item = QTableWidgetItem(uuid_)
                    item.setTextAlignment(Qt.AlignCenter)
                    tableWidget.setItem(row_num, col + 1, item)
            tableWidget.setCellWidget(row_num, len(self.lst) - 1, self.buttonForRow(tableWidget, isCN))
            item = QTableWidgetItem(id_)
            item.setData(Qt.DisplayRole, int(id_))
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            tableWidget.setItem(row_num, 0, item)

            if len(id_) <= 0 or len(uuid_) <= 0 or len(menu_name) <= 0:
                tableWidget.removeRow(row_num)
                QMessageBox.about(self, "错误",
                                  '字段信息错误：' + 'id: ' + id_ + ' uuid: ' + uuid_ + ' menu_name: ' + menu_name)
                return

            if len(uuid_) != 36:
                tableWidget.removeRow(row_num)
                QMessageBox.about(self, "错误", "uuid 长度要求为36！！！")
                return

            try:
                sql_str = "insert into IMMO_Menu_cn (id,uuid,menu_name) values (?,?,?);"
                if not isCN:
                    sql_str = sql_str.replace('IMMO_Menu_cn', 'IMMO_Menu_en')
                rs = self.sql.execute(sql_str, [(id_, uuid_, menu_name)])
                if not rs:
                    tableWidget.removeRow(row_num)
                    QMessageBox.about(self, "错误", "error！！！")
            except Exception as e:
                print('id: ', id_, ' uuid: ', uuid_, ' menu_name: ', menu_name)
                tableWidget.removeRow(row_num)
                QMessageBox.about(self, "错误",
                                  str(e) + '\n字段信息错误：' + 'id: ' + id_ + ', uuid: ' + uuid_ + ', menu_name: ' + menu_name)

    def search(self, tableWidget_operate, isCN: bool):
        button = self.sender()
        uuid_ = ''
        menu_name = ''

        uuid_s = list()

        if button:
            row = tableWidget_operate.indexAt(button.parent().pos()).row()
            for col in range(0, tableWidget_operate.columnCount() - 1):
                if tableWidget_operate.item(row, col) and len(tableWidget_operate.item(row, col).text().strip()) > 0:
                    if col == 0:
                        uuid_ = tableWidget_operate.item(row, col).text()
                    else:
                        menu_name = tableWidget_operate.item(row, col).text()
            sql_str_cn = "select * from IMMO_Menu_cn where uuid like '%%%%%s%%%%' and menu_name like '%%%%%s%%%%'" % (uuid_, menu_name)
            sql_str_en = "select * from IMMO_Menu_en where uuid like '%%%%%s%%%%' and menu_name like '%%%%%s%%%%'" % (uuid_, menu_name)

            tableWidget_show = self.tableWidget_cn_show
            if isCN:
                self.rs = self.sql.query(sql_str_cn)
            else:
                self.rs = self.sql.query(sql_str_en)
                tableWidget_show = self.tableWidget_en_show

            while True:
                rows = tableWidget_show.rowCount()  # 获取当前表格共有多少行
                if rows != 0:
                    tableWidget_show.removeRow(rows - 1)
                else:
                    break

            for row in self.rs:
                tableWidget_show.insertRow(tableWidget_show.rowCount())  # 先增加一行
                i = 0
                for clo in row:
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignCenter)

                    if i == 1:
                        uuid_s.append(str(clo))

                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    if i == 0:
                        item.setData(Qt.DisplayRole, int(clo))
                    else:
                        item.setText(str(clo))
                    tableWidget_show.setItem(tableWidget_show.rowCount() - 1, i, item)
                    i += 1

                # tableWidget_show.setCellWidget(tableWidget_show.rowCount() - 1, len(self.lst) - 1,
                #                           self.buttonForRow(tableWidget_show, isCN))  # 在最后一个单元格中加入修改、删除按钮

            print(self.rs)



class simpleToolSql():
    """
    simpleToolSql for sqlite3
    简单数据库工具类
    编写这个类主要是为了封装sqlite，继承此类复用方法
    """

    def __init__(self, filename="stsql"):
        """
        初始化数据库，默认文件名 stsql.db
        filename：文件名
        """
        self.filename = filename + ".db"
        self.db = sqlite3.connect(self.filename)
        self.c = self.db.cursor()

    def close(self):
        """
        关闭数据库
        """
        self.c.close()
        self.db.close()

    def execute(self, sql, param=None):
        """
        执行数据库的增、删、改
        sql：sql语句
        param：数据，可以是list或tuple，亦可是None
        retutn：成功返回True
        """
        try:
            if param is None:
                self.c.execute(sql)
            else:
                if type(param) is list:
                    self.c.executemany(sql, param)
                else:
                    self.c.execute(sql, param)
            count = self.db.total_changes
            self.db.commit()
        except Exception as e:
            print(e)
            raise e
            # return False, e
            # return False
        if count > 0:
            return True
        else:
            return False

    def query(self, sql, param=None):
        """
        查询语句
        sql：sql语句
        param：参数,可为None
        retutn：成功返回结果
        """
        if param is None:
            self.c.execute(sql)
        else:
            self.c.execute(sql, param)
        return self.c.fetchall()

    # def set(self,table,field=" * ",where="",isWhere=False):
    #     self.table = table
    #     self.filed = field
    #     if where != "" :
    #         self.where = where
    #         self.isWhere = True
    #     return True


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    lst = ['id', 'uuid', '菜单名称', '操作']
    win = NewTableWidget(lst)
    app.setWindowIcon(QtGui.QIcon('img/system.png'))
    win.show()
    sys.exit(app.exec_())
