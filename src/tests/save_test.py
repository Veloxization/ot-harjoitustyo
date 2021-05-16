import unittest
import os
from os import walk

from classes.save import Save
from classes.notes import Notes
from classes.scenariogenerator import ScenarioGenerator
from classes.npc import Npc

class TestSave(unittest.TestCase):
    def setUp(self):
        self.scenario = ScenarioGenerator("seed for testing")
        npc1 = self.scenario.npcs[0]
        npc2 = self.scenario.npcs[1]
        note1 = Notes(npc1, self.scenario)
        note2 = Notes(npc2, self.scenario)
        self.notes = {npc1.name: note1, npc2.name: note2}

    def test_a_file_with_a_correct_name_is_created(self):
        save = Save()
        name = "RESERVED_FOR_TESTING"
        seed = self.scenario.seed
        difficulty = self.scenario.difficulty
        save.write_to_file(name, seed, difficulty, self.notes)
        files = []
        for (dirpath, dirnames, filenames) in walk("src/data/saves"):
            files.extend(filenames)
            break
        found = f"{name}.sav" in files
        self.assertEqual(True, found)
        if os.path.exists(f"src/data/saves/{name}.sav"):
            os.remove(f"src/data/saves/{name}.sav")
        else:
            print("No file found")
