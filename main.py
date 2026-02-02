import sys
import os
import shutil
import platform

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QFileDialog,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QCheckBox, QMessageBox, QProgressBar
)
from PySide6.QtCore import Qt, QThread, Signal

from mahoyo_extractor import Extractor
from replacer import Replacer, metric, romanization, name_order, honorifics

# -----------------------
# Constants
# -----------------------
HFA_NAME = "data00200"
HFA_REL_PATH = f"{HFA_NAME}.hfa"
STEAM_APP_ID = "2052410"

EN_SCRIPT = 0
JP_SCRIPT = 1

EN_TXT = "extracted/script_en.txt"
JP_TXT = "extracted/script_jp.txt"
OUT_TXT = "extracted/script_en_patched.txt"

APP_ICON = "icon.ico"

# -----------------------
# Helper: Resource Path
# -----------------------
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# -----------------------
# Helper: Auto-detect
# -----------------------
def autodetect_game_path():
    """Attempts to find the game installation path via Windows Registry."""
    if platform.system() != "Windows":
        return None

    import winreg

    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App " + STEAM_APP_ID,
        r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Steam App " + STEAM_APP_ID
    ]

    for reg_path in reg_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                install_loc, _ = winreg.QueryValueEx(key, "InstallLocation")
                if os.path.isdir(install_loc):
                    return install_loc
        except Exception:
            continue

    return None


# -----------------------
# Worker Thread
# -----------------------
class PatchWorker(QThread):
    progress_signal = Signal(int)
    status_signal = Signal(str)
    finished_signal = Signal(bool, str)

    def __init__(self, game_dir, hfa_path, options):
        super().__init__()
        self.game_dir = game_dir
        self.hfa_path = hfa_path
        self.options = options

    def run(self):
        try:
            # --- Step 1: Backup ---
            self.status_signal.emit("Backing up HFA file...")
            self.progress_signal.emit(5)
            self.backup_hfa()

            # --- Step 2: Extraction ---
            self.status_signal.emit("Extracting scripts...")
            extractor = Extractor(self.game_dir, HFA_NAME)

            extractor.extract(EN_SCRIPT, EN_TXT)
            self.progress_signal.emit(15)

            extractor.extract(JP_SCRIPT, JP_TXT)
            self.progress_signal.emit(25)

            # --- Step 3: Loading Text ---
            self.status_signal.emit("Loading text files...")
            replacer_en = Replacer(self.game_dir, EN_TXT, OUT_TXT)
            replacer_jp = Replacer(self.game_dir, JP_TXT, JP_TXT)

            text_en = replacer_en.get_script()
            text_jp = replacer_jp.get_script()
            self.progress_signal.emit(35)

            # --- Step 4: Applying Patches ---
            self.status_signal.emit("Processing text...")

            if self.options['metric']:
                text_en = metric(text_en)
                self.progress_signal.emit(45)

            if self.options['romanization']:
                text_en = romanization(text_en)
                self.progress_signal.emit(55)

            if self.options['name_order']:
                text_en = name_order(text_en)
                self.progress_signal.emit(65)

            if self.options['honorifics']:
                self.status_signal.emit("Applying honorifics (this may take a moment)...")
                text_en = honorifics(text_en, text_jp)
                self.progress_signal.emit(85)

            # --- Step 5: Saving & Injecting ---
            self.status_signal.emit("Saving and injecting...")
            replacer_en.set_script(text_en)
            self.progress_signal.emit(95)

            extractor.inject(EN_SCRIPT, OUT_TXT)

            # --- Step 6: Cleanup ---
            self.status_signal.emit("Cleaning up temporary files...")
            temp_folder = os.path.join(self.game_dir, "extracted")
            if os.path.exists(temp_folder):
                shutil.rmtree(temp_folder)

            self.progress_signal.emit(100)
            self.finished_signal.emit(True, "Patch applied successfully!")

        except Exception as e:
            self.finished_signal.emit(False, str(e))

    def backup_hfa(self):
        bak_path = self.hfa_path + ".bak"
        if not os.path.exists(bak_path):
            shutil.copy2(self.hfa_path, bak_path)


