'''
#Created by: Jack Cornwall
#Email: jackcornwall91@gmail.com
#Git hub: https://github.com/JackDCornwall
#Website:https://jackcornwall.co.uk/

#Project: Font extractor
#Date: 07.06.21
#Description: Google fonts can be downloaded all simultaneously from githib, however they are all in directories and
#sub-directories (source: https://github.com/google/fonts) this script unpacks them all into a single directory for
#easy installation.
#In the event files without an extension are found (eg. AUTHORS/CONTRIBUTORS/README) these need to be deleted before proceeding
'''
#importing required functions
import os
import pandas as pd
import re
import shutil

#Starting folder
wd = os.getcwd() #current working directory
crawl_dir = "Google_fonts_all" #crawl start folder

#creating regex checks
re_dir = re.compile("^[^.]+$") #directory names should not contain dots
re_font = re.compile("^[A-z0-9-_]+\.(otf|ttf|ttl|svg|eot|woff(2)?)$")

#buffer list (current list of files to crawl)
#adding start position
buffer = pd.DataFrame({
    "path": [crawl_dir],
    "clas":["dir"],
    "crawled":[False]
})

#uncrawled count
uc = 1 #initially set to one so that while loop begins
#(also there is only one un-crawled path initially, the crawl_dir)


#crawling as long as there are files to crawl
#uc is the number of files to crawl
while uc != 0:


    #subsetting paths to be crawled this iteration
    to_crawl = buffer[buffer.crawled == False]  # subsetting by hasn't been crawled
    #to_crawl = buffer[buffer.clas == "dir"]  # subsetting by is a directory (redundant as only dir is set to False)

    #generating un-crawled directory list from buffer
    for dir in to_crawl["path"]:

        #performing crawl
        dir_list = os.listdir(dir)

        #setting parent path
        pth_parent = dir

        #adding newfly found files and directories to buffer
        for pth in dir_list:

            # checking for directory
            if bool(re.search(re_dir, pth)):

                # adding directories to buffer in un-crawled state
                buffer = buffer.append(pd.DataFrame({
                    "path": [pth_parent + "/" + pth],
                    "clas": ["dir"],
                    "crawled": [False]
                }), ignore_index=True)

            # checking for font
            elif bool(re.search(re_font, pth)):

                # added fonts to buffer
                # these arent a directory and dont need crawling (hence True)
                buffer = buffer.append(pd.DataFrame({
                    "path": [pth_parent + "/" + pth],
                    "clas": ["font"],
                    "crawled": [True]
                }), ignore_index=True)

            # checking for anything else
            else:

                # adding any non dir/ non font to the buffer in crawled state (true)
                # this is done as we don't want to do anything with these.
                buffer = buffer.append(pd.DataFrame({
                    "path": [pth_parent + "/" + pth],
                    "clas": ["NA"],
                    "crawled": [True]
                }), ignore_index=True)

        #changing dir to crawled state
        #extracting index that needs updating
        update_index = (buffer[buffer["path"] == dir].index.values)
        buffer.at[update_index,"crawled"] = True #updating index so it wont re-run

    # updating un-crawled list each iteration as we are constantly adding to it (until there are no more)
    #this is done at the end of the while loop so new dirs are factored in to whether crawl continues
    uc = buffer.query("crawled == False").count()["crawled"]

#generating list of fonts to move
font_list = buffer[buffer.clas == "font"]
font_list = list(font_list["path"])

re_fnt_name = re.compile("^(([^\/|\.])*\/)*") #regex to remove suffix from font path to generate font name

#iterating through fonts and moving them to Font_deposit folder
for font_path in font_list:


    #extracting font name
    font_name = re.sub(re_fnt_name,"",font_path)

    #origin and target for file moves
    origin = os.path.join(wd,font_path) #generating origin

    target = os.path.join(wd,"Fonts_deposit",font_name)#genenrating target
    #target = re.sub(re_fwd, "/", target)

    #performing font file move
    shutil.copyfile(origin,target)

print("The code has made it to the end")