from algorithms.local_search.stochastic_hill_climbing import StochasticHillClimbingSolver


class RandomRestartHillClimbingSolver(StochasticHillClimbingSolver):
    """Random Restart Hill Climbing cho bài toán Knight's Tour.

    Thuật toán chạy Stochastic Hill Climbing nhiều lần. Khi một lần chạy bị kẹt
    ở cực trị cục bộ, thuật toán khởi động lại từ trạng thái ban đầu và giữ lại
    đường đi tốt nhất đã tìm được.
    """

    MAX_RESTARTS = 50

    def solve(self):
        total_visited_nodes = 0
        best_path = [self.start_pos]

        for _ in range(self.MAX_RESTARTS):
            attempt_generator = self.run_one_attempt()
            final_path = [self.start_pos]
            previous_attempt_nodes = 0

            try:
                while True:
                    path, attempt_nodes, done = next(attempt_generator)
                    final_path = path

                    node_delta = max(0, attempt_nodes - previous_attempt_nodes)
                    previous_attempt_nodes = attempt_nodes
                    total_visited_nodes += node_delta

                    if len(path) > len(best_path):
                        best_path = path.copy()

                    yield path.copy(), total_visited_nodes, False

            except StopIteration as stop_result:
                if stop_result.value:
                    final_path, attempt_nodes = stop_result.value
                    node_delta = max(0, attempt_nodes - previous_attempt_nodes)
                    total_visited_nodes += node_delta

            if len(final_path) > len(best_path):
                best_path = final_path.copy()

            if len(best_path) == self.total_cells:
                yield best_path.copy(), total_visited_nodes, True
                return

        yield best_path.copy(), total_visited_nodes, True
