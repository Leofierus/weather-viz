import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from threading import Thread

from get_coordinates import run_flask


class LatLngSender(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTML + PyQt5 Example")

        # Set up layout
        layout = QVBoxLayout()
        self.label = QLabel("HTML Integration with Flask and PyQt5")
        layout.addWidget(self.label)

        # Embedded browser
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:5000"))  # Flask's index.html
        layout.addWidget(self.browser)

        # Container widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.setDaemon(True)
    flask_thread.start()

    # Start PyQt5 application
    app = QApplication(sys.argv)
    window = LatLngSender()
    window.show()
    sys.exit(app.exec_())
