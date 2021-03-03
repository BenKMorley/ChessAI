from unittest import TestCase
from chessboard.chessboard import Chessboard

class TestChessboard(TestCase):
    def test_fen_to_board(self):
        c = Chessboard()

        c.fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        print(c.board)
        self.assertFalse(True)