import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Button: #Create all button for the game
    def __init__(self, x, y, w, h, text, color, hover_color): # init is Конструктор
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont("Verdana", 20)

    def draw(self, surface): #draw everyhting 
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=5)
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

class TextInput: # Class for to enter the username
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.font = pygame.font.SysFont("Verdana", 24)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN: #enter the username
            if event.key == pygame.K_BACKSPACE: #delete the text
                self.text = self.text[:-1]
            elif len(self.text) < 12 and event.unicode.isalnum():
                self.text += event.unicode
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect, border_radius=5)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=5)
        text_surf = self.font.render(self.text, True, BLACK)
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + 5))