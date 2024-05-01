from pathlib import Path
from functools import partial

from PyQt6.QtWidgets import (
    QDialog, QWidget, QLabel, QLineEdit, QPushButton,
    QCheckBox, QVBoxLayout, QHBoxLayout, QFileDialog
)

from neat.genome import Genome

class LoadDialog(QDialog):
    """Dialog box that enables the user to create a new GenomeWidget from a saved Genome."""

    def __init__(self, enforced: bool, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Load")

        self.file_path_label = QLabel("Path to Genome:")
        self.file_path_label.setGeometry(0, 0, 200, 20)

        self.file_path = QLineEdit()
        self.file_path.setGeometry(0, 20, 200, 20)

        self.browse = QPushButton("Browse")
        self.browse.clicked.connect(self.browse_clicked)
        self.browse.setGeometry(220, 20, 60, 20)

        self.warning_label = QLabel("")

        self.new_window = QCheckBox("Create in new window")
        self.new_window.setChecked(True)
        self.new_window.toggled.connect(partial(self.new_window_toggle, enforced))

        self.cancel = QPushButton("Cancel")
        self.cancel.clicked.connect(self.cancel_clicked)
        self.load = QPushButton("Load")
        self.load.clicked.connect(self.load_clicked)
        self.load.setEnabled(False)


        layout = QVBoxLayout()
        layout.setSpacing(0)
        file_path_layout = QHBoxLayout()
        file_path_layout.addWidget(self.file_path)
        file_path_layout.addWidget(self.browse)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel)
        button_layout.addWidget(self.load)
        layout.addWidget(self.file_path_label)
        layout.addLayout(file_path_layout)
        layout.addWidget(self.warning_label)
        layout.addStretch()
        layout.addWidget(self.new_window)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.setFixedSize(400, 120)

    def browse_clicked(self) -> None:
        """Open a QFileDialog for the user to choose a Genome to load."""

        f_dlg = QFileDialog()
        f_dlg.setNameFilter("Pickle files (*.pickle)")

        if f_dlg.exec():
            path = f_dlg.selectedFiles()[0]
            self.file_path.setText(path)

            try:
                self.loaded_genome = Genome.load(Path(path))
                self.warning_label.setText("")
                self.load.setEnabled(True)
            except (OSError, EOFError):
                self.warning_label.setText("Provided file does not contain a valid Genome.")
                self.load.setEnabled(False)

    def new_window_toggle(self, enforced: bool) -> None:
        """Allow the user to create the new GenomeWidget in the same window only if it wasn't enforced
        that it had to be a new window."""

        if enforced and not self.new_window.isChecked():
            self.new_window.setChecked(True)

    def cancel_clicked(self) -> None:
        self.done(0)

    def load_clicked(self) -> None:
        self.done(1)