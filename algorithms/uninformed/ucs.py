import heapq
from algorithms.uninformed.common import SearchBaseSolver

class UCSSolver(SearchBaseSolver):
    def solve(self):
        """Uniform Cost Search (UCS) sử dụng Priority Queue
        Với Mã Đi Tuần, chi phí mỗi bước nhảy đồng nhất bằng 1.
        """
        # Trạng thái lưu vào heapq: (chi_phí, vị_trí_hiện_tại, danh_sách_đường_đi)
        p_queue = [(0, self.start_pos, [self.start_pos])]
        visited_nodes_count = 0

        while p_queue:
            cost, curr, path = heapq.heappop(p_queue)
            visited_nodes_count += 1
            
            yield path, visited_nodes_count, False

            if len(path) == self.total_cells:
                yield path, visited_nodes_count, True
                return

            r, c = curr
            for dr, dc in self.knight_moves:
                nr, nc = r + dr, c + dc
                if self.is_valid_position(nr, nc, path):
                    # Chi phí tăng thêm 1 đơn vị cho mỗi nước đi
                    heapq.heappush(p_queue, (cost + 1, (nr, nc), path + [(nr, nc)]))
                    
        yield [], visited_nodes_count, False