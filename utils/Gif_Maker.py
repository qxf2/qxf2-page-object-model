"""
Utility to make a GIF of all the screenshots captured during test run

"""
import imageio
import os

images = []

def make_gif(screenshot_dir):
    "Creates gif of the screenshots"
    filenames = os.listdir(screenshot_dir)
    suffix = '.gif'
    gif_name = os.path.join(screenshot_dir, "test_gif" + suffix)
    
    for files in filenames: 
        images.append(imageio.imread(os.path.join(screenshot_dir, files)))
    imageio.mimsave(gif_name, images,format='.gif',duration=2)
    return gif_name        
