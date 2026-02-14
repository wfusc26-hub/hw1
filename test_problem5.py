import unittest

from problem5 import shortest_path_with_teleports, solve_maze


def _find_symbol(maze, symbol):
    for r, row in enumerate(maze):
        for c, cell in enumerate(row):
            if cell == symbol:
                return (r, c)
    raise ValueError(f"Missing symbol: {symbol}")


class TestProblem5(unittest.TestCase):
    def assert_valid_path(self, maze, path):
        self.assertIsNotNone(path, "Expected a path but got None.")
        assert path is not None

        contains_marked_start = any("S" in row for row in maze)
        contains_marked_exit = any("E" in row for row in maze)

        if contains_marked_start or contains_marked_exit:
            start = _find_symbol(maze, "S")
            exit_cell = _find_symbol(maze, "E")
        else:
            start = (0, 0)
            exit_cell = (len(maze) - 1, len(maze[0]) - 1)

        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], exit_cell)

        rows = len(maze)
        cols = len(maze[0])

        for r, c in path:
            self.assertTrue(0 <= r < rows and 0 <= c < cols)
            self.assertNotIn(maze[r][c], {"#", "1"})

        for (r1, c1), (r2, c2) in zip(path, path[1:]):
            manhattan = abs(r1 - r2) + abs(c1 - c2)
            if manhattan == 1:
                continue

            self.assertEqual(
                maze[r1][c1],
                "T",
                "Non-adjacent moves are only valid from a teleport.",
            )
            self.assertEqual(
                maze[r2][c2],
                "T",
                "Non-adjacent moves are only valid to a teleport.",
            )

    def test_shortest_path_without_teleport(self):
        maze = [
            "S..",
            ".#.",
            "..E",
        ]
        path = shortest_path_with_teleports(maze)
        self.assert_valid_path(maze, path)
        self.assertEqual(len(path) - 1, 4)  # 4 moves

    def test_teleport_required(self):
        maze = [
            "S.T",
            "###",
            "T.E",
        ]
        path = shortest_path_with_teleports(maze)
        self.assert_valid_path(maze, path)
        self.assertEqual(len(path) - 1, 5)  # includes one teleport move

        used_teleport = any(
            abs(r1 - r2) + abs(c1 - c2) > 1
            for (r1, c1), (r2, c2) in zip(path, path[1:])
        )
        self.assertTrue(used_teleport, "Expected teleport usage in the path.")

    def test_returns_none_when_no_path(self):
        maze = [
            "S#E",
        ]
        self.assertIsNone(shortest_path_with_teleports(maze))

    def test_legacy_basic_01_grid_is_supported(self):
        maze = [
            "000",
            "010",
            "000",
        ]
        path = shortest_path_with_teleports(maze)
        self.assert_valid_path(maze, path)
        self.assertEqual(len(path) - 1, 4)  # from (0,0) to (2,2)

    def test_legacy_blocked_start_or_exit_returns_none(self):
        self.assertIsNone(shortest_path_with_teleports(["1"]))
        self.assertIsNone(shortest_path_with_teleports(["01", "01"]))

    def test_alias_matches_main_solver(self):
        maze = [
            "000",
            "010",
            "000",
        ]
        self.assertEqual(solve_maze(maze), shortest_path_with_teleports(maze))


if __name__ == "__main__":
    unittest.main()
