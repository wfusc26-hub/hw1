"""Recursive shortest-path solver for basic and advanced maze formats.

Advanced symbols:
- 'S': start
- 'E': exit
- 'T': teleport pad
- '#': wall

Basic format compatibility:
- '0': open
- '1': wall
- if S/E are not present, start is top-left and exit is bottom-right
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

Coordinate = Tuple[int, int]


def shortest_path_with_teleports(maze: Sequence[str]) -> Optional[List[Coordinate]]:
    """Return the shortest path through a maze, or None if no path exists.

    Path output is a list of (row, col) coordinates from start to exit.

    Supported input modes:
    - Advanced: explicit S and E markers (+ optional T teleports and # walls)
    - Basic: 0/1 grid with implicit start=(0,0), exit=(rows-1, cols-1)

    Movement cost:
    - Adjacent step (up/right/down/left): 1
    - Teleport from one T to any other T: 1
    """

    if not maze:
        raise ValueError("Maze must not be empty.")

    width = len(maze[0])
    if width == 0:
        raise ValueError("Maze rows must not be empty.")
    if any(len(row) != width for row in maze):
        raise ValueError("Maze must be rectangular.")

    start_marked: Optional[Coordinate] = None
    exit_marked: Optional[Coordinate] = None
    teleports: List[Coordinate] = []

    for r, row in enumerate(maze):
        for c, cell in enumerate(row):
            if cell == "S":
                if start_marked is not None:
                    raise ValueError("Maze must contain exactly one start 'S'.")
                start_marked = (r, c)
            elif cell == "E":
                if exit_marked is not None:
                    raise ValueError("Maze must contain exactly one exit 'E'.")
                exit_marked = (r, c)
            elif cell == "T":
                teleports.append((r, c))

    if (start_marked is None) != (exit_marked is None):
        raise ValueError("Maze must contain both 'S' and 'E', or neither.")

    start = start_marked if start_marked is not None else (0, 0)
    exit_cell = exit_marked if exit_marked is not None else (len(maze) - 1, width - 1)

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    parents: Dict[Coordinate, Optional[Coordinate]] = {start: None}
    teleports_expanded = False

    def in_bounds(r: int, c: int) -> bool:
        return 0 <= r < len(maze) and 0 <= c < width

    def is_walkable(r: int, c: int) -> bool:
        return maze[r][c] not in {"#", "1"}

    if not is_walkable(*start) or not is_walkable(*exit_cell):
        return None

    def reconstruct_path() -> List[Coordinate]:
        path: List[Coordinate] = []
        current: Optional[Coordinate] = exit_cell
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()
        return path

    def search_level(frontier: List[Coordinate]) -> Optional[List[Coordinate]]:
        nonlocal teleports_expanded

        if not frontier:
            return None
        if exit_cell in frontier:
            return reconstruct_path()

        next_frontier: List[Coordinate] = []

        for row, col in frontier:
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                candidate = (nr, nc)

                if not in_bounds(nr, nc):
                    continue
                if not is_walkable(nr, nc):
                    continue
                if candidate in parents:
                    continue

                parents[candidate] = (row, col)
                next_frontier.append(candidate)

            if maze[row][col] == "T" and len(teleports) > 1 and not teleports_expanded:
                # T cells form a complete graph; expanding once is enough.
                teleports_expanded = True
                for t_row, t_col in teleports:
                    target = (t_row, t_col)
                    if target == (row, col) or target in parents:
                        continue
                    parents[target] = (row, col)
                    next_frontier.append(target)

        return search_level(next_frontier)

    return search_level([start])


def solve_maze(maze: Sequence[str]) -> Optional[List[Coordinate]]:
    """Backward-compatible alias for the maze solver."""
    return shortest_path_with_teleports(maze)


def path_to_directions(path: Sequence[Coordinate]) -> List[str]:
    """Convert a coordinate path into movement directions.

    Normal moves are one of: U, R, D, L.
    Teleport moves are encoded as TELEPORT.
    """

    if not path:
        return []

    move_map = {
        (-1, 0): "U",
        (0, 1): "R",
        (1, 0): "D",
        (0, -1): "L",
    }

    directions: List[str] = []
    for (r1, c1), (r2, c2) in zip(path, path[1:]):
        directions.append(move_map.get((r2 - r1, c2 - c1), "TELEPORT"))
    return directions


SAMPLE_INPUTS: List[Tuple[str, List[str]]] = [
    (
        "Input 1 (simple S->E, no teleports)",
        [
            "S00",
            "110",
            "00E",
        ],
    ),
    (
        "Input 2 (teleports help bypass a wall)",
        [
            "S1T001",
            "111101",
            "0000T1",
            "101111",
            "10000E",
        ],
    ),
    (
        "Input 3 (multiple teleports; choose best T)",
        [
            "S001T0",
            "110110",
            "T00010",
            "0111T0",
            "00010E",
        ],
    ),
]


def run_sample_inputs() -> None:
    """Run the three provided Problem 5 test inputs and print outputs."""
    for label, maze in SAMPLE_INPUTS:
        path = shortest_path_with_teleports(maze)
        print(label)
        for row in maze:
            print(row)
        print("Path:", path)
        if path is None:
            print("Moves: None")
            print("Directions: None")
        else:
            print("Moves:", len(path) - 1)
            print("Directions:", path_to_directions(path))
        print()


if __name__ == "__main__":
    run_sample_inputs()
