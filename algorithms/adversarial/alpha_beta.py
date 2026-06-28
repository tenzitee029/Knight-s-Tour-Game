class AlphaBetaSolver:
    def __init__(self, rows, cols, start_pos, obstacles=None):
        self.rows = rows
        self.cols = cols
        self.start_pos = start_pos
        # Lưu lại các vật cản tĩnh (ô bị hỏng ban đầu)
        self.static_obstacles = obstacles if obstacles else [] 
        
        self.total_cells = rows * cols
        # Luật 6: MAX thắng khi đạt >= 50%
        self.win_condition = self.total_cells / 2  
        self.moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

    def is_valid_knight_move(self, r, c, visited, obstacles):
        return (0 <= r < self.rows and 0 <= c < self.cols and 
                (r, c) not in visited and (r, c) not in obstacles)

    def get_max_moves(self, current_pos, visited, obstacles):
        r, c = current_pos
        valid_moves = [(r + dr, c + dc) for dr, dc in self.moves 
                       if self.is_valid_knight_move(r + dr, c + dc, visited, obstacles)]
        
        # TỐI ƯU HÓA ALPHA-BETA CHO MAX:
        # Sắp xếp các nước đi giảm dần theo số lượng lựa chọn tiếp theo.
        # MAX muốn tối đa hóa không gian, duyệt nước đi tốt trước giúp cắt tỉa Beta nhanh hơn.
        valid_moves.sort(key=lambda move: len([
            1 for dr, dc in self.moves 
            if self.is_valid_knight_move(move[0] + dr, move[1] + dc, visited + [move], obstacles)
        ]), reverse=True)
        
        return valid_moves
    def solve(self):
        """
        Generator method để Pygame gọi. Trả về tuple 3 phần tử: (visited, obstacles, done)
        """
        max_games = 100 
        
        for game_idx in range(1, max_games + 1):
            visited = [self.start_pos]
            obstacles = list(self.static_obstacles)
            current_pos = self.start_pos
            step_count = 0
            game_over = False
            max_won = False

            # Yield trạng thái ban đầu (chưa kết thúc -> False)
            yield visited, obstacles, False

            while not game_over:
                is_min_turn = (step_count % 3 == 2)
                
                if not is_min_turn:
                    # === LƯỢT CỦA MAX ===
                    score, best_move = self.alphabeta(
                        current_pos, visited, obstacles, step_count, 
                        depth=4, alpha=-float('inf'), beta=float('inf')
                    )
                    
                    if not best_move:
                        game_over = True
                        max_won = False
                        break
                        
                    visited.append(best_move)
                    current_pos = best_move
                    
                    if len(visited) >= self.win_condition:
                        game_over = True
                        max_won = True
                        # MAX thắng -> ván game kết thúc -> True
                        yield visited, obstacles, True
                        break
                    else:
                        # Vẫn đang chơi -> False
                        yield visited, obstacles, False
                else:
                    # === LƯỢT CỦA MIN ===
                    score, best_block = self.alphabeta(
                        current_pos, visited, obstacles, step_count, 
                        depth=3, alpha=-float('inf'), beta=float('inf')
                    )
                    
                    if best_block:
                        obstacles.append(best_block)
                        # Vẫn đang chơi -> False
                        yield visited, obstacles, False
                
                step_count += 1

            # Dừng vòng lặp lớn nếu MAX thắng
            if max_won:
                break
            
            # Nếu MAX thua, vòng lặp tự động chạy lại ván mới.
            # Có thể báo kết thúc ván thua trước khi sang ván mới
            if not max_won:
                yield visited, obstacles, True
        
        for game_idx in range(1, max_games + 1):
            # Khởi tạo trạng thái cho ván mới
            visited = [self.start_pos]
            obstacles = list(self.static_obstacles)
            current_pos = self.start_pos
            step_count = 0
            game_over = False
            max_won = False

            # Yield trạng thái ban đầu lên UI
            yield visited, obstacles

            while not game_over:
                # Luật 3: MIN hành động sau mỗi 2 lượt MAX (0,1: MAX | 2: MIN)
                is_min_turn = (step_count % 3 == 2)
                
                if not is_min_turn:
                    # === LƯỢT CỦA MAX ===
                    score, best_move = self.alphabeta(
                        current_pos, visited, obstacles, step_count, 
                        depth=4, alpha=-float('inf'), beta=float('inf')
                    )
                    
                    if not best_move:
                        # MAX hết đường đi -> Thua
                        game_over = True
                        max_won = False
                        break
                        
                    visited.append(best_move)
                    current_pos = best_move
                    
                    # Báo cho UI vẽ lại bàn cờ sau khi MAX đi
                    yield visited, obstacles
                    
                    if len(visited) >= self.win_condition:
                        # MAX đạt mục tiêu -> Thắng
                        game_over = True
                        max_won = True
                        break
                else:
                    # === LƯỢT CỦA MIN ===
                    score, best_block = self.alphabeta(
                        current_pos, visited, obstacles, step_count, 
                        depth=3, alpha=-float('inf'), beta=float('inf')
                    )
                    
                    if best_block:
                        obstacles.append(best_block)
                        
                        # Báo cho UI vẽ lại bàn cờ sau khi MIN đặt vật cản
                        yield visited, obstacles
                
                step_count += 1

            # Dừng vòng lặp lớn nếu MAX thắng
            if max_won:
                break
            
            # Nếu MAX thua, vòng lặp for sẽ tự động reset state và chạy ván tiếp theo (Luật 7).
            # Bạn có thể yield một cờ đặc biệt ở đây nếu UI cần biết để hiển thị thông báo chuyển ván.
    def get_min_moves(self, current_pos, visited, obstacles):
        min_moves = []
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in visited and (r, c) not in obstacles:
                    min_moves.append((r, c))
        
        # TỐI ƯU HÓA ALPHA-BETA CHO MIN:
        # Sắp xếp các ô trống theo khoảng cách Manhattan tới vị trí hiện tại của MAX.
        current_r, current_c = current_pos
        min_moves.sort(key=lambda pos: abs(pos[0] - current_r) + abs(pos[1] - current_c))
        
        # MIN chỉ duyệt 10 ô gần MAX nhất để chặn, tránh duyệt toàn bộ bàn cờ gây bùng nổ tổ hợp.
        return min_moves[:10]

    def evaluate(self, current_pos, visited, obstacles):
        # Hàm lượng giá: +9999 nếu MAX thắng, -9999 nếu MAX thua, 
        # Nếu chưa kết thúc, trả về số lượng nước đi tiếp theo của MAX.
        if len(visited) >= self.win_condition:
            return 9999
        
        max_options = len(self.get_max_moves(current_pos, visited, obstacles))
        if max_options == 0:
            return -9999
            
        return max_options

    def alphabeta(self, current_pos, visited, obstacles, step_count, depth, alpha, beta):
        # Trạng thái kết thúc hoặc đạt giới hạn độ sâu
        if len(visited) >= self.win_condition:
            return 9999, None
            
        if depth == 0:
            return self.evaluate(current_pos, visited, obstacles), None

        # Luật 3: MIN hành động sau mỗi 2 lượt MAX (0,1: MAX | 2: MIN | 3,4: MAX | 5: MIN...)
        is_min_turn = (step_count % 3 == 2)

        if not is_min_turn:
            # === LƯỢT CỦA MAX ===
            max_moves = self.get_max_moves(current_pos, visited, obstacles)
            if not max_moves:
                return -9999, None # MAX hết đường đi

            max_eval = -float('inf')
            best_move = None
            
            for move in max_moves:
                new_visited = visited + [move]
                eval_score, _ = self.alphabeta(move, new_visited, obstacles, step_count + 1, depth - 1, alpha, beta)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                    
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break # Cắt tỉa nhánh Beta
                    
            return max_eval, best_move

        else:
            # === LƯỢT CỦA MIN ===
            min_moves = self.get_min_moves(current_pos, visited, obstacles)
            if not min_moves:
                return self.evaluate(current_pos, visited, obstacles), None

            min_eval = float('inf')
            best_block = None
            
            for block in min_moves:
                new_obstacles = obstacles + [block]
                # Lưu ý: Lượt MIN đặt vật cản, vị trí của MAX không đổi
                eval_score, _ = self.alphabeta(current_pos, visited, new_obstacles, step_count + 1, depth - 1, alpha, beta)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_block = block
                    
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break # Cắt tỉa nhánh Alpha
                    
            return min_eval, best_block

