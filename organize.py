import os
import shutil
import datetime

import tifffile as tf
import numpy as np
import pandas as pd

from tkinter import Tk, filedialog



def make_skeleton(chosen_folder, image_locations):
    """ Parses a list of excel rows, and constructs a multi-folder directory based on the mesoscale image storing structure"""

    if len(image_locations) != len(os.listdir(chosen_folder)):
        raise Exception("Selected folder and Excel sheet do not match.")

    save_folder = os.path.join(os.path.dirname(chosen_folder), "Organized")
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    for list_path in image_locations:

        animal_id = list_path[0]
        animal_folder = os.path.join(save_folder, str(animal_id))
        if not os.path.exists(animal_folder):
            os.mkdir(animal_folder)

        if int(list_path[1]) < 10:
            list_path[1] = "0" + str(list_path[1])

        slide = list_path[1]
        slide_folder = os.path.join(animal_folder, str(slide))
        if not os.path.exists(slide_folder):
            os.mkdir(slide_folder)

        if int(list_path[2]) < 10:
            list_path[2] = "0" + str(list_path[2])

        section = list_path[2]
        hemisphere = list_path[3]
        section_folder = os.path.join(slide_folder, str(section) + "_" + str(hemisphere))
        if not os.path.exists(section_folder):
            os.mkdir(section_folder)

    return save_folder


def populate(chosen_folder, image_locations, save_folder):
    """Stores each stack image in its corresponding folder, according to the excel sheet. Renames all images to
    match Leika naming conventions. Creates MIP images out of all stack images. """

    channel_dict = {"C001" : "ch00", "C002" : "ch01", "C003" : "ch02"}

    stack_dict = {"Z001" : "z00", "Z002" : "z01", "Z003" : "z02", "Z004" : "z03", "Z005" : "z04", "Z006" : "z05", "Z007" : "z06", "Z008" : "z07", "Z009" : "z08", "Z010" : "z09", "Z011" : "z10", "Z012" : "z11", "Z013" : "z12",
     "Z014" : "z13", "Z015" : "z14", "Z016" : "z15", "Z017" : "z16", "Z018" : "z17", "Z019" : "z18", "Z020" : "z19", "Z021" : "z20", "Z022" : "z21", "Z023" : "z22", "Z024" : "z23", "Z025" : "z24", "Z026" : "z25",
     "Z027" : "z26", "Z028" : "z27", "Z29" : "z28", "Z030" : "z29", "Z031" : "z30", "Z032" : "z31", "Z033" : "z32", "Z034" : "z33", "Z035" : "z34", "Z036" : "z35", "Z037" : "z36", "Z038" : "z37", "Z039" : "z38",
     "Z040" : "z39"}

    stack_folders = os.listdir(chosen_folder)

    log_string = "Transfers executed on: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " \n \n"

    for i in range(len(stack_folders)):

        current_folder = stack_folders[i]
        list_path = image_locations[i]

        label = str(list_path[0]) + "_" + str(list_path[1]) + "_" + str(list_path[2]) + "_" + str(list_path[3])

        destination_path = os.path.join(save_folder, str(list_path[0]), str(list_path[1]), str(list_path[2]) + "_" + str(list_path[3]))
        shutil.move(os.path.join(chosen_folder, current_folder), destination_path)

        log_string += os.path.basename(current_folder) + "  ->  " + destination_path + "\n"

        old_folder = os.path.join(destination_path, os.path.basename(current_folder))
        new_folder = os.path.join(destination_path, "Stack")
        os.rename(old_folder, new_folder)

        for z_image in os.listdir(new_folder):
            new_label = label

            if z_image.endswith(".tif"):

                for z in stack_dict.keys():
                    if z in z_image:
                        new_label += "_" + stack_dict[z]

                for ch in channel_dict.keys():
                    if ch in z_image:
                        new_label += "_" + channel_dict[ch] + ".tif"

                new_img = os.path.join(new_folder, new_label)
                old_img = os.path.join(new_folder, z_image)

                os.rename(old_img, new_img)

        save_mips(new_folder, label)
        print("Completed: " + os.path.basename(current_folder) + "  ->  " + destination_path)

    return log_string


def save_mips(stack_folder, label):
    """Uses numpy.max() to create maximum z intensity projections of stack images. Labels according to Leika format."""

    channels = ["ch00", "ch01", "ch02"]
    mip_folder = os.path.join(os.path.dirname(stack_folder), "MIP")
    if not os.path.exists(mip_folder):
        os.mkdir(mip_folder)

    for ch in channels:

        stack = [tf.imread(os.path.join(stack_folder, f)) for f in os.listdir(stack_folder) if (ch in f)]

        zplanes = len(stack)
        shape = stack[0].shape
        rows, cols = shape[0], shape[1]
        final_stack = np.zeros((zplanes, rows, cols))

        for i in range(zplanes):
            final_stack[i,:,:] = stack[i]

        mip_img = np.max(final_stack, axis = 0)

        filename = label + "_MIP_" + ch + ".tif"
        tf.imsave(os.path.join(mip_folder, filename), mip_img.astype(np.uint16))


def save_log(log, dir):
    """Saves the log string as a dated .txt file"""

    save_path = os.path.join(dir, datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "_transfer_log.txt")
    with open(save_path,'w') as f:
        f.write(log)


def main():
    """ First selection made by user is a folder containing stack folders. Second selection is the corresponding excel sheet."""

    root = Tk()
    root.withdraw()
    chosen_folder = filedialog.askdirectory(initialdir = os.getcwd(), title = "Select the image folder.")

    blueprint_table = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Select the excel template.")
    blueprint = pd.read_excel(blueprint_table, sheet_name='Sheet1')
    image_locations = blueprint.values.tolist()

    save_folder = make_skeleton(chosen_folder, image_locations)
    log = populate(chosen_folder, image_locations, save_folder)
    save_log(log, save_folder)

if __name__ == "__main__":
    main()
