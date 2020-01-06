"""
Qxf2 Services: This utility is for creating a GIF of all the screenshots captured during current test run

"""
import imageio
import os


def make_gif(screenshot_dir_path,name = "test_recap",suffix=".gif",duration=2):
    "Creates gif of the screenshots"
    images = []
    filenames = os.listdir(screenshot_dir_path)
    gif_name = os.path.join(screenshot_dir_path, name + suffix)
    
    for files in sorted(filenames): 
        images.append(imageio.imread(os.path.join(screenshot_dir_path, files)))
    imageio.mimwrite(gif_name, images,duration=duration)
    return gif_name        
