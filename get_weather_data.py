from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QDesktopWidget

class DownloadDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Downloading...")
        self.setGeometry(100, 100, 350, 70)

        # Main Widget and Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        self.label = QLabel("Downloading next 24 hours data, hang tight!!!")
        self.label.setStyleSheet("""
                       QLabel {
                           text-align: center;
                           width: 200px;
                           margin-left: auto;
                           margin-right: auto;
                       }
                   """)
        self.layout.addWidget(self.label)

        self.central_widget.setLayout(self.layout)
        self.setFixedSize(self.size())

        # Center the window
        self.center()

    def center(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
