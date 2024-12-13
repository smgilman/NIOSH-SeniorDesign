class IdentifyNeighbors:
    '''
    IdentifyNeighbors applies the nearest neighbor algorithm to determine a node's nearest neighbor.

    Authors:
        Hermann Ndeh
        Misk Hussain
        Sharon Gilman
    '''

    def __init__(self, grid_dimensions, grid_numbers):
        '''
        Initialize the class with grid dimensions and grid numbers.

        Parameters:
            grid_dimensions (tuple): (width, height) of the entire grid area.
            grid_numbers (int): Total number of grids.
        '''

        self.grid_dimensions = grid_dimensions
        self.grid_numbers = grid_numbers

    def get_adjacent_grids(self, n, b):
        '''
        Get the grid numbers adjacent to the grid labeled n in a b x b grid.
        """
        Get the grid numbers adjacent to the grid labeled `n` in a `b x b` grid,
        including diagonal neighbors.

        Parameters:
            n (int): The grid number (1-indexed).
            b (int): The size of the grid (b x b).

        Returns:
            set: A set of adjacent grid numbers.
        '''

        adjacent = set()

        # Check direct neighbors
        if n > b:  # Top
            adjacent.add(n - b)
        if n <= b * (b - 1):  # Bottom
            adjacent.add(n + b)
        if (n - 1) % b != 0:  # Left
            adjacent.add(n - 1)
        if n % b != 0:  # Right
            adjacent.add(n + 1)

        # Check diagonal neighbors
        if n > b and (n - 1) % b != 0:  # Top-left
            adjacent.add(n - b - 1)
        if n > b and n % b != 0:  # Top-right
            adjacent.add(n - b + 1)
        if n <= b * (b - 1) and (n - 1) % b != 0:  # Bottom-left
            adjacent.add(n + b - 1)
        if n <= b * (b - 1) and n % b != 0:  # Bottom-right
            adjacent.add(n + b + 1)

        return adjacent

    def compute_connected_set(self, start, b, valid_numbers):
        '''
        Compute the full set of connected grids starting from a specific grid, filtering to include only numbers in `valid_numbers`.
        """
        Compute the set of connected grids starting from a specific grid,
        including only numbers in `valid_numbers`.

        Parameters:
            start (int): The starting grid number.
            b (int): The size of the grid (b x b).
            valid_numbers (set): Set of valid grid numbers to include.

        Returns:
            set: A set of connected grids starting from `start` that are in `valid_numbers`.
        '''

        visited = set()  # Track visited grids
        to_visit = {start}  # Start with the given grid
        
        visited = set()
        to_visit = {start}

        while to_visit:
            current = to_visit.pop()
            if current not in visited:
                visited.add(current)
                neighbors = self.get_adjacent_grids(current, b)
                to_visit.update(neighbors & valid_numbers - visited)

        return visited

    def compute_cluster_centers(self, clusters, b):
        '''
        Compute the center point for each cluster of connected grids.

        Parameters:
            clusters (list[set]): List of sets of grid numbers representing clusters.
            b (int): The size of the grid (b x b).

        Returns:
            dict: A dictionary mapping cluster indices (starting from 1) to their center coordinates.
                Example: {1: (x_center, y_center), 2: (x_center, y_center), ...}
        '''

        grid_width, grid_height = self.grid_dimensions
        cell_width = grid_width / b
        cell_height = grid_height / b
        cluster_centers = {}

        for i, cluster in enumerate(clusters, start=1):
            x_coords = []
            y_coords = []

            for grid in cluster:
                row = (grid - 1) // b  # Row index (0-indexed)
                col = (grid - 1) % b  # Column index (0-indexed)
                center_x = (col + 0.5) * cell_width
                center_y = (row + 0.5) * cell_height
                x_coords.append(center_x)
                y_coords.append(center_y)

            cluster_centers[i] = (
                sum(x_coords) / len(x_coords),
                sum(y_coords) / len(y_coords),
            )

        return cluster_centers