# ==========================================
# Trình quản lý Vòng lặp Game
# ==========================================
def run_minimax_tournament(rows=8, cols=8, start_pos=(0,0)):
    max_games = 100 # Luật 8: Tối đa 100 trận
    
    for game_idx in range(1, max_games + 1):
        print(f"\n--- Bắt đầu ván thứ {game_idx} ---")
        game = AlphaBetaGame(rows, cols, start_pos)
        
        visited = [start_pos]
        obstacles = []
        current_pos = start_pos
        step_count = 0
        game_over = False
        max_won = False

        while not game_over:
            is_min_turn = (step_count % 3 == 2)
            
            if not is_min_turn:
                print(f"[Bước {step_count}] MAX đang suy nghĩ...")
                score, best_move = game.alphabeta(current_pos, visited, obstacles, step_count, depth=4, alpha=-float('inf'), beta=float('inf'))
                
                if not best_move:
                    print(f"MAX hết đường đi! Số ô đạt được: {len(visited)}/int({game.win_condition})")
                    game_over = True
                    max_won = False
                    break
                    
                visited.append(best_move)
                current_pos = best_move
                print(f"MAX đi tới: {best_move}")
                
                if len(visited) >= game.win_condition:
                    print(f"MAX đã đạt đủ 50% số ô ({len(visited)} ô). MAX CHIẾN THẮNG!")
                    game_over = True
                    max_won = True
                    break
            else:
                print(f"[Bước {step_count}] MIN đang suy nghĩ...")
                # Lượt của MIN, có thể set depth thấp hơn 1 chút để chạy nhanh hơn (vd: depth=3)
                score, best_block = game.alphabeta(current_pos, visited, obstacles, step_count, depth=3, alpha=-float('inf'), beta=float('inf'))
                
                if best_block:
                    obstacles.append(best_block)
                    print(f"MIN khóa ô: {best_block}")
                else:
                    print("MIN không thể khóa thêm ô nào.")
            
            step_count += 1

        # Luật 8: Dừng khi MAX thắng
        if max_won:
            print(f"==> KẾT THÚC: MAX thắng ở ván thứ {game_idx}! Dừng chương trình.")
            break
        else:
            # Luật 7: Tự động chơi trận mới nếu MAX thua
            print(f"==> KẾT QUẢ: MAX thua ở ván thứ {game_idx}. Chuyển sang ván mới...")

    if not max_won:
        print(f"\nĐã chạy đủ {max_games} ván mà MAX không thắng.")