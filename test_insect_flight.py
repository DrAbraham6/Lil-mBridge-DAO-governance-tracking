import unittest
from insect_flight import calculate_flight_stats, get_preset_insects, FlightStats


class TestInsectFlightCalculator(unittest.TestCase):

    def test_housefly_calculations(self):
        # Housefly: 12 mg, 200 Hz, 15% muscle ratio, 80 W/kg density
        stats = calculate_flight_stats(
            mass_mg=12.0,
            freq_hz=200.0,
            muscle_mass_ratio=0.15,
            power_density_w_kg=80.0,
            insect_name="Housefly",
        )

        self.assertEqual(stats.beats_per_min, 12000)
        self.assertAlmostEqual(stats.power_watts, 0.000144, places=7)
        self.assertAlmostEqual(stats.power_mw, 0.144, places=3)
        self.assertAlmostEqual(stats.energy_per_beat_joules, 7.2e-7, places=9)
        self.assertAlmostEqual(stats.energy_per_beat_uj, 0.72, places=2)
        self.assertAlmostEqual(stats.energy_per_min_joules, 0.00864, places=5)

    def test_bumblebee_calculations(self):
        # Bumblebee: 200 mg, 200 Hz, 18% muscle ratio, 80 W/kg density
        stats = calculate_flight_stats(
            mass_mg=200.0,
            freq_hz=200.0,
            muscle_mass_ratio=0.18,
            power_density_w_kg=80.0,
            insect_name="Bumblebee",
        )

        self.assertEqual(stats.beats_per_min, 12000)
        self.assertAlmostEqual(stats.power_mw, 2.88, places=2)
        self.assertAlmostEqual(stats.energy_per_beat_uj, 14.40, places=2)

    def test_yellow_jacket_calculations(self):
        # Yellow jacket: 100 mg, 220 Hz, 18% muscle ratio, 80 W/kg density
        stats = calculate_flight_stats(
            mass_mg=100.0,
            freq_hz=220.0,
            muscle_mass_ratio=0.18,
            power_density_w_kg=80.0,
            insect_name="Yellow jacket",
        )

        self.assertEqual(stats.beats_per_min, 13200)
        self.assertAlmostEqual(stats.power_mw, 1.44, places=2)
        self.assertAlmostEqual(stats.energy_per_beat_uj, 6.54545, places=3)

    def test_presets(self):
        presets = get_preset_insects()
        self.assertIn("housefly", presets)
        self.assertIn("bumblebee", presets)
        self.assertIn("yellow_jacket", presets)
        self.assertIsInstance(presets["housefly"], FlightStats)

    def test_zero_frequency_edge_case(self):
        stats = calculate_flight_stats(mass_mg=10.0, freq_hz=0.0)
        self.assertEqual(stats.beats_per_min, 0)
        self.assertEqual(stats.energy_per_beat_joules, 0.0)


if __name__ == "__main__":
    unittest.main()
