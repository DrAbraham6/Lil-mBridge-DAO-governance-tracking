# Lil-mBridge-DAO-governance-tracking

## Insect Flight Calculator

A Python module to calculate wing-beat frequencies, power output, and mechanical energy estimates for various flying insects including houseflies, bumblebees, and yellow jackets.

### Overview

Insect flight muscles act as high-performance biological engines with specific power densities around 50 to 100 W/kg of muscle mass. This tool provides estimates for:
- Wing beats per second (Hz) and beats per minute (BPM)
- Mechanical power output in Watts / milliwatts
- Mechanical energy per wing beat (Joules / microjoules)
- Total mechanical energy per minute

### Usage

Run the module directly to view calculations for standard insect presets (Housefly, Bumblebee, Yellow jacket):

```bash
python3 insect_flight.py
```

### Running Tests

Execute the unit test suite:

```bash
python3 -m unittest test_insect_flight.py
```
