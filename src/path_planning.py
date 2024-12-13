import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as animation
import io
from PIL import Image
import random


class ClusterPathPlanner:
    '''
    ClusterPathPlanner defines a drone's path by using the nearest neighbor algorithm. The paths are presented to the user in the terminal 
    and displayed on an image using matplotlib.

    Authors:
        Hermann Ndeh
        Misk Hussain
        Sharon Gilman
    '''

    def __init__(self, centroids, num_groups):
        '''
        Initialize the class with the given centroids and number of groups of drones.

        Parameters:
            centroids (list): The coordinates of each node. Used to determine the center of a node.
            num_groups (int): The number of groups of drones to deploy.
        '''

        self.centroids = centroids
        self.num_groups = num_groups
        self.groups = None
        self.paths = None

    def split_clusters(self):
        '''
        Converts the centroid coordinates to an array so the nearest neighbor algorithm can be run on the file.

        Returns:
            set: A set of the groups of red subgrids contained in the image.
        '''

        # Convert centroid coordinates to an array for KMeans
        coords = np.array(list(self.centroids.values()))
        
        kmeans = KMeans(n_clusters=self.num_groups, random_state=42, n_init=10)
        labels = kmeans.fit_predict(coords)
        
        self.groups = {i + 1: [] for i in range(self.num_groups)}  # Group labels start from 1
        for node, label in zip(self.centroids.keys(), labels):
            self.groups[label + 1].append(node)  # Adjust label to start from 1
        
        return self.groups

    def nearest_neighbor_path(self, group):
        '''
        Performs the nearest neighbor algorithm to determine a group of red subgrid's nearest neighbor.

        Parameters:
            group (set): An individual group of red subgrids.

        Returns:
            list: The list of nodes a group is required to travel to.
        '''

        coords = {node: self.centroids[node] for node in group}
        unvisited = set(coords.keys())
        path = []
        current = next(iter(unvisited))  # Start with a random node
        path.append(current)
        unvisited.remove(current)

        while unvisited:
            current_coords = coords[current]
            nearest = min(unvisited, key=lambda node: np.linalg.norm(np.array(coords[node]) - np.array(current_coords)))
            path.append(nearest)
            unvisited.remove(nearest)
            current = nearest

        return path

    def plan_paths(self):
        '''
        Calls on the nearest_neighbor_path method to determine a node's nearest neighbor.

        Returns:
            set: The set of all paths contained on the image.
        '''

        if self.groups is None:
            raise ValueError("Groups have not been split. Call split_clusters() first.")

        self.paths = {group_id: self.nearest_neighbor_path(group) for group_id, group in self.groups.items()}
        return self.paths

    def plot_paths(self):
        '''
        Displays each group's path to identify potential hazards.

        Returns:
            plot: A plot of the paths contained in the image through matplotlib.
        '''

    def plot_paths(self, image=None, save_path=None):
        if self.groups is None or self.paths is None:
            raise ValueError("Groups or paths are not available. Ensure both are computed.")

        colors = cm.get_cmap("tab10", self.num_groups)
        coords = self.centroids

        fig, ax = plt.subplots(figsize=(10, 10))

        if image:
            im = plt.imread(image)
            ax.imshow(im, extent=[0, 3923, 2950, 0])

        for group_id, group in self.groups.items():
            group_coords = [coords[node] for node in group]
            path = self.paths[group_id]

            ax.scatter(
                [coords[node][0] for node in group], 
                [coords[node][1] for node in group], 
                color=colors(group_id / self.num_groups),
                edgecolor="black",
                s=100,
                label=f"Group {group_id}"
            )

            path_coords = [coords[node] for node in path]
            path_x, path_y = zip(*path_coords)
            colors_paths = ['#' + ''.join(f"{random.randint(0, 255):02X}" for _ in range(3)) for _ in range(10) if not all(abs(random.randint(0, 255) - random.randint(0, 255)) < 50 for _ in range(3))]

            # Then use it in the plot like this
            ax.plot(path_x, path_y, color=colors_paths[group_id - 1],linewidth=2)

            for node, (x, y) in coords.items():
                ax.text(x, y, str(node), fontsize=9, ha="center", va="center", color="white", 
                        bbox=dict(facecolor="black", edgecolor="none", boxstyle="round,pad=0.3"))

        ax.set_title("Cluster Groups and Paths")
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.xaxis.set_label_position("top")
        ax.xaxis.set_ticks_position("top")
        ax.grid(True)
        ax.set_xlim(0, 3923)
        ax.set_ylim(2950, 0)

        if save_path:
            fig.savefig(save_path, format="png", dpi=300)

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=300)
        buf.seek(0)
        plt.close(fig)
        return Image.open(buf)

    def print_paths(self):
        '''
        Displays the paths to the user via the terminal.
        '''

        if self.paths is None:
            raise ValueError("Paths have not been planned. Call plan_paths() first.")
        
        for group_id, path in self.paths.items():
            print(f"Group {group_id} Path: {path}")

    def animate_paths(self, save_to=None):
        if self.groups is None or self.paths is None:
            raise ValueError("Groups or paths are not available. Ensure both are computed.")
        
        colors = cm.get_cmap("tab10", self.num_groups)  # Color map for groups
        coords = self.centroids
        fig, ax = plt.subplots(figsize=(8, 6))

        # Prepare the plot
        ax.set_title("Drone Path Animation")
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.grid(True)
        
        # Move the x-axis to the top
        ax.xaxis.set_ticks_position('top')
        ax.xaxis.set_label_position('top')  # Set x-axis label at the top

        ax.set_xlim(0, 3923)
        ax.set_ylim(2950, 0)

        # Invert Y-axis to make (0, 0) at the top-left corner
        ax.invert_yaxis()
        
        ax.set_xlim(min(x[0] for x in coords.values()) - 10, max(x[0] for x in coords.values()) + 10)
        ax.set_ylim(min(x[1] for x in coords.values()) - 10, max(x[1] for x in coords.values()) + 10)
        
        # Initialize scatter and line plot objects for animation
        scatter_plots = []
        line_plots = []
        for group_id in range(1, self.num_groups + 1):
            scatter, = ax.plot([], [], 'o', color=colors(group_id / self.num_groups), label=f"Group {group_id}")
            line, = ax.plot([], [], '-', color=colors(group_id / self.num_groups), lw=2)
            scatter_plots.append(scatter)
            line_plots.append(line)

        # Animation function
        def update(frame):
            for group_id, path in self.paths.items():
                group_index = group_id - 1  # Convert group ID to index
                extended_path = [(0, 0)] + [coords[node] for node in path[:frame + 1]]
                scatter_plots[group_index].set_data(
                    [p[0] for p in extended_path],
                    [p[1] for p in extended_path]
                )
                line_plots[group_index].set_data(
                    [p[0] for p in extended_path],
                    [p[1] for p in extended_path]
                )

            return scatter_plots + line_plots

        # Determine the maximum number of frames
        max_frames = max(len(path) for path in self.paths.values())
        
        # Create animation
        ani = animation.FuncAnimation(
            fig, update, frames=max_frames, interval=500, blit=True, repeat=False
        )
        plt.gca().invert_yaxis()
        
        # Save animation if required
        if save_to:
            ani.save(save_to, writer='imagemagick')
        
        # Return the animation object
        return ani
