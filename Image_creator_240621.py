'''
#Created by: Jack Cornwall
#Email: jackcornwall91@gmail.com
#Git hub: https://github.com/JackDCornwall
#Website:https://jackcornwall.co.uk/

#Project: Image generator
#Date: 24.06.21
#Description: automatically creates a large library of varied images that can be used for ML
'''

#importing required packages
import cv2
import os
import random
import numpy as np
import pandas as pd
from PIL import ImageFont,ImageDraw,Image,ImageOps
from fontTools.ttLib import TTFont
from datetime import datetime

###########----SETTINGS----###########
preview_mode = True #if preview is true, files aren't saved but displayed. If false, files are saved.
preview_time = 250 #time in ms to display preview image
blanks = False #should blanks be generated? (Empty sudoku cells)
chars = "012" #All characters to include (Blanks are denoted above)
'''abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789'''
iterations = 2000
#number of images to create per character
max_angle = 25 #maximum angle rotation for any letters
max_smudge = 5 #maximum number of random smudges
smudge_chance = 20 #likelyhood of smudge appearing
smudge_spread = 30 #likelyhood of smudge spreading
sprinkle_chance = 4 #percentage chance of a sprinkle appearing
inversion_chance = 3 #percentage chance of an inversion occurring
######################################

#extracting characters from string
chars = list(chars)

#setting paths
wd_path = os.getcwd() #current working directory
fonts_path = "C://Windows/Fonts/"
background_path = "Backgrounds"
overlay_path = "Overlays"


#generating list of all fonts on pc
fonts = os.listdir(fonts_path)
#converting fonts list to np array to subset
fonts = pd.DataFrame(fonts)

#########################Font clean up########################
#removing all .fon fonts as these break PIL
fonts = fonts.loc[fonts[0].str.contains("^.*\.fon$|^.*\.FON$")==False]

#removing all .ttc fonts as these break the glyph check function
fonts = fonts.loc[fonts[0].str.contains("^.*\.ttc$|^.*\.TTC$")==False]

#removing all .CompositeFont fonts as these break the glyph check function
fonts = fonts.loc[fonts[0].str.contains("^.*\.CompositeFont$")==False]

#removing all .xml fonts as these break the glyph check function
fonts = fonts.loc[fonts[0].str.contains("^.*\.xml$|^.*\.XML$")==False]

#removing all .ini fonts as these break the glyph check function
fonts = fonts.loc[fonts[0].str.contains("^.*\.ini$")==False]

#removing all .dat fonts as these break the glyph check function
fonts = fonts.loc[fonts[0].str.contains("^.*\.dat$")==False]

#removing the deleted subfolder
fonts = fonts.loc[fonts[0].str.contains("^Deleted$")==False]

#resetting the index as all .fon fonts have been removed
fonts = fonts.reset_index(drop=True)
###############################################################


#################################################----IMPORT FUNCTIONS----#################################################
# defining a function that returns a square with randomized features as needed
# in future versions of the code this will create a more complex square for use
#v1 was used for debugging
def getSquare_v1():

    #imports the required colour square, mostly for debugging purposes
    #img = cv2.imread("Black_square_sample_32x32.jpg") #Black
    #img = cv2.imread("White_square_sample_32x32.jpg") #White
    img = cv2.imread("Pink_square_sample_32x32.jpg") #Pink
    #img = cv2.imread("Green_square_sample_32x32.jpg") #Green
    return img

# #generates a black square for mask creation
# def getSquare_v2():
#     img = np.zeros((32,32,3),dtype="uint8") # since this will be used for a mask it is fine to be pure black
#     return img

#extracting random square for background and foreground
def getSquare_v3(path):

    images_list = os.listdir(str(path)) #finding all potential images
    images_count = len(images_list) #total number of potential images
    random_n = np.random.randint(0, images_count) #random number to select image
    random_image_name = images_list[random_n] #selecting random image
    image_path = str(path +"/" + random_image_name) #path to randomly selected image
    random_image = cv2.imread(image_path) #importing image

    #extracting height and width of image
    width = random_image.shape[1]
    height = random_image.shape[0]

    #extracting random coordinates to begin cut out
    x_coord = np.random.randint(0,width-33)
    y_coord = np.random.randint(0,height-33)

    #cropping array
    crop_image = random_image[y_coord:y_coord+32,x_coord:x_coord+32]

    return crop_image

# #testing font functions
# def getFont_v1():
#     font = fonts[0][0]  # setting font
#
#     return font

