def bidirectional_search(labyrinth):
    def is_valid(row, col):
        return 0 <= row < len(labyrinth) and 0 <= col < len(labyrinth[0]) and labyrinth[row][col] != '#'

    def get_neighbors(row, col):
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        return [(r, c) for r, c in neighbors if is_valid(r, c)]

    def bfs(start, target, visited, parent):
        queue = deque()
        queue.append(start)
        visited[start[0]][start[1]] = True

        while queue:
            current = queue.popleft()

            if current == target:
                return True

            for neighbor in get_neighbors(current[0], current[1]):
                if not visited[neighbor[0]][neighbor[1]]:
                    queue.append(neighbor)
                    visited[neighbor[0]][neighbor[1]] = True
                    parent[neighbor] = current

        return False

    rows, cols = len(labyrinth), len(labyrinth[0])
    start, end = None, None

    # Find the starting E and ending E positions
    for row in range(rows):
        for col in range(cols):
            if labyrinth[row][col] == 'E':
                start = (row, col)
            elif labyrinth[row][col] == 'A':
                end = (row, col)

    visited_start = [[False] * cols for _ in range(rows)]
    visited_end = [[False] * cols for _ in range(rows)]
    parent_start = {}
    parent_end = {}

    if bfs(start, end, visited_start, parent_start) or bfs(end, start, visited_end, parent_end):
        if start == end:
            return [start]  # Handle case where start and end are equal
        path = [end]
        while path[-1] != start:
            current = path[-1]
            if current not in parent_start:
                return "No path found."
            path.append(parent_start[current])
        path.reverse()
        return path
    else:
        return "No path found."

labyrinth = [
    ['#', '#', '#', '#'],
    ['#', 'E', '.', '#'],
    ['#', '.', '.', '#'],
    ['#', '#', '.', 'A'],
]

result = bidirectional_search(labyrinth)
