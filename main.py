import sys
import time
import threading
import pyautogui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from pyautogui import ImageNotFoundException

MODES = {
    "Farm": {"command": "$map", "main_image": "img/combat.png", "secondary_image": "img/map.png", "message": "Honedge: Hell yeah time to genocide these little bitches"},
    "Mining": {"command": "$mining", "main_image": "img/pick.png", "secondary_image": "img/mine.png", "message": "Honedge: Oh so now Im a pickaxe and not a sword?"},
    "Foraging": {"command": "$forage", "main_image": "img/grab.png", "secondary_image": "img/forage.png", "message": "Honedge: What's next? I'm going to harvest Cottonees?"},
}

running = False

def locate(imagem, conf=0.72):
    try:
        pos = pyautogui.locateCenterOnScreen(imagem, confidence=conf)
        if pos:
            pyautogui.click(pos)
            return True
        return False
    except ImageNotFoundException:
        return False

def refresh(comando):
    pyautogui.write(comando)
    pyautogui.press('enter')
    time.sleep(1.5)

def bot_loop(config, update_status):
    global running
    running = True
    update_status(config["message"])

    while running:
        start = time.time()
        found = False

        while time.time() - start < 10:
            if not running:
                return
            if locate(config["main_image"]):
                found = True
                break
            time.sleep(0.5)

        if not found:
            refresh(config["command"])
            time.sleep(1)
            locate(config["secondary_image"])

            start = time.time()
            while time.time() - start < 10:
                if not running:
                    return
                if locate(config["main_image"]):
                    found = True
                    break
                time.sleep(0.5)

            if not found:
                update_status(f"I can't see '{config['main_image']}' anywhere. I'm done.")
                running = False
                return

        time.sleep(1)

    update_status("Stopped.")

class Honedge(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(300, 300)
        self.setWindowTitle('Honedge')
        self.setWindowIcon(QIcon('img/honedge.ico'))
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        for mode in MODES:
            btn = QPushButton(mode)
            btn.clicked.connect(lambda _, m=mode: self.start_bot(m))
            btn.setFixedSize(QSize(250, 40))
            btn.setStyleSheet("background-color: #333; color: white; font-size: 14px;")
            layout.addWidget(btn, alignment=Qt.AlignHCenter)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_bot)
        self.stop_btn.setFixedSize(QSize(250, 40))
        self.stop_btn.setStyleSheet("background-color: #aa0000; color: white; font-size: 14px;")
        layout.addWidget(self.stop_btn, alignment=Qt.AlignHCenter)

        self.status_label = QLabel("Choose a function!")
        self.status_label.setWordWrap(True)
        self.status_label.setFixedWidth(280)
        self.status_label.setStyleSheet("font-size: 14px; padding: 10px;")
        layout.addWidget(self.status_label, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def update_status(self, message):
        self.status_label.setText(message)

    def start_bot(self, mode_name):
        if running:
            self.update_status("Honedge: WAAAIT YOU FUCKER, IM WORKING HERE")
            return

        config = MODES[mode_name]
        thread = threading.Thread(target=bot_loop, args=(config, self.update_status), daemon=True)
        thread.start()

    def stop_bot(self):
        global running
        running = False
        self.update_status("Honedge: Finally some rest.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Honedge()
    window.show()
    sys.exit(app.exec_())