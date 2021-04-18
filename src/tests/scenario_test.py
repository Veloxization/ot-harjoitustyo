import unittest
from classes.scenariogenerator import ScenarioGenerator

class TestScenario(unittest.TestCase):
    def setUp(self):
        self.seed = "seed for testing"

    def test_same_seed_gives_same_npcs(self):
        scen1 = ScenarioGenerator(self.seed)
        scen2 = ScenarioGenerator(self.seed)
        self.assertEqual(scen1.npcs, scen2.npcs)

    def test_same_seed_gives_same_murderer(self):
        scen1 = ScenarioGenerator(self.seed)
        scen2 = ScenarioGenerator(self.seed)
        self.assertEqual(scen1.murderer, scen2.murderer)

    def test_same_seed_gives_same_murderer_despite_difficulty(self):
        scen1 = ScenarioGenerator(self.seed)
        scen2 = ScenarioGenerator(self.seed, 2)
        self.assertEqual(scen1.murderer, scen2.murderer)
