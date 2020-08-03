"""
Qxf2 Services: Utility script to compare images
* Compare two images(actual and expected) smartly and generate a resultant image
* Get the sum of colors in an image
"""
from PIL import Image, ImageChops
import math, os

def rmsdiff(im1,im2):
    "Calculate the root-mean-square difference between two images"

    h = ImageChops.difference(im1, im2).histogram()
    # calculate rms
    return math.sqrt(sum(h*(i**2) for i, h in enumerate(h)) / (float(im1.size[0]) * im1.size[1]))


def is_equal(img_actual,img_expected,result):
    "Returns true if the images are identical(all pixels in the difference image are zero)"
    result_flag = False

    if not os.path.exists(img_actual):
        print('Could not locate the generated image: %s'%img_actual)

    if not os.path.exists(img_expected):
        print('Could not locate the baseline image: %s'%img_expected)

    if os.path.exists(img_actual) and os.path.exists(img_expected):
        actual = Image.open(img_actual)
        expected = Image.open(img_expected)
        result_image = ImageChops.difference(actual,expected)
        color_matrix = ([0] + ([255] * 255))
        result_image = result_image.convert('L')
        result_image = result_image.point(color_matrix)
        result_image.save(result)#Save the result image

        if (ImageChops.difference(actual,expected).getbbox() is None):
            result_flag = True
        else:
            #Let's do some interesting processing now
            result_flag = analyze_difference_smartly(result)
            if result_flag is False:
                print("Since there is a difference in pixel value of both images, we are checking the threshold value to pass the images with minor difference")
                #Now with threshhold!
                result_flag = True if rmsdiff(actual,expected) < 958 else False
            #For temporary debug purposes
            print('RMS diff score: ',rmsdiff(actual,expected))

    return result_flag


def analyze_difference_smartly(img):
    "Make an evaluation of a difference image"
    result_flag = False
    if not os.path.exists(img):
        print('Could not locate the image to analyze the difference smartly: %s'%img)
    else:
        my_image = Image.open(img)
        #Not an ideal line, but we dont have any enormous images
        pixels = list(my_image.getdata())
        pixels = [1 for x in pixels if x!=0]
        num_different_pixels = sum(pixels)
        print('Number of different pixels in the result image: %d'%num_different_pixels)
        #Rule 1: If the number of different pixels is <10, then pass the image
        #This is relatively safe since all changes to objects will be more than 10 different pixels
        if num_different_pixels < 10:
            result_flag = True

    return result_flag


def get_color_sum(img):
    "Get the sum of colors in an image"
    sum_color_pixels = -1
    if not os.path.exists(img):
        print('Could not locate the image to sum the colors: %s'%actual)
    else:
        my_image = Image.open(img)
        color_matrix = ([0] + ([255] * 255))
        my_image = my_image.convert('L')
        my_image = my_image.point(color_matrix)
        #Not an ideal line, but we don't have any enormous images
        pixels = list(my_image.getdata())
        sum_color_pixels = sum(pixels)
        print('Sum of colors in the image %s is %d'%(img,sum_color_pixels))

    return sum_color_pixels


#--START OF SCRIPT
if __name__=='__main__':
    # Please update below img1, img2, result_img values before running this script
    img1 = r'Add path of first image'
    img2 = r'Add path of second image'
    result_img= r'Add path of result image' #please add path along with resultant image name which you want

    # Compare images and generate a resultant difference image
    result_flag = is_equal(img1,img2,result_img)
    if (result_flag == True):
        print("Both images are matching")
    else:
        print("Images are not matching")

    # Get the sum of colors in an image
    get_color_sum(img1)
