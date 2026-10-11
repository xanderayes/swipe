from PIL import Image, ImageDraw, ImageFont
import sys

# QWERTY keyboard layout with key positions (x, y coordinates)
# Using a standard keyboard layout with spacing
KEYBOARD_LAYOUT = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

# Key dimensions and spacing
KEY_WIDTH = 60
KEY_HEIGHT = 60
KEY_SPACING_X = 10
KEY_SPACING_Y = 15
KEYBOARD_START_X = 50
KEYBOARD_START_Y = 50

# Colors
BACKGROUND_COLOR = (30, 30, 30)
KEY_COLOR = (60, 60, 60)
KEY_BORDER_COLOR = (100, 100, 100)
TEXT_COLOR = (255, 255, 255)
TRACE_COLOR = (0, 200, 255)
TRACE_WIDTH = 4


def get_key_position(letter, image_width):
    """Get the (x, y) center position of a key on the keyboard."""
    letter = letter.upper()
    for row_idx, row in enumerate(KEYBOARD_LAYOUT):
        if letter in row:
            col_idx = row.index(letter)
            # Calculate x position with row offset for centering
            row_width = len(row) * KEY_WIDTH + (len(row) - 1) * KEY_SPACING_X
            row_start_x = KEYBOARD_START_X + (image_width - 100 - row_width) // 2
            
            x = row_start_x + col_idx * (KEY_WIDTH + KEY_SPACING_X) + KEY_WIDTH // 2
            y = KEYBOARD_START_Y + row_idx * (KEY_HEIGHT + KEY_SPACING_Y) + KEY_HEIGHT // 2
            return (x, y)
    return None


def draw_keyboard(draw, image_width, image_height):
    """Draw the QWERTY keyboard."""
    for row_idx, row in enumerate(KEYBOARD_LAYOUT):
        row_width = len(row) * KEY_WIDTH + (len(row) - 1) * KEY_SPACING_X
        row_start_x = KEYBOARD_START_X + (image_width - 100 - row_width) // 2
        
        for col_idx, key in enumerate(row):
            x = row_start_x + col_idx * (KEY_WIDTH + KEY_SPACING_X)
            y = KEYBOARD_START_Y + row_idx * (KEY_HEIGHT + KEY_SPACING_Y)
            
            # Draw key rectangle
            draw.rectangle(
                [x, y, x + KEY_WIDTH, y + KEY_HEIGHT],
                fill=KEY_COLOR,
                outline=KEY_BORDER_COLOR,
                width=2
            )
            
            # Draw key letter
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Get text bounding box to center the text
            bbox = draw.textbbox((0, 0), key, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            text_x = x + (KEY_WIDTH - text_width) // 2
            text_y = y + (KEY_HEIGHT - text_height) // 2 - bbox[1]
            
            draw.text((text_x, text_y), key, fill=TEXT_COLOR, font=font)


def draw_swipe_trace(draw, word, image_width):
    """Draw the swipe trace connecting the letters of the word."""
    word = word.upper()
    points = []
    
    for letter in word:
        pos = get_key_position(letter, image_width)
        if pos:
            points.append(pos)
    
    if len(points) < 2:
        return
    
    # Draw smooth curve through the points
    for i in range(len(points) - 1):
        draw.line(
            [points[i], points[i + 1]],
            fill=TRACE_COLOR,
            width=TRACE_WIDTH
        )
    
    # Draw circles at each point
    for point in points:
        draw.ellipse(
            [point[0] - 6, point[1] - 6, point[0] + 6, point[1] + 6],
            fill=TRACE_COLOR,
            outline=TRACE_COLOR
        )


def generate_swipe_image(word, output_file='swipe_track.png'):
    """Generate an image showing the swipe track for a word."""
    word = word.strip()
    if not word:
        print("Error: Please provide a word")
        return False
    
    # Calculate image dimensions
    max_row_length = max(len(row) for row in KEYBOARD_LAYOUT)
    keyboard_width = max_row_length * KEY_WIDTH + (max_row_length - 1) * KEY_SPACING_X + 100
    keyboard_height = len(KEYBOARD_LAYOUT) * (KEY_HEIGHT + KEY_SPACING_Y) + 100
    
    image_width = keyboard_width
    image_height = keyboard_height + 50  # Extra space at bottom
    
    # Create image
    image = Image.new('RGB', (image_width, image_height), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)
    
    # Draw keyboard
    draw_keyboard(draw, image_width, image_height)
    
    # Draw swipe trace
    draw_swipe_trace(draw, word, image_width)
    
    # Save image
    image.save(output_file)
    print(f"Swipe track image saved to: {output_file}")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python swipe_generator.py <word> [output_file]")
        print("Example: python swipe_generator.py hello")
        print("Example: python swipe_generator.py hello my_swipe.png")
        sys.exit(1)
    
    word = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'swipe_track.png'
    
    generate_swipe_image(word, output_file)


if __name__ == '__main__':
    main()
