# VonNeuman   

A Python simulator for the Von Neumann architecture, featuring a visual console interface.

## Features

- Simulates a simple Von Neumann CPU with configurable bus sizes.
- Supports arithmetic and logic instructions: ADD, SUB, PRD, PWR, AND, OR, MOV, HALT.
- Visualizes memory, registers, and ALU operations in the console.
- Loads instructions interactively or from a file.

## Usage

1. **Run the simulator:**
   ```sh
   python scripts/main.py
   ```

   or

   ```sh
   start bin/bin.exe
   ```

2. **Enter instructions:**
   - Type 8-bit binary instructions one by one.
   - Type `run` to start execution.
   - Type `charge` to load instructions from a file (e.g., `others/test.txt`).
   - Type `exit` to quit.

3. **Simulation controls:**
   - Set simulation speed (seconds per step).
   - View the visual representation of the CPU and memory.

## File Structure

- `scripts/main.py`: Main simulator logic
- `scripts/visual.py`: Visual interface
- `others/test.txt`: Example instruction set
- `others/template`: Visual layout template
- `bin/bin.exe`: Binary executable (not used by the Python scripts)

## Example Instructions

See `others/test.txt` for a sample instruction set.

## Requirements

- Python 3.x

## Future Updates

- Custom memory bus and direction bus size selection from the visual interface.

-Vinbelt

arreglos:
 1.- control del path de los ficheros
 2.- El fichero de memoria lo carga al revés con charge...
