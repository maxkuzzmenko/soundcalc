@ -1,95 +0,0 @@
### README.md

# Exoplanet Sound Simulator

This project simulates the soundscape of an exoplanet based on environmental parameters such as temperature, pressure, gas composition, wind speed, and volcanic activity. It generates a wind sound and combines it with other pre-recorded sounds such as rain, thunderstorms, ice cracking, and ocean waves based on calculated probabilities for each environmental condition.

## Features

- **Simulate Exoplanetary Soundscape**: Based on user inputs for temperature, pressure, gas composition, wind speed, and volcanic activity, the app generates and plays a soundscape resembling an exoplanet's atmosphere.
- **Generated Wind Sound**: Wind noise is generated dynamically and is always included in the soundscape.
- **Pre-recorded Sounds**: Additional pre-recorded sounds (rain, thunderstorms, ice cracking, and ocean waves) are added if the probabilities for these conditions are high enough.
- **Speed of Sound Calculation**: The program calculates the speed of sound based on temperature and gas composition, and displays it in the GUI.

## Requirements

To run the Exoplanet Sound Simulator, ensure the following dependencies are installed:

### Python Version
- Python 3.7 or higher

### Required Libraries

- `numpy`: For generating the wind sound.
- `pydub`: For handling and mixing audio files (MP3s).
- `sounddevice`: For audio playback.
- `tkinter`: For the GUI (this is included with most Python installations).

To install the required libraries, use the following command:

```bash
pip install numpy pydub sounddevice
```

### Additional Requirements

1. **FFmpeg**: The `pydub` library requires FFmpeg to handle MP3 files. You can download it from the [official FFmpeg website](https://ffmpeg.org/download.html). After downloading, make sure to add FFmpeg to your system's PATH or configure it in the script as shown in the code.

2. **MP3 Files**: The following audio files should be available in the `spaceappssounds/` directory:
    - `rain.mp3`
    - `thunder.mp3`
    - `ice.mp3`
    - `ocean.mp3`

   If these files are not available, the program will raise a "File Error" for missing files.

## How to Run

1. Ensure that Python and the necessary libraries are installed.
2. Place the required MP3 files (`rain.mp3`, `thunder.mp3`, `ice.mp3`, `ocean.mp3`) in the `spaceappssounds/` directory.
3. Run the program using:

   ```bash
   python exoplanet_sound_simulator.py
   ```

4. The program will open a graphical user interface (GUI) where you can enter:
   - **Temperature (K)**: Temperature in Kelvin.
   - **Pressure (Pa)**: Pressure in Pascals.
   - **Gas Composition**: A string specifying the gas composition in the format `'Gas1:Fraction,Gas2:Fraction,...'`. Example: `'N2:0.78,O2:0.21,CO2:0.01,H2O:0.01'`.
   - **Wind Speed (m/s)**: Wind speed in meters per second.
   - **Volcanic Activity (0 to 1)**: A value between 0 and 1 representing the intensity of volcanic activity.
   
5. Press the "Run Simulation" button to generate the soundscape. The calculated speed of sound will also be displayed.
6. To stop the playback, press the "Stop Simulation" button.

## Code Overview

- **ExoplanetEnvironment**: This class stores the environmental parameters for the simulation.
- **generate_wind_sound**: This function generates a wind sound using white noise, modulated to simulate gusting wind.
- **calculate_speed_of_sound**: Calculates the speed of sound based on temperature and gas composition.
- **load_and_resample**: Loads and resamples the pre-recorded MP3 files.
- **calculate_rain_probability**, **calculate_thunderstorm_probability**, **calculate_ice_cracking_probability**, **calculate_ocean_waves_probability**: These functions calculate the probability of each weather condition occurring, based on the environmental parameters.
- **run_simulation**: The main function that combines generated and pre-recorded sounds based on calculated probabilities and plays the resulting soundscape.

## Example Use Case

1. Set the temperature to `290 K` (around 17°C).
2. Set the pressure to `101325 Pa` (standard Earth atmosphere).
3. Use a gas composition like `'N2:0.78,O2:0.21,CO2:0.01,H2O:0.01'`.
4. Set the wind speed to `15 m/s`.
5. Set volcanic activity to `0.5` (medium volcanic activity).
6. Run the simulation to hear the generated soundscape for these conditions.

## Troubleshooting

- **Missing File Error**: Ensure the required MP3 files are available in the `spaceappssounds/` folder.
- **No Sound Played**: Make sure that probabilities for rain, thunderstorms, ice cracking, or ocean waves are non-zero based on the input parameters.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Feel free to modify the settings and experiment with different environmental conditions to generate unique exoplanet soundscapes!