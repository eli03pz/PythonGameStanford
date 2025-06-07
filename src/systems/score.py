import pygame
class Score:
    def __init__(self):
        self.player1_score = 0
        self.player2_score = 0

    def update_score(self, player):
        if player == 1:
            self.player1_score += 1
        elif player == 2:
            self.player2_score += 1

    def get_scores(self):
        return self.player1_score, self.player2_score

    def display_scores(self, screen):
        font = pygame.font.Font(None, 36)
        score_text = f"Player 1: {self.player1_score}  Player 2: {self.player2_score}"
        text_surface = font.render(score_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))