# Swipe Track Generator

A Python script that generates images showing swipe typing tracks for any word on a QWERTY keyboard.

## Features

- Visualizes the QWERTY keyboard layout
- Draws the swipe/gesture typing path connecting letters
- Supports any word input
- Customizable output filename

## Installation

1. Install Python 3.6 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic usage
```bash
python swipe_generator.py hello
```
This will create `swipe_track.png` showing the swipe path for "hello".

### Custom output filename
```bash
python swipe_generator.py hello my_swipe.png
```

### Examples
```bash
python swipe_generator.py python
python swipe_generator.py swipe typing.png
python swipe_generator.py qwerty
```

## How it works

1. The script takes a word as input
2. It maps each letter to its position on a QWERTY keyboard
3. It draws the keyboard layout
4. It connects the letter positions with a blue trace line
5. The resulting image is saved as a PNG file

## Output

The generated image shows:
- A dark background with a QWERTY keyboard
- Gray keys with white letters
- A blue trace line connecting the letters in the word
- Blue circles marking each letter position

## Requirements

- Python 3.6+
- Pillow (PIL) 10.0.0
