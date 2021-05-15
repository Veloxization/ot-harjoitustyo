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
