from PIL import Image, ImageDraw

class DefineGrayScale:
    '''
    DefineGrayscale opens a given image and converts into an 16-bit grayscale image that can be used across the program. The process_image 
    method converts the image into an 8-bit grayscale image with grids drawn directly on the image to make identifying potential hazards 
    easier. Converted images are saved in the 'grayscale_drone_images' folder as .JPG files.

    Authors:
        Hermann Ndeh
        Misk Hussain
        Sharon Gilman
    '''

    def __init__(self, image_path, grayscale_path, grid_size=(20, 20)):
        '''
        Intialize the class with the specified image path, grayscale path, and grid size.

        Parameters:
            image_path (string): The path to the raw image.
            grayscale_path (string): The path to the grayscale image.
            grid_size (tuple): (width, height) of the entire grid area.
        '''
        
    
    def __init__(self, image_path, grayscale_path, grid_size=(20, 20)):
        """
        Initialize the class with image path, output path, and grid size.

        Parameters:
            image_path (str): Path to the input image.
            grayscale_path (str): Path to save the processed grayscale image.
            grid_size (tuple): Number of grid cells (rows, columns).
        """
        self.image_path = image_path
        self.grayscale_path = grayscale_path
        self.grid_size = grid_size

    def process_image(self):
        '''
        Processes an image first into an 8-bit grayscale image, displays the grid directly on the image, and saves the final image into a 
        16-bit grayscale to the specified file path.
        '''
        
        # Open the image directly as an 8-bit grayscale (L) image for easier manipulation
        """
        Process the image by converting it to grayscale, overlaying a grid,
        and saving it as a 16-bit grayscale image.
        """
        # Open the image and convert to 8-bit grayscale ('L')
        image = Image.open(self.image_path).convert('L')
        width, height = image.size

        # Calculate cell dimensions
        cell_width = width // self.grid_size[1]
        cell_height = height // self.grid_size[0]

        # Draw grid lines on the image
        draw = ImageDraw.Draw(image)

        # Draw horizontal grid lines
        for i in range(1, self.grid_size[0]):
            y = i * cell_height
            draw.line([(0, y), (width, y)], fill=0)

        # Draw vertical grid lines
        for i in range(1, self.grid_size[1]):
            x = i * cell_width
            draw.line([(x, 0), (x, height)], fill=0)

        # Convert to 16-bit grayscale ('I;16') and save the output
        final_image = image.convert('I;16')
        final_image.save(self.grayscale_path)
