import unittest

from problem5 import shortest_path_with_teleports


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

        start = _find_symbol(maze, "S")
        exit_cell = _find_symbol(maze, "E")
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], exit_cell)

        rows = len(maze)
        cols = len(maze[0])

        for r, c in path:
            self.assertTrue(0 <= r < rows and 0 <= c < cols)
            self.assertNotEqual(maze[r][c], "#")

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


if __name__ == "__main__":
    unittest.main()
