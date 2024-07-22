import pygame
import json
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1024 # screen width
SCREEN_HEIGHT = 768 # screen height

# Load images
background = pygame.image.load('assets/background.png')
bubble_img = pygame.image.load('assets/bubble.png')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load words from JSON file
with open('words.json', 'r', encoding='utf-8') as file:
    words = json.load(file)['words']

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Word Bubble Game')

# Set frame rate
clock = pygame.time.Clock()
FPS = 30

# Font setup
font = pygame.font.Font(None, 28)  # Reduced font size by ~20%

# Calculate maximum text dimensions
max_text_width = 0
max_text_height = 0
for word_pair in words:
    english_text = font.render(word_pair['english'], True, BLACK)
    spanish_text = font.render(word_pair['spanish'], True, BLACK)
    max_text_width = max(max_text_width, english_text.get_width(), spanish_text.get_width())
    max_text_height = max(max_text_height, english_text.get_height(), spanish_text.get_height())

# Define bubble radius based on maximum text size
radius = int((max(max_text_width, max_text_height) // 2 + 10) * 0.8)  # Adjust this as needed 

# Define grid size
GRID_WIDTH = 10
GRID_HEIGHT = 8
CELL_WIDTH = SCREEN_WIDTH // GRID_WIDTH
CELL_HEIGHT = SCREEN_HEIGHT // GRID_HEIGHT

# Function to get the font size for a given text while maintaining aspect ratio and fitting within the given dimensions
def get_font_size(text, max_width, max_height, font_name=None):
    font_size = 28
    font = pygame.font.Font(font_name, font_size)
    text_surf = font.render(text, True, BLACK)
    while text_surf.get_width() > max_width or text_surf.get_height() > max_height:
        font_size -= 1
        font = pygame.font.Font(font_name, font_size)
        text_surf = font.render(text, True, BLACK)
    return font_size


# Function to create a circular bubble
def create_circular_bubble(text):
    bubble_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    bubble_rect = bubble_surf.get_rect()
    
    # Scale bubble image to fit within the circle while maintaining aspect ratio
    scaled_bubble_img = pygame.transform.smoothscale(bubble_img, (radius * 2, radius * 2))
    bubble_surf.blit(scaled_bubble_img, (0, 0))
    
    # Draw text on the bubble
    font_size = get_font_size(text, radius * 1.5, radius * 1.5)  # Allow some padding
    font = pygame.font.Font(None, font_size)
    
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = bubble_rect.center
    bubble_surf.blit(text_surf, text_rect.topleft)
    
    return bubble_surf


# Bubble class
class Bubble(pygame.sprite.Sprite):
    def __init__(self, word, x, y, language):
        super().__init__()
        self.word = word
        self.language = language
        self.image = create_circular_bubble(word)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Function to check if two bubbles overlap
def bubbles_overlap(bubble1, bubble2):
    distance = ((bubble1.rect.centerx - bubble2.rect.centerx) ** 2 + (bubble1.rect.centery - bubble2.rect.centery) ** 2) ** 0.5
    return distance < radius * 1.8  # Allow a bit of overlap by reducing the factor

# Function to add a new bubble ensuring no overlap
def add_new_bubble(word, language, bubbles):
    placed = False
    attempts = 0
    max_attempts = 10000  # Increase the maximum attempts further
    while not placed and attempts < max_attempts:
        x_pos = random.randint(radius, SCREEN_WIDTH - radius)
        y_pos = random.randint(radius, SCREEN_HEIGHT - radius)

        new_bubble = Bubble(word, x_pos, y_pos, language)
        if not any(bubbles_overlap(new_bubble, bubble) for bubble in bubbles):
            bubbles.append(new_bubble)
            placed = True
        attempts += 1
    if not placed:
        print(f"Could not place bubble for word: {word} after {attempts} attempts")
    return placed



# Ensure exactly 6 bubbles on the screen
def ensure_six_bubbles(bubbles, used_words):
    while len(bubbles) < 6:
        available_pairs = [wp for wp in words if wp['english'] not in used_words and wp['spanish'] not in used_words]
        if available_pairs:
            new_pair = random.choice(available_pairs)
            temp_used_words = set([new_pair['english'], new_pair['spanish']])
            if add_new_bubble(new_pair['english'], 'english', bubbles) and add_new_bubble(new_pair['spanish'], 'spanish', bubbles):
                used_words.update(temp_used_words)

# Create initial bubbles
bubbles = []
used_words = set()
initial_pairs = random.sample(words, 3)  # Select 3 random pairs to start

for word_pair in initial_pairs:
    used_words.add(word_pair['english'])
    used_words.add(word_pair['spanish'])
    add_new_bubble(word_pair['english'], 'english', bubbles)
    add_new_bubble(word_pair['spanish'], 'spanish', bubbles)

selected_bubbles = []

# Main game loop
running = True
while running:
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Only handle left mouse button clicks
            x, y = event.pos
            for bubble in bubbles:
                if bubble.rect.collidepoint(x, y):
                    print(f'Clicked on: {bubble.word}')
                    selected_bubbles.append(bubble)
                    if len(selected_bubbles) == 2:
                        bubble1, bubble2 = selected_bubbles
                        if bubble1.language != bubble2.language:
                            if (bubble1.language == 'english' and bubble2.language == 'spanish' and any(word_pair['english'] == bubble1.word and word_pair['spanish'] == bubble2.word for word_pair in words)) or \
                               (bubble1.language == 'spanish' and bubble2.language == 'english' and any(word_pair['english'] == bubble2.word and word_pair['spanish'] == bubble1.word for word_pair in words)):
                                print(f'Matched pair: {bubble1.word} - {bubble2.word}')
                                bubbles.remove(bubble1)
                                bubbles.remove(bubble2)
                                used_words.discard(bubble1.word)
                                used_words.discard(bubble2.word)
                        selected_bubbles = []
    
    ensure_six_bubbles(bubbles, used_words)

    for bubble in bubbles:
        bubble.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)  # Limit the frame rate

pygame.quit()
