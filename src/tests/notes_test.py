import unittest
from classes.notes import Notes
from classes.npc import Npc
from classes.scenariogenerator import ScenarioGenerator
from classes.time import Time
from classes.interrogation import Interrogation

class TestInterrogation(unittest.TestCase):
    def setUp(self):
        self.scenario = ScenarioGenerator("seed for testing")
        self.time = Time(36)
        self.interrogation = Interrogation(self.time, self.scenario)
        self.npc = self.scenario.npcs[0]

    def test_initially_all_notes_are_unknown(self):
        notes = Notes(self.npc, self.scenario)
        for routine in notes.routine:
            self.assertEqual(routine, "UNKNOWN")
        for company in notes.company:
            self.assertEqual(company, "UNKNOWN")
        for note in notes.npc_location_at_time:
            for npc_location in note:
                self.assertEqual(npc_location, "UNKNOWN")

    def test_adding_a_routine_appears_correctly(self):
        notes = Notes(self.npc, self.scenario)
        index = 0
        reply = self.interrogation.where_were_you_at(self.npc, index)
        notes.add_routine_to_notes(index, reply)
        self.assertEqual(reply, notes.routine[index])
