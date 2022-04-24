from move import Move
from copy import deepcopy

# reference for weight:
# http://dhconnelly.com/paip-python/docs/paip/othello.html#localmax

WEIGHT = [[120, -20,  20,   5,   5,  20, -20, 120],
          [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
          [20,   -5,  15,   3,   3,  15,  -5,  20],
          [5,    -5,   3,   3,   3,   3,  -5,   5],
          [5,    -5,   3,   3,   3,   3,  -5,   5],
          [20,   -5,  15,   3,   3,  15,  -5,  20],
          [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
          [120, -20,  20,   5,   5,  20, -20, 120]]

BEST_TILE = max(max(WEIGHT))
WORST_TILE = min(min(WEIGHT))
DEPTH = 3
INIT_SCORE = -1000
WHITE = 225
BLACK = 0


class Computer(Move):
    """Class for computer moves"""

    def first_two_tile(self):
        """Computer place down first two tiles"""
        self.add_disk(self.board.UP, self.board.LEFT)
        self.add_disk(self.board.DOWN, self.board.RIGHT)

    def greedy(self, tile):
        """Greedy algorithm to determine the best move for computer"""
        # the score is simlply amount of tile it can flip
        swap = self.tiles_to_swap(tile)
        raw_score = len(swap)
        return raw_score

    def weight_greedy(self, tile):
        """Weighted greedy algorithm to determine the best move for computer"""
        swap = self.tiles_to_swap(tile)
        # multiple the newly placed tile with weight
        score = WEIGHT[tile.row][tile.column]

        # multiple all the flipping tiles with weight
        for t in swap:
            score += WEIGHT[t.row][t.column]

        return score

    def minimax(self, tile, depth, board, score):
        """Minimax algorithm combines with weighted greedy"""

        # temper board to simulate the move on
        player = Move(BLACK, board)
        computer = Move(WHITE, board)

        # when depth is zero (1), return to return the final score
        if depth == 0:
            return

        # computer make the move on the input tile
        computer.one_full_move(tile)

        # calculate the score is depth is one (1)
        if depth == 1:
            temp_score = self.minimax_score(board)
            if temp_score > score:
                score = temp_score
                self.score_list.append(score)

        # player make move
        for tp in board.tiles:
            if player.is_valid_move(tp):
                player.one_full_move(tp)

                # for valid tiles, continue recursion with depth = depth -1
                for tc in board.tiles:
                    if computer.is_valid_move(tc):
                        self.minimax(tc, depth - 1, board, score)

        # score might be empty if no valid tile exist during recursion,
        # to avoid error, only return non-empty list
        if self.score_list:
            return max(self.score_list)
        else:
            return INIT_SCORE

    def minimax_score(self, temp_board_name):
        """Calculate the final score at the end of minimax recursion"""
        black_total = 0
        white_total = 0
        for tile in temp_board_name.tiles:
            if tile.color == BLACK:
                black_total += 1
            elif tile.color == WHITE:
                white_total += 1

        score = white_total - black_total

        return score

    def best_move(self, difficulty="hard"):
        """Find the best move for computer"""
        all_move = {}
        score = 0

        for tile in self.board.tiles:
            if self.is_valid_move(tile):
                if difficulty == "hard":
                    # the computer always take the best tile and
                    # avoid the worst tile
                    if WEIGHT[tile.row][tile.column] == BEST_TILE:
                        score = BEST_TILE
                    elif WEIGHT[tile.row][tile.column] == WORST_TILE:
                        score = WORST_TILE
                    # if neither best or worst can happen, it does a recursion
                    # to find the tile that will result in optimal result in
                    # the future
                    else:
                        self.score_list = []
                        temp_board = deepcopy(self.board)
                        score = self.minimax(tile, DEPTH, temp_board,
                                             INIT_SCORE)
                elif difficulty == "median":
                    score = self.weight_greedy(tile)
                else:
                    score = self.greedy(tile)
                all_move[tile] = score

        # sort the dictionary with all score
        sorted_move = sorted(
            all_move.items(),
            key=lambda x: x[1],
            reverse=True
        )

        best_tile = sorted_move[0][0]
        tiles_to_swap = self.tiles_to_swap(best_tile)
        return (best_tile, tiles_to_swap)
