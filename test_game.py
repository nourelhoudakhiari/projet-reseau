import unittest
from game import TicTacToe

class TestTicTacToe(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToe()
    
    def test_initial_state(self):
        state = self.game.get_state()
        self.assertEqual(state['board'], [[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.assertEqual(state['current_player'], 1)
        self.assertFalse(state['game_over'])
        self.assertIsNone(state['winner'])
    
    def test_valid_moves(self):
        self.assertEqual(len(self.game.get_valid_moves()), 9)
        self.game.make_move(0, 0)
        self.assertEqual(len(self.game.get_valid_moves()), 8)
    
    def test_win_conditions(self):
        # Test victoire en ligne
        moves = [(0, 0), (1, 1), (0, 1), (2, 2), (0, 2)]
        for row, col in moves:
            self.game.make_move(row, col)
        state = self.game.get_state()
        self.assertTrue(state['game_over'])
        self.assertEqual(state['winner'], 1)
        self.assertEqual(state['winning_line'], ('row', 0))
        
        # Réinitialiser pour tester colonne
        self.game.reset()
        moves = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]
        for row, col in moves:
            self.game.make_move(row, col)
        state = self.game.get_state()
        self.assertEqual(state['winning_line'], ('col', 0))
        
        # Réinitialiser pour tester diagonale
        self.game.reset()
        moves = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)]
        for row, col in moves:
            self.game.make_move(row, col)
        state = self.game.get_state()
        self.assertEqual(state['winning_line'], ('diag', 1))

if __name__ == "__main__":
    unittest.main()
