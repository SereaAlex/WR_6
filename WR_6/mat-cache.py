import random
import time

def generate_input(filename, num_matrices, min_rows, max_rows, min_cols, max_cols):
    with open(filename, 'w') as file:
        for _ in range(num_matrices):
            rows = random.randint(min_rows, max_rows)
            cols = random.randint(min_cols, max_cols)
            matrix = ''.join([random.choice(['0', '1']) for _ in range(rows * cols)])
            file.write(f"{rows}x{cols}:{matrix}\n")

def read_input(filename):
    matrices = []
    with open(filename, 'r') as file:
        for line in file:
            matrix_str = line.strip().split(':')[1]
            rows, cols = map(int, line.split(':')[0].split('x'))
            matrices.append((rows, cols, matrix_str))
    return matrices

def count_isolated_ones(matrix, rows, cols):
    grid = [list(map(int, matrix[i:i + cols])) for i in range(0, len(matrix), cols)]
    count = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                if (i == 0 or grid[i - 1][j] == 0) and \
                   (i == rows - 1 or grid[i + 1][j] == 0) and \
                   (j == 0 or grid[i][j - 1] == 0) and \
                   (j == cols - 1 or grid[i][j + 1] == 0):
                    count += 1
    return count

def count_clusters(matrix, rows, cols, size):
    grid = [list(map(int, matrix[i:i + cols])) for i in range(0, len(matrix), cols)]
    visited = [[False] * cols for _ in range(rows)]
    count = 0

    def dfs(row, col):
        if row < 0 or row >= rows or col < 0 or col >= cols or visited[row][col] or grid[row][col] == 0:
            return 0
        visited[row][col] = True
        cluster_size = 1
        cluster_size += dfs(row - 1, col)
        cluster_size += dfs(row + 1, col)
        cluster_size += dfs(row, col - 1)
        cluster_size += dfs(row, col + 1)
        return cluster_size

    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and grid[i][j] == 1:
                cluster_size = dfs(i, j)
                if cluster_size == size:
                    count += 1
    return count

def process_matrices(matrices, cache_size):
    cache = {}
    results = []
    for rows, cols, matrix_str in matrices:
        if matrix_str in cache:
            isolated_ones, clusters_two, clusters_three = cache[matrix_str]
        else:
            isolated_ones = count_isolated_ones(matrix_str, rows, cols)
            clusters_two = count_clusters(matrix_str, rows, cols, 2)
            clusters_three = count_clusters(matrix_str, rows, cols, 3)
            if len(cache) >= cache_size:
                cache.pop(next(iter(cache)))  # Remove the oldest entry in the cache
            cache[matrix_str] = (isolated_ones, clusters_two, clusters_three)
        results.append((isolated_ones, clusters_two, clusters_three))
    return results

def process_matrices_without_cache(matrices):
    results = []
    for rows, cols, matrix_str in matrices:
        isolated_ones = count_isolated_ones(matrix_str, rows, cols)
        clusters_two = count_clusters(matrix_str, rows, cols, 2)
        clusters_three = count_clusters(matrix_str, rows, cols, 3)
        results.append((isolated_ones, clusters_two, clusters_three))
    return results

def write_output(filename, results):
    with open(filename, 'w') as file:
        for result in results:
            file.write(' '.join(map(str, result)) + '\n')

if __name__ == "__main__":
    # Generate a large input file for testing
    generate_input("mat.in", 100000, 5, 5, 5, 5)
    
    # Read matrices from the input file
    matrices = read_input("mat.in")
    
    # Process matrices with caching
    start_time = time.time()
    results_with_cache = process_matrices(matrices, cache_size=1000)
    with_cache_duration = time.time() - start_time
    
    # Write results to output file
    write_output("mat.out", results_with_cache)
    
    # Process matrices without caching for comparison
    start_time = time.time()
    results_without_cache = process_matrices_without_cache(matrices)
    without_cache_duration = time.time() - start_time
    
    # Log the duration of both implementations
    with open("task-mat-cache-testing.txt", 'w') as log_file:
        log_file.write(f"With cache duration: {with_cache_duration} seconds\n")
        log_file.write(f"Without cache duration: {without_cache_duration} seconds\n")
