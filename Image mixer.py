import os
import re
import fnmatch
from PIL import Image
from itertools import product

# == Variables ==
# Change this to select another directory 
starting_directory = os.getcwd()
# Change this to change the name pattern
pattern = re.compile(r"^layer (\d+)$")
# Directory for the generated images
results_directory = os.path.join(starting_directory, 'results')
# Create the results directory if it doesn't exist
if not os.path.exists(results_directory):
    os.makedirs(results_directory)

# == Functions ==
def search_folders(path, name_format):
    folders = []
    # Search for each folder inside the main folder
    for name in os.listdir(path):
        route = os.path.join(path, name)
        # Check if the file is a folder with the correct name format
        if os.path.isdir(route) and name_format.match(name):
            folders.append(route)
    # Organize the folders found if they aren't in the correct order
    folders.sort(key=lambda x: int(name_format.match(os.path.basename(x)).group(1)))
    return folders
# ---------------------------------------------------------------------
def search_image(paths):
    images = []
    formats = ['*.png']
    # Search in the folder any image 
    for root, dirs, files in os.walk(paths):
        for ext in formats:
            for filename in fnmatch.filter(files, ext):
                images.append(os.path.join(root, filename))
    return images
# ---------------------------------------------------------------------
def combine_images(images):
    images_list = [Image.open(i) for i in images]
    width, high = images_list[0].size
    new_image = Image.new('RGBA', (width, high))
    # Combine each image into a new one
    for im in images_list:
        new_image = Image.alpha_composite(new_image, im.convert('RGBA'))
    # Combine the names of the images
    name_images = [os.path.splitext(os.path.basename(i))[0] for i in images]
    names_combined = "-".join(name_images) + '.png'
    # Save a new image in the folder of the script
    new_image.save(os.path.join(results_directory, names_combined))
    
# == Main code ==
images = []
layers = search_folders(starting_directory, pattern)
for layer in layers:
    images.append(search_image(layer))

# List that exclude all the empty folders
filtered_list = [lst for lst in images if lst]

list_combinations = list(product(*filtered_list))

# Create all the image combinations
for combination in list_combinations:
    combine_images(combination)
print("Done")
