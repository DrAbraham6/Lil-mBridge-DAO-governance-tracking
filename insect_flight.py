"""Insect Flight Calculator

Calculates wing-beat frequencies, power output, and mechanical energy per stroke/second/minute
for various insects (e.g. housefly, bumblebee, yellow jacket).
"""

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class FlightStats:
    insect_name: str
    mass_mg: float
    frequency_hz: float
    beats_per_min: int
    power_watts: float
    energy_per_beat_joules: float
    energy_per_min_joules: float

    @property
    def power_mw(self) -> float:
        return self.power_watts * 1e3

    @property
    def energy_per_beat_uj(self) -> float:
        return self.energy_per_beat_joules * 1e6


def calculate_flight_stats(
    mass_mg: float,
    freq_hz: float,
    muscle_mass_ratio: float = 0.18,
    power_density_w_kg: float = 80.0,
    insect_name: str = "Insect",
) -> FlightStats:
    """Calculate flight stats for an insect given mass in mg and wing frequency in Hz."""
    mass_kg = mass_mg * 1e-6
    muscle_mass_kg = mass_kg * muscle_mass_ratio
    power_watts = muscle_mass_kg * power_density_w_kg
    energy_per_beat = power_watts / freq_hz if freq_hz > 0 else 0.0
    beats_per_min = int(freq_hz * 60)
    energy_per_min = power_watts * 60.0

    return FlightStats(
        insect_name=insect_name,
        mass_mg=mass_mg,
        frequency_hz=freq_hz,
        beats_per_min=beats_per_min,
        power_watts=power_watts,
        energy_per_beat_joules=energy_per_beat,
        energy_per_min_joules=energy_per_min,
    )


def get_preset_insects() -> Dict[str, FlightStats]:
    """Returns calculations for default presets: Housefly, Bumblebee, Yellow jacket."""
    return {
        "housefly": calculate_flight_stats(
            mass_mg=12.0,
            freq_hz=200.0,
            muscle_mass_ratio=0.15,
            power_density_w_kg=80.0,
            insect_name="Housefly",
        ),
        "bumblebee": calculate_flight_stats(
            mass_mg=200.0,
            freq_hz=200.0,
            muscle_mass_ratio=0.18,
            power_density_w_kg=80.0,
            insect_name="Bumblebee",
        ),
        "yellow_jacket": calculate_flight_stats(
            mass_mg=100.0,
            freq_hz=220.0,
            muscle_mass_ratio=0.18,
            power_density_w_kg=80.0,
            insect_name="Yellow jacket",
        ),
    }


def main():
    presets = get_preset_insects()
    print("=== Insect Wing Beats & Flight Energy Calculations ===\n")

    housefly = presets["housefly"]
    print(f"Housefly (Mass: {housefly.mass_mg} mg, Wing Frequency: {housefly.frequency_hz} Hz):")
    print(f"  Beats per second: {int(housefly.frequency_hz)}")
    print(f"  Beats per minute: {housefly.beats_per_min:,}")
    print(f"  Power output: {housefly.power_watts:.6f} W ({housefly.power_mw:.3f} mW)")
    print(f"  Energy per beat: {housefly.energy_per_beat_joules:.2e} Joules ({housefly.energy_per_beat_uj:.2f} µJ)")
    print(f"  Energy per minute: {housefly.energy_per_min_joules:.5f} Joules\n")

    bb = presets["bumblebee"]
    print(f"Bumblebee (Mass: {bb.mass_mg} mg, Wing Frequency: {bb.frequency_hz} Hz):")
    print(f"  Beats per minute: {bb.beats_per_min:,} bpm")
    print(f"  Power output: {bb.power_mw:.2f} mW")
    print(f"  Energy per beat: {bb.energy_per_beat_uj:.2f} µJ\n")

    yj = presets["yellow_jacket"]
    print(f"Yellow Jacket (Mass: {yj.mass_mg} mg, Wing Frequency: {yj.frequency_hz} Hz):")
    print(f"  Beats per minute: {yj.beats_per_min:,} bpm")
    print(f"  Power output: {yj.power_mw:.2f} mW")
    print(f"  Energy per beat: {yj.energy_per_beat_uj:.2f} µJ\n")


if __name__ == "__main__":
    main()
