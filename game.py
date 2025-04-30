import pygame
import sys
from pygame.locals import *

class TicTacToe:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # 3x3 grid
        self.current_player = 1  # 1 for X, 2 for O
        self.game_over = False
        self.winner = None
        self.winning_line = None
    
    def make_move(self, row, col):
        if self.game_over or row not in range(3) or col not in range(3):
            return False
        
        if self.board[row][col] != 0:
            return False
        
        self.board[row][col] = self.current_player
        self.check_winner(row, col)
        
        if not self.game_over:
            self.current_player = 3 - self.current_player  # Switch player (1->2, 2->1)
        return True
    
    def check_winner(self, row, col):
        player = self.board[row][col]
        
        # Check row
        if all(cell == player for cell in self.board[row]):
            self.winning_line = ('row', row)
            self.game_over = True
            self.winner = player
            return
        
        # Check column
        if all(self.board[i][col] == player for i in range(3)):
            self.winning_line = ('col', col)
            self.game_over = True
            self.winner = player
            return
        
        # Check diagonals
        if row == col and all(self.board[i][i] == player for i in range(3)):
            self.winning_line = ('diag', 1)
            self.game_over = True
            self.winner = player
            return
        
        if row + col == 2 and all(self.board[i][2-i] == player for i in range(3)):
            self.winning_line = ('diag', 2)
            self.game_over = True
            self.winner = player
            return
        
        # Check for draw
        if all(cell != 0 for row in self.board for cell in row):
            self.game_over = True
    
    def get_state(self):
        """Added for testing - returns the current game state"""
        return {
            'board': [row[:] for row in self.board],
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner,
            'winning_line': self.winning_line
        }
    
    def get_valid_moves(self):
        """Added for testing - returns list of valid moves"""
        moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    moves.append((row, col))
        return moves

