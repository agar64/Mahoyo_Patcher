import os
from mahoyo_tools import hfa

class Extractor:
    def __init__(self, game_dir, hfa_name):
        self.GAME_DIR = game_dir
        self.hfa_name = hfa_name
        self.hfa_path = os.path.join(self.GAME_DIR, f"{hfa_name}.hfa")
        self.archive = hfa.HfaArchive(self.hfa_path, 'rw')

    def extract(self, script, filepath):
        full_path = os.path.normpath(os.path.join(self.GAME_DIR, filepath))
        directory = os.path.dirname(full_path)
        os.makedirs(directory, exist_ok=True)
        self.archive.open()
        entry = self.archive[script]
        entry.extract(full_path)
        self.archive.close()

    def inject(self, script, filepath):
        self.archive.open()
        entry = self.archive[script]
        entry.inject(os.path.join(self.GAME_DIR, filepath))
        self.archive.close()