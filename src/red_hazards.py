from PIL import Image, ImageDraw
import numpy as np

class IdentifyHazards:
    '''
    IdentifyHazards processes a grayscale image and identifies potential areas where a hazard may be on a construction site.

    Authors:
        Hermann Ndeh
        Misk Hussain
        Sharon Gilman
    '''

    def __init__(self, image_path, potential_hazards_path, grid_size, min_threshold=0, max_threshold=65535):
        '''
        Initialize the class with the provided image paths to the raw image and the path to the folder where the processed image will be 
        saved to. Sets the minimum and maximum thresholds for identifying potential hazards.

        Parameters:
            image_path (string): The path to the raw image.
            potential_hazards_path (string): The path to the image with identified potential hazards.
            grid_size (tuple): The size of the grid.
            min_threshold (int): The minimum threshold to identify potential hazards.
            max_threshold (int): The maximum threshold to identify potential hazards.
        '''

        """
        Initialize the class with parameters for hazard identification.

        Parameters:
            image_path (str): Path to the input image.
            potential_hazards_path (str): Path to save the annotated image.
            grid_size (tuple): Number of rows and columns for the grid.
            min_threshold (int): Minimum standard deviation threshold.
            max_threshold (int): Maximum standard deviation threshold.
        """
        self.image_path = image_path
        self.potential_hazards_path = potential_hazards_path
        self.grid_size = grid_size
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold
        self.red_grid_count = 0  # Counter for grids meeting the hazard criteria
        self.red_grids_coords = []  # Stores label and center coordinates of red grids
        self.red_grids = []  # Stores labels of grids meeting hazard criteria

    def highlight_grids(self):
        '''
        Uses the 16-bit grayscale image to determine which grids are within the minimum threshold and maximum threshold.
        '''
        
        """
        Process the image, overlay a grid, and highlight potential hazard areas.
        """
        # Open and convert the image to 16-bit grayscale
        image = Image.open(self.image_path)
        gray_image = image.convert('I;16')
        grayscale_array = np.array(gray_image, dtype=np.float32) * (65535 / 255)

        height, width = grayscale_array.shape
        cell_height = height // self.grid_size[0]
        cell_width = width // self.grid_size[1]

        # Convert to RGB for drawing highlights
        rgb_image = gray_image.convert('RGB')
        draw = ImageDraw.Draw(rgb_image, 'RGBA')

        label = 1  # Grid label counter

        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                top = row * cell_height
                left = col * cell_width
                bottom = (row + 1) * cell_height
                right = (col + 1) * cell_width

                # Extract the current grid cell
                grid_cell = grayscale_array[top:bottom, left:right]
                std_value = np.std(grid_cell)

                if self.min_threshold <= std_value <= self.max_threshold:
                    # Highlight the grid cell with a red overlay
                    draw.rectangle([left, top, right, bottom], fill=(255, 0, 0, 30))
                    self.red_grid_count += 1

                    # Divide the grid into 8 smaller sub-grids (2 rows x 4 columns)
                    small_cell_height = (bottom - top) // 4
                    small_cell_width = (right - left) // 4

                    for i in range(4):
                        for j in range(4):
                            small_top = top + i * small_cell_height
                            small_left = left + j * small_cell_width
                            small_bottom = small_top + small_cell_height
                            small_right = small_left + small_cell_width

                            # Outline the smaller grids
                            draw.rectangle([small_left, small_top, small_right, small_bottom], outline="black")

                    # Calculate center coordinates of the grid
                    center_x = (left + right) // 2
                    center_y = (top + bottom) // 2

                    # Store hazard grid information
                    self.red_grids_coords.append({"label": label, "center": (center_x, center_y)})
                    self.red_grids.append(label)

                # Label the grid in the top-left corner
                draw.text((left + 5, top + 5), str(label), fill="white")
                label += 1

        # Save the annotated image
        rgb_image.save(self.potential_hazards_path)

    def count_red_grids(self):
        '''
        Returns the number of red grids contained in a processed image.

        Returns:
            int: The number of red grids contained in the processed image.
        '''

        return self.red_grid_count  # Return the count of red grids

    def grid_info(self):
        '''
        Returns a list of coordinates of the red grids contained in the processed image.

        Returns:
            list: The list of each red grid's coordinates.
        '''
        
        return self.red_grids_cords
    
    def red_grids_lists(self):
        '''
        Returns a list of all the red grids contained in the processed image.

        Returns:
            list: The list of red grids displayed on an image.
        '''

        return self.red_grids
    
        """
        Get the count of grids meeting the hazard criteria.

        Returns:
            int: Number of grids highlighted as hazards.
        """
        return self.red_grid_count

    def grid_info(self):
        """
        Get detailed information about grids meeting hazard criteria.

        Returns:
            list[dict]: List of dictionaries containing grid labels and center coordinates.
        """
        return self.red_grids_coords

    def red_grids_list(self):
        """
        Get a list of labels for grids meeting hazard criteria.

        Returns:
            list[int]: List of grid labels.
        """
        return self.red_grids