# -----------------------
# Main Window
# -----------------------
class PatchWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mahoyo Patcher")
        self.setMinimumWidth(480)

        # --- NEW ICON CODE ---
        # Look for the icon using the resource_path helper
        icon_path = resource_path(APP_ICON)
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        # ---------------------

        self.game_dir = None
        self.hfa_path = None
        self.worker = None

        self._build_ui()
        self._connect_signals()

        self.try_autodetect()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # 1. Path Display (Label)
        # Added border and padding to make it look like a text box
        self.folder_label = QLabel("No game folder selected")
        self.folder_label.setWordWrap(True)
        self.folder_label.setAlignment(Qt.AlignCenter)
        self.folder_label.setStyleSheet(
            "border: 1px solid #aaa; padding: 5px; background: #f0f0f0; border-radius: 4px;")
        layout.addWidget(self.folder_label)

        # 2. Select Button (Underneath)
        self.select_folder_btn = QPushButton("Select game folder")
        layout.addWidget(self.select_folder_btn)

        # Separator line
        line = QLabel("Options")
        line.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(line)

        # Checkboxes
        self.metric_cb = QCheckBox("Metric System")
        self.romanization_cb = QCheckBox("Fix Romanization")
        self.name_order_cb = QCheckBox("Fix Name Order")
        self.honorifics_cb = QCheckBox("Restore Honorifics")

        self.name_order_cb.setEnabled(False)
        self.honorifics_cb.setEnabled(False)

        layout.addWidget(self.metric_cb)
        layout.addWidget(self.romanization_cb)
        layout.addWidget(self.name_order_cb)
        layout.addWidget(self.honorifics_cb)

        # Progress Bar
        self.progress_label = QLabel("")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("margin-top: 10px;")
        layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Patch button
        self.patch_btn = QPushButton("Patch!")
        self.patch_btn.setEnabled(False)
        self.patch_btn.setMinimumHeight(40)  # Make it a bit bigger
        layout.addWidget(self.patch_btn)

    def _connect_signals(self):
        self.select_folder_btn.clicked.connect(self.manual_select_folder)
        self.romanization_cb.toggled.connect(self.on_romanization_toggled)
        self.name_order_cb.toggled.connect(self.on_name_order_toggled)
        self.patch_btn.clicked.connect(self.run_patch)

    def try_autodetect(self):
        path = autodetect_game_path()
        if path:
            self.validate_and_set_path(path)

    def manual_select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select main game folder")
        if folder:
            self.validate_and_set_path(folder)

    def validate_and_set_path(self, folder):
        self.game_dir = folder
        self.folder_label.setText(folder)

        candidate = os.path.join(folder, HFA_REL_PATH)

        if not os.path.isfile(candidate):
            self.patch_btn.setEnabled(False)
            if self.sender() == self.select_folder_btn:
                QMessageBox.critical(self, "File not found", f"Could not find:\n\n{HFA_REL_PATH}")
            return

        self.hfa_path = candidate
        self.patch_btn.setEnabled(True)

    def on_romanization_toggled(self, checked):
        self.name_order_cb.setEnabled(checked)
        if not checked:
            self.name_order_cb.setChecked(False)

    def on_name_order_toggled(self, checked):
        self.honorifics_cb.setEnabled(checked)
        if not checked:
            self.honorifics_cb.setChecked(False)

    def run_patch(self):
        options = {
            'metric': self.metric_cb.isChecked(),
            'romanization': self.romanization_cb.isChecked(),
            'name_order': self.name_order_cb.isChecked(),
            'honorifics': self.honorifics_cb.isChecked(),
        }

        self.patch_btn.setEnabled(False)
        self.select_folder_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_label.setText("Starting...")

        self.worker = PatchWorker(self.game_dir, self.hfa_path, options)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.status_signal.connect(self.update_status)
        self.worker.finished_signal.connect(self.on_patch_finished)
        self.worker.start()

    def update_progress(self, val):
        self.progress_bar.setValue(val)

    def update_status(self, text):
        self.progress_label.setText(text)

    def on_patch_finished(self, success, message):
        self.patch_btn.setEnabled(True)
        self.select_folder_btn.setEnabled(True)
        self.progress_label.setText("Done" if success else "Error")

        if success:
            QMessageBox.information(self, "Success", message)
            self.progress_bar.setVisible(False)
            self.progress_label.setText("")
        else:
            QMessageBox.critical(self, "Patch Failed", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PatchWindow()
    window.show()
    sys.exit(app.exec())