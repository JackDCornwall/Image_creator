'''
#Created by: Jack Cornwall
#Email: hello@jackcornwall.co.uk
#Git hub: https://github.com/JackDCornwall
#Website:https://jackcornwall.co.uk/

#Project: Image renamer
#Date: 10.07.21
#Description: renames files to avoid duplicate names
'''
#importing required files
import os
import pandas as pd
import re
import shutil

###########################SETTINGS###########################
folder = "C://Users/conta/Documents/python/Training data/74K Charset/English/Img/GoodImg/Bmp/Sample002/" # folder of images to rename
##############################################################

#### creating/deleting directories

# checking if converted folder exists
if os.path.exists(folder+"/Renamed/"):

    # if it exists we delete it
    os.rmdir(folder+"/Renamed/")

# creating os directory
os.mkdir(folder+"/Renamed/")

#### manipulating data

# extracting all images to list
files = os.listdir(folder)

# converting to pandas array
files = pd.DataFrame(files, columns=["file"])

#subsetting to only images with required file extension
files = files.loc[files["file"].str.contains("\.png$|\.jpg$|\.jpeg$|\.bmp$", regex=True)]
files = files.reset_index(drop=True) #resetting index in case any images have been removed

# compiling regex for extension and filename
re_ext = re.compile("\.png$|\.jpg$|\.jpeg$|\.bmp$")
re_name = re.compile("^.*\.")



# generating appendix number
dix = 0

#### looping through all files
for file in files["file"]:

    name = re_ext.sub("", file) # extracting name

    typ = re_name.sub(".", file) # extracting filetype

    origin = folder + file # generating source file name

    export = folder + "Renamed/" + name + "_" + str(dix) + "_good" + typ # generating export name

    dix = dix + 1  # adding one to extension number

    shutil.copy(origin , export)

    print(origin)
    print(export)







# code success message
print("The code has run successfully")