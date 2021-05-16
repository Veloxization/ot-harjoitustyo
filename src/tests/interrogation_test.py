import unittest
from classes.interrogation import Interrogation
from classes.time import Time
from classes.scenariogenerator import ScenarioGenerator

class TestInterrogation(unittest.TestCase):
    def setUp(self):
        self.scenario = ScenarioGenerator("seed for testing")
        self.time = Time(36)
        self.interrogation = Interrogation(self.time, self.scenario)

    def test_murderer_does_not_tell_their_true_location_at_murder_time(self):
        result_room = self.interrogation.where_were_you_at(self.scenario.murderer, self.scenario.murder_committed_index)[0]
        self.assertNotEqual(result_room, self.scenario.crime_scene)

    def test_murderer_says_they_were_alone_at_murder_time(self):
        result_company = self.interrogation.who_were_you_with_at(self.scenario.murderer, self.scenario.murder_committed_index)[0]
        self.assertEqual("Alone", result_company)

    def test_the_liar_isnt_revealed_from_asking_who_they_were_with_at_start_time(self):
        npcs = self.interrogation.who_were_you_with_at(self.scenario.liar, 0)[0]
        self.assertNotEqual(npcs, "Alone")
