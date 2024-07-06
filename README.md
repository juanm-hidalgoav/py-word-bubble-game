
# Word Bubble Game

This word bubble game was created using Python and Pygame. The game displays bubbles with words in English and Spanish, and the player must click on the corresponding English and Spanish words to match them. When a correct match is made, the bubbles disappear and new bubbles appear so that there are always six bubbles on the screen.

## Features

- Interactive bubble popping game with words in English and Spanish.
- Keeps six bubbles on screen at all times.
- Efficient event handling and frame rate control to optimize GPU usage.
- Supports UTF-8 encoded words for proper handling of special characters.

## Requirements

- Python 3.x
- Pygame library

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/juanm-hidalgoav/word-bubble-game.git
   cd word-bubble-game
   ```

2. **Install the required packages:**

   ```bash
   pip install pygame
   ```

3. **Prepare the assets:**

   Ensure you have the following files in an `assets` folder:

   - `background.png` (Background image for the game)
   - `bubble.png` (Image for the bubble)

4. **Prepare the words JSON file:**

   Create a `words.json` file with the following structure:

   ```json
   {
       "words": [
           {"english": "apple", "spanish": "manzana"},
           {"english": "house", "spanish": "casa"},
           {"english": "dog", "spanish": "perro"},
           {"english": "cat", "spanish": "gato"},
           {"english": "book", "spanish": "libro"},
           {"english": "again", "spanish": "otra vez"}
           // Add more word pairs as needed
       ]
   }
   ```

## How to Run

1. **Run the game:**

   ```bash
   python word_bubble_game.py
   ```

## How the Code Works

### Initialization

- Pygame Initialization:** The game initializes Pygame and sets the screen dimensions.
- Loading assets:** Background and bubble images are loaded.
- Word List Loading:** The words are loaded from a JSON file.
- Font Setup:** A font is set up to render the words in the bubbles.

### Bubble Creation

- Bubble Radius Calculation:** The radius of each bubble is calculated based on the maximum text dimensions to ensure that the text fits comfortably inside the bubbles.
- Circular Bubble Creation:** Bubbles are created with a circular surface and the text is rendered in the center.

### Bubble Class

The `Bubble` class represents each word bubble. It contains methods for creating the bubble, checking for overlap with other bubbles, and drawing itself on the screen.

### Adding Bubbles

- Add new bubble:** The `add_new_bubble` function ensures that a new bubble is placed without overlapping existing bubbles. It will try to place the bubble up to a maximum number of attempts.
- Ensure Six Bubbles:** The `ensure_six_bubbles` function ensures that there are always six bubbles on the screen by adding new bubbles as needed.

### Main Game Loop

- **Event Handling:** The game loop handles user input, specifically left mouse button clicks, to select and match bubbles.
- **Bubble Matching:** When two bubbles are selected, the game checks if they form a correct English-Spanish pair. If they match, the bubbles are removed, and new bubbles are added.
- **Screen Update:** The game screen is updated every frame, maintaining a frame rate of 30 FPS to optimize GPU usage.

### Game Optimization

- Frame Rate Control:** The `clock.tick(FPS)` call limits the frame rate to reduce the frequency of screen updates and offload the GPU.
- Efficient Rendering:** Only necessary elements are rendered for each frame to optimize performance.

