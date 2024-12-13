import numpy as np
import matplotlib.pyplot as plt

class DroneSurvey:
    '''
    DroneSurvey initializes a grid and assigns drones to subgrids if there is a potential hazard that has been identified. The drones' path 
    is created using the Lawnmower Algorithm (an inefficient path planning algorithm but ensures 100% coverage of the construction site). 

    Authors:
        Hermann Ndeh
        Misk Hussain
        Sharon Gilman
    '''

    def __init__(self, grid_size=50, subgrid_size=5, num_drones=1):
        '''
        Initialize the class with the grid size, subgrid size, and the given number of drones.

        Parameters:
            grid_size (int): The size of the grid.
            subgrid_size (int): The size of the subgrid.
            num_drones (int): The number of drones being used.
        '''

        self.grid_size = grid_size
        self.subgrid_size = subgrid_size
        self.num_drones = num_drones
        self.grid, self.subgrids = self.grid_init()
        self.drone_paths = self.assign_drones_to_grid()
        
    def grid_init(self):
        '''
        Initialize the main grid and divides it into subgrids.

        Returns:
            numpy array: The grid.
            numpy array: The subgrids of the main grid.
        '''

        grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        subgrid_dim = self.grid_size // self.subgrid_size
        # Reshape grid into subgrids
        subgrids = grid.reshape(subgrid_dim, self.subgrid_size, subgrid_dim, self.subgrid_size).swapaxes(1, 2)
        return grid, subgrids

    def assign_drones_to_grid(self):
        '''
        Assigns drones to evenly spaced areas of the grid and generates their paths using the Lawnmower Algorithm.

        Returns:
            set: A set of all the drone paths.
        '''

        grid_width_per_drone = self.grid_size // self.num_drones
        drone_paths = {}

        for drone_id in range(self.num_drones):
            start_col = drone_id * grid_width_per_drone
            end_col = start_col + grid_width_per_drone
            path = self.generate_lawnmower_path(start_col, end_col)
            drone_paths[drone_id] = path

        return drone_paths

    def generate_lawnmower_path(self, start_col, end_col):
        '''
        Generates a Lawnmower path for a drone to ensure it covers the assigned grid area.

        Parameters:
            start_col (int): the starting column of the drone's path.
            end_col (int): the ending column of the drone's path.
        
        Returns:
            list: The Lawnmower path for a single drone.
        '''

        path = []
        for row in range(self.grid_size):
            if row % 2 == 0:
                # Traverse from left to right
                path.extend([(row, col) for col in range(start_col, end_col)])
            else:
                # Traverse from right to left
                path.extend([(row, col) for col in range(end_col - 1, start_col - 1, -1)])
        return path

    def plot_paths(self):
        '''
        Plots each drone path and the smaller subgrids on the grid using matplotlib.
        '''

        plt.figure(figsize=(10, 10))
        # Set the origin to 'lower' to invert the y-axis
        plt.imshow(self.grid, cmap='Greys', origin='lower')

        # Plot each drone's path
        for drone_id, path in self.drone_paths.items():
            path = np.array(path)
            plt.plot(path[:, 1], path[:, 0], label=f'Drone {drone_id + 1}')

        # Plot the smaller subgrids (5x5)
        num_grids_per_row = self.grid_size // self.subgrid_size
        for i in range(num_grids_per_row):
            for j in range(num_grids_per_row):
                rect = plt.Rectangle((j * self.subgrid_size, i * self.subgrid_size), 
                                     self.subgrid_size, self.subgrid_size, 
                                     linewidth=1, edgecolor='r', facecolor='none')
                plt.gca().add_patch(rect)

        plt.title('Drone Survey Paths and Smaller 5x5 Grids')
        plt.legend()
        plt.grid(True)
        plt.show()

    def print_paths(self):
        '''
        Displays each path a drone follows, including its start point, end point, and the total grids each drone has passed through their 
        flyover.
        '''

        for drone_id, path in self.drone_paths.items():
            start_point = path[0]
            end_point = path[-1]
            num_grids = len(path)

            print(f"Drone {drone_id + 1} path:")
            print(f"  Start point: {start_point}")
            print(f"  End point: {end_point}")
            print(f"  Number of grids passed: {num_grids}")
            print()  

if __name__ == "__main__":
    num_drones = 6
    survey = DroneSurvey(grid_size=50, num_drones=num_drones)
    survey.print_paths() 
    survey.plot_paths()