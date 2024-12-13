from grid_and_grayscale import DefineGrayScale
from red_hazards import IdentifyHazards
import os
import tkinter as tk
from tkinter import filedialog

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

class ImageProcessor:
    '''
    ImageProcessor processes images from an image folder by converting them into a grayscale image and identifying potential hazards. 

    Authors:
        Hermann Ndeh
        Misk Hussain
        Sharon Gilman
    '''

    def __init__(self, image_folder='drone-images', grayscale_folder='grayscale_drone_images', potential_hazards_folder='potential_hazards'):
        '''
        Initialize the class with the providied image folder, grayscale folder, and potential hazards folder.

        Parameters:
            image_folder (string): The path to the drone images.
            grayscale_folder (string): The path to save the processed grayscale images to.
            potential_hazards_folder (string): The path to save the processed images to. Images in this folder have highlighted red grids 
                where potential hazards may reside.
        '''

        self.image_folder = image_folder
        self.grayscale_folder = grayscale_folder
        self.potential_hazards_folder = potential_hazards_folder
        ensure_directory_exists(self.grayscale_folder)
        ensure_directory_exists(self.potential_hazards_folder)

    def select_image(self):
        '''
        Prompts the user to select an image file.

        Returns:
            string: The file path to the selected image.
        '''

        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        file_path = filedialog.askopenfilename(
            initialdir=self.image_folder,
            title="Select an Image File",
            filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*"))
        )
        return file_path if file_path else None

    def process_image_files(self):
        '''
        Processes each file in the drone folder.
        '''

        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith('.jpg'):
                self.process_image(filename)

    def process_image(self, filename):
        '''
        Processes the provided image. First converts the image to grayscale and then identifies potential hazards.

        Parameters:
            filename (string): The name of the image to process.
        '''

        image_path = os.path.join(self.image_folder, filename)
        grayscale_path = os.path.join(self.grayscale_folder, filename)
        potential_hazards_path = os.path.join(self.potential_hazards_folder, filename)

        # Process grayscale
        grayscale = DefineGrayScale(image_path, grayscale_path, grid_size=(20, 20))
        grayscale.process_image()

        # Identify hazards
        potential_hazards = IdentifyHazards(
            grayscale_path, potential_hazards_path, 
            grid_size=(20, 20), min_threshold=10000, max_threshold=20000
        )
        potential_hazards.highlight_grids()

def main():
    processor = ImageProcessor()
    
    # Prompt user to select an image file
    selected_image = processor.select_image()
    if selected_image:
        # If an image was selected, process it individually
        filename = os.path.basename(selected_image)
        processor.process_image(filename)
    else:
        # Otherwise, process all images in the directory
        processor.process_image_files()

if __name__ == "__main__":
    main()
