import tkinter as tk
from tkinter import messagebox
from sounddevice import stop
from pydub import AudioSegment
from pydub.playback import play
import os
import numpy as np

print("Current working directory:", os.getcwd())
with open("spaceappssounds/rain.mp3", "r") as f:
    print("File is accessible")

# Ensure ffmpeg is configured (update with correct path if needed)
AudioSegment.converter = "C:/ffmpeg/bin/ffmpeg.exe"  # Update this to the actual ffmpeg path on your system

# Define a class to represent an exoplanet's environment
root = tk.Tk()
root.title("Exoplanet Sound Simulator")

class ExoplanetEnvironment:
    def __init__(self, temperature, pressure, gas_composition, wind_speed, volcanic_activity):
        self.temperature = temperature          # in Kelvin
        self.pressure = pressure                # in Pascals
        self.gas_composition = gas_composition  # dict of gases, e.g., {'H2': 0.8, 'He': 0.2}
        self.wind_speed = wind_speed            # in m/s
        self.volcanic_activity = volcanic_activity  # activity level (0 to 1 scale)

# Generate wind sound and convert to pydub AudioSegment
def generate_wind_sound(wind_speed, duration=10, sampling_rate=44100):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

    # Create a base white noise signal
    noise = np.random.normal(0, 1, size=t.shape)

    # Use a lower frequency modulation to simulate gusting wind (slower changes)
    modulation = 1 + 0.2 * np.sin(2 * np.pi * wind_speed / 20 * t)

    # Multiply white noise by modulation factor and wind speed to shape the sound
    wind_sound = 0.001 * wind_speed * noise * modulation

    # Convert to 16-bit PCM format and create AudioSegment
    wind_sound_pcm = (wind_sound * 32767).astype(np.int16).tobytes()
    wind_audio = AudioSegment(
        data=wind_sound_pcm,
        sample_width=2,  # 16 bits = 2 bytes
        frame_rate=sampling_rate,
        channels=1
    )
    return wind_audio

# Calculate speed of sound based on temperature and gas composition
def calculate_speed_of_sound(temperature, gas_composition):
    gas_molar_masses = {'N2': 0.028, 'O2': 0.032, 'CO2': 0.044, 'H2': 0.002, 'He': 0.004, 'H2O': 0.018}
    gamma = 1.4  # Approximate value

    avg_molar_mass = sum(gas_molar_masses[gas] * fraction for gas, fraction in gas_composition.items())
    r = 8.31446261815324
    speed_of_sound = (gamma * r * temperature / avg_molar_mass) ** 0.5
    return speed_of_sound

# Load and resample the sound file to 44100 Hz sample rate
def load_and_resample(file_path, target_sample_rate=44100):
    try:
        sound = AudioSegment.from_file(file_path)
        sound = sound.set_frame_rate(target_sample_rate)  # Resample to 44100 Hz
        return sound
    except Exception as e:
        messagebox.showerror("File Error", f"Error processing {file_path}: {e}")
        return None

# Probability models for different surface conditions
def calculate_rain_probability(temperature, pressure, gas_composition):
    if temperature < 273 or temperature > 373:
        return 0
    pressure_factor = min(1, pressure / 101325)
    water_vapor_fraction = gas_composition.get('H2O', 0)
    return pressure_factor * water_vapor_fraction

def calculate_thunderstorm_probability(wind_speed, volcanic_activity, gas_composition):
    wind_factor = min(1, wind_speed / 50)
    volcanic_factor = volcanic_activity
    water_vapor_fraction = gas_composition.get('H2O', 0)
    return wind_factor * volcanic_factor * water_vapor_fraction

def calculate_ice_cracking_probability(temperature, volcanic_activity):
    if temperature > 273:
        return 0
    return (273 - temperature) / 273 * (1 - volcanic_activity)

def calculate_ocean_waves_probability(temperature, wind_speed, gas_composition):
    if temperature < 273 or temperature > 373:
        return 0
    wind_factor = min(1, wind_speed / 20)
    water_vapor_fraction = gas_composition.get('H2O', 0)
    return wind_factor * water_vapor_fraction