class TicTacToeGUI:
    def __init__(self, is_ai_game=False):
        pygame.init()
        
        # Configurable parameters
        self.cell_size = 150  # Size of each cell in pixels
        self.line_width = 10   # Width of grid lines
        self.margin = 50       # Margin around the grid
        self.info_height = 100 # Height of info panel
        
        # Calculate window size
        self.width = 3 * self.cell_size + 2 * self.margin
        self.height = 3 * self.cell_size + 2 * self.margin + self.info_height
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tic Tac Toe - DRL")
        
        self.game = TicTacToe()
        self.is_ai_game = is_ai_game
        self.ai_player = 2 if is_ai_game else None
        
        # Colors
        self.BG_COLOR = (28, 170, 156)  # Background
        self.LINE_COLOR = (23, 145, 135)  # Grid lines
        self.X_COLOR = (84, 84, 84)     # X color
        self.O_COLOR = (242, 235, 211)  # O color
        self.WIN_COLOR = (255, 0, 0)    # Winning line color
        self.INFO_BG = (255, 255, 255)  # Info panel background
        
        # Fonts
        self.font = pygame.font.SysFont('Arial', 36)
        self.small_font = pygame.font.SysFont('Arial', 24)
        
        # Create symbol images
        self.x_img = self.create_symbol('X')
        self.o_img = self.create_symbol('O')
    
    def create_symbol(self, symbol):
        """Create X or O symbol with proper scaling"""
        size = self.cell_size - 30
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        
        if symbol == 'X':
            margin = 10
            thickness = 15
            pygame.draw.line(surf, self.X_COLOR, 
                           (margin, margin), 
                           (size-margin, size-margin), 
                           thickness)
            pygame.draw.line(surf, self.X_COLOR, 
                           (size-margin, margin), 
                           (margin, size-margin), 
                           thickness)
        else:  # 'O'
            radius = (size - 20) // 2
            thickness = 15
            pygame.draw.circle(surf, self.O_COLOR, 
                             (size//2, size//2), 
                             radius, thickness)
        
        return surf
    
    def draw_grid(self):
        """Draw the Tic Tac Toe grid"""
        # Vertical lines
        for i in range(1, 3):
            x = self.margin + i * self.cell_size
            pygame.draw.line(self.screen, self.LINE_COLOR,
                           (x, self.margin),
                           (x, self.margin + 3 * self.cell_size),
                           self.line_width)
        
        # Horizontal lines
        for i in range(1, 3):
            y = self.margin + i * self.cell_size
            pygame.draw.line(self.screen, self.LINE_COLOR,
                           (self.margin, y),
                           (self.margin + 3 * self.cell_size, y),
                           self.line_width)
    
    def draw_symbols(self):
        """Draw X and O symbols on the board"""
        for row in range(3):
            for col in range(3):
                if self.game.board[row][col] == 0:
                    continue
                
                x = self.margin + col * self.cell_size + self.cell_size//2
                y = self.margin + row * self.cell_size + self.cell_size//2
                
                if self.game.board[row][col] == 1:
                    self.screen.blit(self.x_img, 
                                    (x - self.x_img.get_width()//2, 
                                     y - self.x_img.get_height()//2))
                else:
                    self.screen.blit(self.o_img, 
                                    (x - self.o_img.get_width()//2, 
                                     y - self.o_img.get_height()//2))
    
    def draw_winning_line(self):
        """Draw the winning line if there's a winner"""
        if not self.game.winning_line:
            return
            
        line_type, index = self.game.winning_line
        color = self.WIN_COLOR
        width = self.line_width + 2
        
        if line_type == 'row':
            y = self.margin + index * self.cell_size + self.cell_size//2
            pygame.draw.line(self.screen, color,
                           (self.margin, y),
                           (self.margin + 3 * self.cell_size, y),
                           width)
        
        elif line_type == 'col':
            x = self.margin + index * self.cell_size + self.cell_size//2
            pygame.draw.line(self.screen, color,
                           (x, self.margin),
                           (x, self.margin + 3 * self.cell_size),
                           width)
        
        elif line_type == 'diag' and index == 1:
            pygame.draw.line(self.screen, color,
                           (self.margin, self.margin),
                           (self.margin + 3 * self.cell_size, 
                            self.margin + 3 * self.cell_size),
                           width)
        
        elif line_type == 'diag' and index == 2:
            pygame.draw.line(self.screen, color,
                           (self.margin + 3 * self.cell_size, self.margin),
                           (self.margin, self.margin + 3 * self.cell_size),
                           width)
    
    def draw_info_panel(self):
        """Draw the game status information panel"""
        panel_rect = pygame.Rect(0, self.height - self.info_height, 
                                self.width, self.info_height)
        pygame.draw.rect(self.screen, self.INFO_BG, panel_rect)
        
        if self.game.game_over:
            if self.game.winner:
                text = f"Player {self.game.winner} wins!"
            else:
                text = "It's a draw!"
            restart_text = self.small_font.render("Click to play again", True, (0, 0, 0))
            self.screen.blit(restart_text, 
                           (self.width//2 - restart_text.get_width()//2, 
                            self.height - self.info_height//2))
        else:
            text = f"Player {self.game.current_player}'s turn"
        
        text_surface = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, 
                       (self.width//2 - text_surface.get_width()//2, 
                        self.height - self.info_height + 20))
    
    def draw_board(self):
        """Draw the complete game board"""
        self.screen.fill(self.BG_COLOR)
        self.draw_grid()
        self.draw_symbols()
        self.draw_winning_line()
        self.draw_info_panel()
    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        if self.game.game_over:
            self.game.reset()
            return
        
        x, y = pos
        # Check if click is within the grid
        if (self.margin <= x < self.margin + 3 * self.cell_size and
            self.margin <= y < self.margin + 3 * self.cell_size):
            
            # Convert to grid coordinates
            row = (y - self.margin) // self.cell_size
            col = (x - self.margin) // self.cell_size
            
            # If it's human player's turn or not AI game
            if self.game.current_player == 1 or not self.is_ai_game:
                self.game.make_move(row, col)
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            
            self.draw_board()
            pygame.display.update()
            clock.tick(30)

if __name__ == "__main__":
    game = TicTacToeGUI(is_ai_game=False)
    game.run()