#selecting a random font
def getFont_v2(font_list):

    #selecting a random font from inputted list
    font_num = random.randrange(0,len(font_list))

    #returning a random font
    return font_list[0][font_num]

#creating function to check for the existence of a glyph in a font library
def glyphCheck(font,char):

    #path to font for glyph search
    font_path = str(fonts_path + font)

    #extracting font to check for char glyph
    gFont = TTFont(font_path)

    #running through tables in fonts cmap
    for table in gFont["cmap"].tables:

        #font Cmaps can flag AssertionErrors, these are caught here
        try:
            #checking if character has a font
            if ord(char) in table.cmap.keys():
                return True #returns true if a glyph is found

        #printing error message
        except AssertionError:
            print("Skipping font:",font_path,"due to Assertion Error in Glyph Check")

    return False #returns false if a glyph cannot be found

#selecting font size to use based on random size requirements
def getFontSize(font,char):

    # path to font for glyph search
    font_path = str(fonts_path + font)

    #randomly selecting target size between 10 and 30 (this will be the target size of the maximum dimension)
    target = np.random.randint(10,31)

    #a for loop that will attempt 20 times to generate a font of the desired size (if not return the largest)
    for attempt in range(20):

        #preparing font to test size
        try_font = ImageFont.truetype(font_path,9+attempt)

        #attempts to extract font size, however sometimes this raises OSErrors
        try:

            #extracting font dimensions
            font_dim = try_font.getsize(char)

        #If OSError is raised catch it and use a simple font that works
        except OSError:

            font_path = r"C://Windows/Fonts/times.ttf"
            try_font = ImageFont.truetype(font_path, 10)
            font_dim = try_font.getsize(char)
        #extracting maximum dimension
        max_dim = max(font_dim)

        #checking if the dimension has been reached
        if max_dim > target:

            return 8+attempt,font_dim #returning last number that didn't exceed dimensions

    return 8+attempt,font_dim #if no tested size is larger than the target, return the largest to use

