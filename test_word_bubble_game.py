import unittest
import pygame
from word_bubble_game import Bubble, create_circular_bubble, bubbles_overlap, add_new_bubble

class TestWordBubbleGame(unittest.TestCase):
    
    def setUp(self):
        # Initialize Pygame
        pygame.init()
        
        # Create a screen for rendering (necessary for creating bubble surfaces)
        self.screen = pygame.display.set_mode((800, 600))
        
        # Sample words
        self.sample_word_english = "test"
        self.sample_word_spanish = "prueba"
        
        # Create sample bubbles
        self.bubble1 = Bubble(self.sample_word_english, 100, 100, 'english')
        self.bubble2 = Bubble(self.sample_word_spanish, 200, 200, 'spanish')
    
    def tearDown(self):
        # Quit Pygame
        pygame.quit()
    
    def test_create_circular_bubble(self):
        bubble_surface = create_circular_bubble(self.sample_word_english)
        self.assertIsInstance(bubble_surface, pygame.Surface)
        self.assertEqual(bubble_surface.get_width(), self.bubble1.rect.width)
        self.assertEqual(bubble_surface.get_height(), self.bubble1.rect.height)
    
    def test_bubbles_overlap(self):
        # Bubbles should not overlap
        self.assertFalse(bubbles_overlap(self.bubble1, self.bubble2))
        
        # Move bubble2 to overlap with bubble1
        self.bubble2.rect.center = (110, 110)
        self.assertTrue(bubbles_overlap(self.bubble1, self.bubble2))
    
    def test_add_new_bubble(self):
        bubbles = [self.bubble1, self.bubble2]
        add_new_bubble("newword", "english")
        # Ensure the new bubble does not overlap with existing ones
        for bubble in bubbles:
            self.assertFalse(bubbles_overlap(bubble, bubbles[-1]))

if __name__ == "__main__":
    unittest.main()
