"""
Qxf2 Services: This utility is for creating a GIF of all the screenshots captured during current test run

"""
import imageio
import os

images = []

def make_gif(screenshot_dir_path,name = "test_recap",suffix=".gif"):
    "Creates gif of the screenshots"
    filenames = os.listdir(screenshot_dir_path)
    gif_name = os.path.join(screenshot_dir_path, name + suffix)
    
    for files in filenames: 
        images.append(imageio.imread(os.path.join(screenshot_dir_path, files)))
    imageio.mimwrite(gif_name, images,duration=5)
    return gif_name        
