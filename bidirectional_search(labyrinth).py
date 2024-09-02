def bidirectional_search(labyrinth):
    rows, cols = len(labyrinth), len(labyrinth[0])
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    # Find entrance and artifact positions
    entrance, artifact = None, None
    for r in range(rows):
        for c in range(cols):
            if labyrinth[r][c] == 'E':
                entrance = (r, c)
            elif labyrinth[r][c] == 'A':
                artifact = (r, c)

    if entrance is None or artifact is None:
        return "No path found."

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and labyrinth[x][y] != '#'

    def bfs(queue, visited):
        current = queue.popleft()
        r, c = current

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and (nr, nc) not in visited:
                visited[nr, nc] = (r, c)
                queue.append((nr, nc))

    start_visited = {entrance: None}
    end_visited = {artifact: None}
    start_queue = deque([entrance])
    end_queue = deque([artifact])

    while start_queue and end_queue:
        bfs(start_queue, start_visited)
        bfs(end_queue, end_visited)

        # Check for intersection
        intersection = set(start_visited.keys()) & set(end_visited.keys())
        if intersection:
            node = list(intersection)[0]
            path = [node]

            # Construct path from entrance to intersection
            while start_visited[node]:
                node = start_visited[node]
                path.append(node)
            path.reverse()

            # Construct path from intersection to artifact
            node = path[-1]
            while end_visited[node]:
                node = end_visited[node]
                path.append(node)

            return path

    return "No path found."

labyrinth = [
    ['#', '#', '#', '#'],
    ['#', 'E', '.', '#'],
    ['#', '.', '.', '#'],
    ['#', '#', '.', 'A'],
]