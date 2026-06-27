import math

class AlphaBetaSolver:
    def __init__(self, rows, cols, start_pos, obstacles=None, max_depth=3):
        self.rows = rows
        self.cols = cols
        self.start_pos = start_pos
        self.obstacles = obstacles if obstacles else []
        self.max_depth = max_depth
        self.moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        self.total_cells = (rows * cols) - len(self.obstacles)

    def is_valid_move(self, r, c, visited):
        return (0 <= r < self.rows and 0 <= c < self.cols and 
                (r, c) not in visited and (r, c) not in self.obstacles)

    def get_valid_moves(self, current_pos, visited):
        r, c = current_pos
        return [(r + dr, c + dc) for dr, dc in self.moves if self.is_valid_move(r + dr, c + dc, visited)]

    def heuristic(self, pos, visited):
        # Đánh giá dựa trên số nước đi hợp lệ tiếp theo (càng ít càng dễ bị kẹt -> điểm thấp)
        return len(self.get_valid_moves(pos, visited))

    def alpha_beta(self, current_pos, visited, depth, alpha, beta, is_maximizing):
        # Điều kiện dừng: đạt độ sâu tối đa hoặc đã đi hết bàn cờ
        if depth == 0 or len(visited) == self.total_cells:
            return self.heuristic(current_pos, visited), current_pos

        valid_moves = self.get_valid_moves(current_pos, visited)
        
        # Nếu không còn đường đi
        if not valid_moves:
            return -1000 if is_maximizing else 1000, current_pos

        best_move = valid_moves[0]

        if is_maximizing:
            max_eval = -math.inf
            for move in valid_moves:
                visited.append(move)
                eval_score, _ = self.alpha_beta(move, visited, depth - 1, alpha, beta, False)
                visited.pop()

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break # Cắt tỉa Beta
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in valid_moves:
                visited.append(move)
                eval_score, _ = self.alpha_beta(move, visited, depth - 1, alpha, beta, True)
                visited.pop()

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break # Cắt tỉa Alpha
            return min_eval, best_move

    def solve(self):
        visited = [self.start_pos]
        current_pos = self.start_pos
        visited_nodes_count = 1

        yield visited.copy(), visited_nodes_count, False

        while len(visited) < self.total_cells:

            valid_moves = self.get_valid_moves(current_pos, visited)

            if not valid_moves:
                yield visited.copy(), visited_nodes_count, False
                return

            _, next_move = self.alpha_beta(
                current_pos,
                visited,
                self.max_depth,
                -math.inf,
                math.inf,
                True
            )

            visited.append(next_move)
            current_pos = next_move
            visited_nodes_count += 1

            if len(visited) == self.total_cells:
                yield visited.copy(), visited_nodes_count, True
                return

            yield visited.copy(), visited_nodes_count, False

        yield visited.copy(), visited_nodes_count, False