# Adjust run_simulation function for shorter duration
def run_simulation():
    try:
        # Get user inputs
        temperature = float(temp_entry.get())
        pressure = float(pressure_entry.get())
        gas_composition = parse_gas_composition(gas_entry.get())
        wind_speed = float(wind_entry.get())
        volcanic_activity = float(volcanic_entry.get())

        # Create the exoplanet environment
        planet_env = ExoplanetEnvironment(
            temperature=temperature,
            pressure=pressure,
            gas_composition=gas_composition,
            wind_speed=wind_speed,
            volcanic_activity=volcanic_activity
        )

        # Calculate probabilities for surface conditions
        rain_prob = calculate_rain_probability(planet_env.temperature, planet_env.pressure, planet_env.gas_composition)
        thunderstorm_prob = calculate_thunderstorm_probability(planet_env.wind_speed, planet_env.volcanic_activity, planet_env.gas_composition)
        ice_cracking_prob = calculate_ice_cracking_probability(planet_env.temperature, planet_env.volcanic_activity)
        ocean_waves_prob = calculate_ocean_waves_probability(planet_env.temperature, planet_env.wind_speed, planet_env.gas_composition)

        # Initialize combined sound with generated wind sound
        combined_sound = generate_wind_sound(wind_speed)

        # Load and resample sounds based on probabilities, and mix them together
        try:
            if rain_prob > 0.5:
                rain_sound = load_and_resample('spaceappssounds/rain.mp3')
                if rain_sound:
                    combined_sound = combined_sound.overlay(rain_sound)

            if thunderstorm_prob > 0.5:
                thunderstorm_sound = load_and_resample('spaceappssounds/thunder.mp3')
                if thunderstorm_sound:
                    combined_sound = combined_sound.overlay(thunderstorm_sound)

            if ice_cracking_prob > 0.5:
                ice_sound = load_and_resample('spaceappssounds/ice.mp3')
                if ice_sound:
                    combined_sound = combined_sound.overlay(ice_sound)

            if ocean_waves_prob > 0.5:
                ocean_sound = load_and_resample('spaceappssounds/ocean.mp3')
                if ocean_sound:
                    combined_sound = combined_sound.overlay(ocean_sound)

        except FileNotFoundError as e:
            messagebox.showerror("File Error", f"Missing sound file: {e}")

        # Play the combined sound
        play(combined_sound)

        # Calculate and update speed of sound label
        sound_speed = calculate_speed_of_sound(planet_env.temperature, planet_env.gas_composition)
        speed_label.config(text=f"Calculated Speed of Sound: {sound_speed:.2f} m/s")

        print("rain:" ,rain_prob,"thunder:", thunderstorm_prob,"ice:", ice_cracking_prob,"waves:", ocean_waves_prob)

    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid input: {e}")

# Stop the sound playback
def stop_simulation():
    stop()

# Function to parse gas composition input
def parse_gas_composition(gas_input):
    try:
        gas_dict = {}
        gases = gas_input.split(',')
        for gas in gases:
            name, value = gas.split(':')
            gas_dict[name.strip()] = float(value.strip())
        return gas_dict
    except ValueError:
        raise ValueError("Gas composition must be in the format: 'Gas1:Fraction,Gas2:Fraction,...'")

# Create the main window

# Temperature input
tk.Label(root, text="Temperature (K)").grid(row=0, column=0, padx=10, pady=5)
temp_entry = tk.Entry(root, width=32)
temp_entry.insert(0, "290")  # Default example values
temp_entry.grid(row=0, column=1, padx=10, pady=5)

# Pressure input
tk.Label(root, text="Pressure (Pa)").grid(row=1, column=0, padx=10, pady=5)
pressure_entry = tk.Entry(root, width=32)
pressure_entry.insert(0, "101325")  # Default example values
pressure_entry.grid(row=1, column=1, padx=10, pady=5)

# Gas composition input
tk.Label(root, text="Gas Composition").grid(row=2, column=0, padx=10, pady=5)
gas_entry = tk.Entry(root, width=32)
gas_entry.insert(0, "N2:0.78,O2:0.21,CO2:0.01,H2O:0.01")  # Default example values
gas_entry.grid(row=2, column=1, padx=10, pady=5)

# Wind speed input
tk.Label(root, text="Wind Speed (m/s)").grid(row=3, column=0, padx=10, pady=5)
wind_entry = tk.Entry(root, width=32)
wind_entry.insert(0, "15")  # Default example values
wind_entry.grid(row=3, column=1, padx=10, pady=5)

# Volcanic activity input
tk.Label(root, text="Volcanic Activity (0 to 1)").grid(row=4, column=0, padx=10, pady=5)
volcanic_entry = tk.Entry(root, width=32)
volcanic_entry.insert(0, "0.5")  # Default example values
volcanic_entry.grid(row=4, column=1, padx=10, pady=5)

# Speed of sound label
speed_label = tk.Label(root, text="Calculated Speed of Sound: ")
speed_label.grid(row=8, column=0, columnspan=1, padx=1, pady=5)

# Run and stop buttons
run_button = tk.Button(root, text="Run Simulation", command=run_simulation)
run_button.grid(row=7, column=1, padx=100)

#stop_button = tk.Button(root, text="Stop Simulation", command=stop_simulation)
#stop_button.grid(row=6, column=1, padx=10, pady=10)

checkbutton = tk.Checkbutton(root, text="you see a few alien dancing in the distance")
checkbutton.grid(row=6, padx=10)

root.mainloop()
