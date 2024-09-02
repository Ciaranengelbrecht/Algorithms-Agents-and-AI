def nearest_neighbors(N, distances):
    # Finds nearest unvisited neighbor from a city
    def get_nearest_neighbor(city, unvisited_cities):
        min_distance = float('inf')
        nearest_city = None
        for neighbor, distance in enumerate(distances[city]):
            if neighbor in unvisited_cities and distance < min_distance:
                min_distance = distance
                nearest_city = neighbor
        return nearest_city, min_distance
        
    # Start at the castle, initialise path and unvisited cities
    unvisited_cities = set(range(1, N))
    current_city = 0  
    path = [current_city]
    total_distance = 0
    
    # Loop until all cities visited
    # Find nearest unvisited neighbor from the current city
    # Add nearest city to the path and update total distance
    # Remove nearest city from set of unvisited cities
    # Move to nearest city for the next iteration
    while unvisited_cities:
        nearest_city, distance = get_nearest_neighbor(current_city, unvisited_cities)
        path.append(nearest_city)
        total_distance += distance
        unvisited_cities.remove(nearest_city)
        current_city = nearest_city
    # Return to the castle then update total distance
    path.append(0)  
    total_distance += distances[current_city][0]
    
    return path, total_distance

def optimize_tour_with_2opt(N, distance_matrix):
    # Calculate the total distance of a path
    def calculate_total_distance(path):
        total = 0
        for i in range(N):
            total += distance_matrix[path[i - 1]][path[i]]
        return total

    # Swap two edges and check if it improves path
    def two_opt_swap(path, i, j):
        new_path = path[:i] + path[i:j + 1][::-1] + path[j + 1:]
        return new_path, calculate_total_distance(new_path)

    # Initialize the initial path using NN
    initial_path, total_distance = nearest_neighbors(N, distance_matrix)

    improved = True
    while improved:
        improved = False
        for i in range(1, N - 2):
            for j in range(i + 1, N - 1):
                new_path, new_distance = two_opt_swap(initial_path, i, j)
                if new_distance < total_distance:
                    initial_path = new_path
                    total_distance = new_distance
                    improved = True

    return initial_path, total_distance

