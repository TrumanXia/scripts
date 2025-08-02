import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QWidget, QLabel,
                            QFileDialog, QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SimpleTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # 设置窗口基本属性
        self.setWindowTitle('Windows小工具示例')
        self.setGeometry(300, 300, 600, 400)
        
        # 创建中心部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 添加标题
        title_label = QLabel('简易文件处理器')
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 添加按钮区域
        button_layout = QHBoxLayout()
        
        self.open_btn = QPushButton('打开文件')
        self.open_btn.clicked.connect(self.open_file)
        
        self.process_btn = QPushButton('处理文件')
        self.process_btn.clicked.connect(self.process_file)
        self.process_btn.setEnabled(False)
        
        self.save_btn = QPushButton('保存结果')
        self.save_btn.clicked.connect(self.save_file)
        self.save_btn.setEnabled(False)
        
        button_layout.addWidget(self.open_btn)
        button_layout.addWidget(self.process_btn)
        button_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(button_layout)
        
        # 添加文本显示区域
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText('请打开一个文件...')
        main_layout.addWidget(self.text_edit)
        
        # 状态栏
        self.statusBar().showMessage('就绪')
        
        # 存储当前文件路径
        self.current_file = None
        
    def open_file(self):
        """打开文件对话框并读取文件内容"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, '打开文件', '', '文本文件 (*.txt);;所有文件 (*)'
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.text_edit.setText(content)
                    self.current_file = file_path
                    self.statusBar().showMessage(f'已打开: {os.path.basename(file_path)}')
                    self.process_btn.setEnabled(True)
                    self.save_btn.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, '错误', f'打开文件失败: {str(e)}')
    
    def process_file(self):
        """处理文件内容（示例：转为大写）"""
        if not self.current_file:
            return
            
        content = self.text_edit.toPlainText()
        # 简单处理：转为大写
        processed_content = content.upper()
        self.text_edit.setText(processed_content)
        self.statusBar().showMessage('文件处理完成')
    
    def save_file(self):
        """保存处理后的内容"""
        if not self.current_file:
            return
            
        content = self.text_edit.toPlainText()
        try:
            # 可以改为另存为对话框
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(content)
            self.statusBar().showMessage(f'已保存: {os.path.basename(self.current_file)}')
            QMessageBox.information(self, '成功', '文件保存成功')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'保存文件失败: {str(e)}')

if __name__ == '__main__':
    # 确保中文显示正常
    app = QApplication(sys.argv)
    
    # 可以设置全局字体
    font = QFont("SimHei")
    app.setFont(font)
    
    window = SimpleTool()
    window.show()
    sys.exit(app.exec_())
