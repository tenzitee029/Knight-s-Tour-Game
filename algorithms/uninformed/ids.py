from algorithms.uninformed.common import SearchBaseSolver

class IDSSolver(SearchBaseSolver):
    def solve(self):
        """Iterative Deepening Search (IDS) - Tăng dần giới hạn độ sâu (Depth Limit)"""
        visited_nodes_count = 0
        depth_limit = 0
        
        # Vòng lặp tăng dần giới hạn độ sâu cho đến tối đa số ô cờ
        while depth_limit <= self.total_cells:
            # Khởi chạy hàm tìm kiếm sâu giới hạn (DLS)
            found, visited_nodes_count, path = yield from self._depth_limited_search(
                self.start_pos, [self.start_pos], depth_limit, visited_nodes_count
            )
            
            if found:
                yield path, visited_nodes_count, True
                return
                
            depth_limit += 1
            
        yield [], visited_nodes_count, False

    def _depth_limited_search(self, curr, path, limit, node_count):
        """Hàm bổ trợ duyệt đệ quy có giới hạn độ sâu cho IDS"""
        node_count += 1
        yield path, node_count, False
        
        if len(path) == self.total_cells:
            return True, node_count, path
            
        if limit <= 0:
            return False, node_count, []
            
        r, c = curr
        for dr, dc in self.knight_moves:
            nr, nc = r + dr, c + dc
            if self.is_valid_position(nr, nc, path):
                found, node_count, res_path = yield from self._depth_limited_search(
                    (nr, nc), path + [(nr, nc)], limit - 1, node_count
                )
                if found:
                    return True, node_count, res_path
                    
        return False, node_count, []