#getting starting location based on letter size and a bit of random flair
def getLoc(dim):

    if max(dim)>30:
        return (0,0) #if a ridiculously large font is detected shove it in as best as possible

    ####Starting X coordinate ####
    #extracting width from dimensions
    width = dim[1]

    #calculating maximum x offset
    x_offset_max = ((32 - width)//2)

    #calculating x_offset randomly
    x_offset = np.random.randint((-1*x_offset_max),x_offset_max,1)

    #calculating starting x coord
    x_loc = ((32 - width)//2) + x_offset[0]

    ####Starting Y coordinate ####
    #extracting width from dimensions
    height = dim[0]

    #calculating maximum x offset
    y_offset_max = ((32 - height)//2)

    #calculating x_offset randomly
    y_offset = np.random.randint((-1*y_offset_max),y_offset_max,1)

    #calculating starting x coord
    y_loc = ((32 - height)//2) + y_offset[0]

    return (y_loc,x_loc)

# #creating a mask from fed in image
# def applyMask(src,mask):
#
#     maskApplied = cv2.bitwise_and(src,src,mask=mask)
#
#     return maskApplied

#random angle between -20 and 20 degrees for rotation with increased probability of small angle
def randAngle(max):

    #first random value (making smaller angles more likely)
    random = np.random.randint(0, 100)

    #zero tilt added
    if random<30:
        angle = 0

    #-max/8 to max/8 range
    elif random<55:
        angle = np.random.randint(-max//8, (max//8)+1)

    #-max/4 to max/4 range
    elif random<75:
        angle = np.random.randint(-max//4, (max//4)+1)

    #-max/2 to max/2 range
    elif random<90:
        angle = np.random.randint(-max//2, (max//2)+1)

    #-max to max range
    else:
        angle = np.random.randint(-max, max+1)

    return angle

# apply text using PIL
def maskText(font_path, font_size, text, angle):
    font = ImageFont.truetype(font_path, font_size)  # preparing to "draw" letter on with selected font PIL

    # creating mask background (black square) as a PIL image
    transparent = Image.new("L", (32, 32), "black")
    # "L" mode is a single channel image (greyscale) without specifying this defaults to black (0,0,0)
    # This is a black square that will have a white image overlain. It will then be rotated and the black will
    # will be subtracted leaving only the white letter

    draw = ImageDraw.Draw(transparent)  # preparing PIL draw action

    draw.text(start_loc, text, font=font, fill=255)  # PIL Drawing letter

    rotated_image = transparent.rotate(angle, expand=1)  # PIL white letter on black background rotated

    # black background over which to place rotated white letter
    mask_background = Image.new("RGB", (32, 32), "black")

    mask_background.paste(ImageOps.colorize(rotated_image, (0, 0, 0), (255, 255, 255)), (0, 0),
                          rotated_image)  # place white letter over black background

    # creating mask (starting from RGB pil image[32,32,3], 0 to 255 values and ending in Grayscale CV2 image [32,32] 0 or 1 binary valuues)
    mask = np.array(mask_background)  # converting PIL image to openCV image
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)  # converting image to
    mask[mask > 1] = 1  # ensuring all values are 1 or 0 (becomes hard to see using imshow)

    return mask

# overlaying an image over another using
def overlayImg(background, overlay, mask):
    image_out = np.copy(background)  # creating output image (with background to overlay letter)

    # overlaying each BGR channel foreground onto background as dictated by mask
    image_out[:, :, 0] = np.where(mask == 1, overlay[:, :, 0], background[:, :, 0])
    image_out[:, :, 1] = np.where(mask == 1, overlay[:, :, 1], background[:, :, 1])
    image_out[:, :, 2] = np.where(mask == 1, overlay[:, :, 2], background[:, :, 2])

    return image_out

#generating a random smudge
def randomSmudges(smudge_chance, spread_chance):
    random = np.random.randint(0, 100)

    # checking against random chance
    if random < smudge_chance:

        smudge_mask = np.zeros((32, 32), dtype="uint8")  # creating mask

        # random origin of smudge
        origin = [np.random.randint(0, 32), np.random.randint(0, 32)]
        # print(origin)

        smudge_mask[origin[0], origin[1]] = 1

        # spreadking from origin
        while random < spread_chance:

            # randomly selecting a direction
            direction = np.random.randint(0, 4)

            # spreading smudge
            # moving up
            if direction == 0:

                # checking we can move up
                if origin[0] < 31:
                    #moving up unless we are at the top
                    origin[0] = origin[0] + 1

            # moving down
            elif direction == 1:

                # checking we can move down
                if origin[0] > 0:
                    # moving down unless we are at the bottom
                    origin[0] = origin[0] - 1

            # moving right
            elif direction == 2:

                # checking we can move right
                if origin[1] < 31:
                    # moving right unless we are at the side
                    origin[1] = origin[1] + 1

            # moving left
            elif direction == 3:

                # checking we can move left
                if origin[1] > 0:
                    # moving left unless we are at the side
                    origin[1] = origin[1] - 1

            smudge_mask[origin[0], origin[1]] = 1  # updating mask
            random = np.random.randint(0, 100)  # retesting probability

        #returning true & smudge mask so that it can be applied
        return True, smudge_mask

    else:
        # returning false so that random smudge isn't implemented
        return False, ""

#generating random colour for sprinkle
def randomSprinkle():
    R = np.random.randint(0, 256)
    G = np.random.randint(0, 256)
    B = np.random.randint(0, 256)

    # returning 3 coolors
    return R, G, B

#sprinkles is the coloured version of salt and peppering images
def sprinkles(img, sprinkle_chance):
    # looping through rows
    for row in range(32):

        # looping through columns
        for col in range(32):

            # checking if a sprinkle should occur
            if np.random.randint(0, 100) < sprinkle_chance:
                # generating sprinkle colours
                R, G, B = randomSprinkle()

                # adding sprinkle
                img[row, col, 0] = B
                img[row, col, 1] = G
                img[row, col, 2] = R

    return img  # returning sprinkled image

#function that inverts the colours of a cv2 image
def randomInvert(img, inversion_chance):
    # checking if inversion should occur
    if np.random.randint(0, 100) < inversion_chance:
        # performing inversion
        img = (255 - img)

    return img


# saving file as random filetype with random quality
def saveFile(img, name):
    # getting date and time to append
    now = datetime.now()  # extracting time string
    now = now.strftime("%d_%m_%Y_%H_%M_%S")  # converting string to be filename compatible

    file_name = name + "_" + str(now)

    # randomly choosing filetype
    file_type = np.random.randint(0, 3)

    # saving file as chosen filetype
    # saving as jpg
    if (file_type == 0):

        # randomly selecting quality
        quality = np.random.randint(40, 101)

        # saving
        cv2.imwrite(("Created images/" + char + "/" + file_name + "_" + str(quality) + ".jpg"), img,
                    [cv2.IMWRITE_JPEG_QUALITY, quality])

    # saving as jpeg
    elif (file_type == 1):

        # randomly selecting quality
        quality = np.random.randint(40, 101)

        # saving
        cv2.imwrite(("Created images/" + char + "/" + file_name + "_" + str(quality) + ".jpeg"), img,
                    [cv2.IMWRITE_JPEG_QUALITY, quality])

    # saving as png
    elif (file_type == 2):

        # randomly selecting compression
        compression = np.random.randint(0, 10)

        # saving
        cv2.imwrite(("Created images/" + char + "/" + file_name + "_" + str(compression) + ".png"), img,
                    [cv2.IMWRITE_PNG_COMPRESSION, compression])
########################################################################################################################


#appending blank if requested by user in settings
if blanks == True:

    #adding blank as a chars
    chars.append("Blank")

#looping through the user requested number of iterations
for i in range(iterations):

    #printing progress
    print("Current iteration:",i,"of",iterations,"total")

    #loping through each letter
    for char in chars:

        #adding letter unless a blank is required
        if char != "Blank":

            font = getFont_v2(fonts)  # randomly selecting a font from the list

            #checking required glyph exists
            glyph = glyphCheck(font,char)

            #if required glyph exists
            if glyph == 1:

                # extracting font size and dimensions used to calculate font origin
                font_size, dimensions = getFontSize(font, char)

                # getting starting location to input into draw function
                start_loc = getLoc(dimensions)

                #extracting random rotation angle
                angle = randAngle(max_angle)

                #requesting mask
                mask = maskText(font,font_size,char,angle)

                #loading required images
                background = getSquare_v3(background_path) #background
                overlay = getSquare_v3(overlay_path) #overlay

                #overlaying
                image_out = overlayImg(background,overlay,mask)

                #adding up to max_smudge smudges
                for k in range(max_smudge):

                    # generating smudge
                    apply, smudge_mask = randomSmudges(smudge_chance,smudge_spread)

                    # applying smudge if needed
                    if apply == True:

                        # randomly selecting smudge folder
                        random_smu = np.random.randint(0, 2)

                        # selecting between folders
                        if random_smu == 0:

                            # overlay smudge will be dark
                            overlay = getSquare_v3(overlay_path)  # overlay

                        else:

                            # overlay smudge will be light
                            overlay = getSquare_v3(background_path)  # overlay

                        # ovelaying smudge
                        image_out = overlayImg(image_out, overlay, smudge_mask)

                image_out = sprinkles(image_out,sprinkle_chance) #adding rainbow sprinkles

                #randomly inverting image colours
                image_out = randomInvert(image_out,inversion_chance)

                #checking for preview mode
                if preview_mode == False:

                    # name of export file
                    name = char + "_" + str(i) + "_" + str(max_smudge) + "_" + str(smudge_chance) + "_" + str(smudge_spread) + "_" + str(inversion_chance)

                    #saving file
                    saveFile(image_out, name)

                else:

                    #displaying for test purposes
                    image_out = cv2.resize(image_out, (160, 160))
                    cv2.imshow("Output", image_out)
                    cv2.waitKey(preview_time)

            else:

                #ignoring when glyph is returned
                print("Glyph doesnt exists  for font :",font)

        #skipping if blank is required
        else:

            # loading required images
            image_out = getSquare_v3(background_path)  # background

            # adding up to max_smudge smudges
            for k in range(max_smudge):

                # generating smudge
                apply, smudge_mask = randomSmudges(smudge_chance, smudge_spread)

                # applying smudge if needed
                if apply == True:

                    # randomly selecting smudge folder
                    random_smu = np.random.randint(0, 2)

                    # selecting between folders
                    if random_smu == 0:

                        # overlay smudge will be dark
                        overlay = getSquare_v3(overlay_path)  # overlay

                    else:

                        # overlay smudge will be light
                        overlay = getSquare_v3(background_path)  # overlay

                    # ovelaying smudge
                    image_out = overlayImg(image_out, overlay, smudge_mask)

            image_out = sprinkles(image_out, sprinkle_chance)  # adding rainbow sprinkles

            # randomly inverting image colours
            image_out = randomInvert(image_out, inversion_chance)

            # checking for preview mode
            if preview_mode == False:

                # name of export file
                name = char + "_" + str(i) + "_" + str(max_smudge) + "_" + str(smudge_chance) + "_" + str(
                    smudge_spread) + "_" + str(inversion_chance)

                # saving file
                saveFile(image_out, name)

            else:

                # displaying for test purposes
                image_out = cv2.resize(image_out, (160, 160))
                cv2.imshow("Output", image_out)
                cv2.waitKey(preview_time)

#code success message
print("The code has run successfully")