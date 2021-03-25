import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(10)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti), "saldo: 0.1")

    def test_saldo_kasvaa_oikein(self):
        self.maksukortti.lataa_rahaa(1)
        self.assertEqual(str(self.maksukortti), "saldo: 0.11")

    def test_saldo_vahenee_oikein_kun_rahaa_tarpeeksi(self):
        self.maksukortti.ota_rahaa(1)
        self.assertEqual(str(self.maksukortti), "saldo: 0.09")

    def test_saldo_ei_muutu_jos_rahaa_ei_tarpeeksi(self):
        self.maksukortti.ota_rahaa(11)
        self.assertEqual(str(self.maksukortti), "saldo: 0.1")

    def test_ota_rahaa_palauttaa_totuusarvot_oikein(self):
        self.assertEqual(self.maksukortti.ota_rahaa(11), False)
        self.assertEqual(self.maksukortti.ota_rahaa(9), True)
