import os
import shutil
import tkinter
import pathlib
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename
from configparser import ConfigParser
from PIL import Image

def create_configuration():
    config = ConfigParser()
    current_directory = os.getcwd()
    image_directory = os.path.join(current_directory, r"images")
    # Check if config.ini already exists in current folder and if not create it with dummy values.
    if not os.path.exists("config.ini"):
        config["Settings"] = {"nightmodetime": "0", "lightmodetime": "0", "imagepath": f"{image_directory}",}
        with open("config.ini", "w") as config_file:
            config.write(config_file)
    # Check if images file already exists in current directory and if not create it
    if not os.path.exists(image_directory):
            os.makedirs(image_directory)

def validate_image(file_path):
    try:
        # Attempt to open the image file and if successful it's a valid image
        with Image.open(file_path) as image:
            return image.format is not None
    except Exception:
        showinfo(title="Error", message="File is not a valid image.")
        return False

def choose_image(mode):
    try:
        # Spawn file select window     
        filename = askopenfilename()
        # Check if window is closed without selection.
        if not filename:
            showinfo(title="Warning", message="No image was selected")
            return
        # Validate Image
        if not validate_image(filename):
            return
        # Directory and File Operations
        image_directory = os.getcwd() + "\images"
        extension = pathlib.Path(filename).suffix
        # Check if a another wallpaper for the desired mode already exists
        for file in os.listdir(image_directory):
            if file.startswith(mode):
                os.remove(os.path.join(image_directory, file))
        # Copy Image
        shutil.copyfile(filename, fr"{image_directory}\{mode}{extension}")
        showinfo(title="Selected File", message=filename)
    
    except Exception :
        showinfo(title="Error", message="An error occurred while processing the file.")

def submit(night, light):
    # Function created to get user data either when pressing the button or the enter key.
    modify_configuration(0, night)
    modify_configuration(1, light)

def modify_configuration(mode, new_time):
    # Open the config.ini file
    configure = ConfigParser()
    configure.read("config.ini")

    # If only one value is passed ignore the other.
    if new_time == "":
        return None
    # Validate the input and set the time selected for night mode which is mode=0
    elif mode == 0:
        try:
            time = validate_input(new_time)

            configure.set("Settings", "NightModeTime", time)
            with open("config.ini", "w") as config_file:
                configure.write(config_file)
            showinfo(title="Success", message="Night time has been modified")
        
        except Exception:
            showinfo(title="Error", message="An error occurred while setting the new time.")
    # Do the same for light mode which is mode=1
    else:
        try:
            time = validate_input(new_time)

            configure.set("Settings", "lightmodetime", time)
            with open("config.ini", "w") as config_file:
                configure.write(config_file)
            showinfo(title="Success", message="Light time has been modified")
        
        except Exception:
            showinfo(title="Error", message="An error occurred while setting the new time.")

def validate_input(input):
    # Check if the input is an integer between 0 and 24.
    try:
        new_time = int(input)
        if new_time < 0 or new_time > 24:
            showinfo(title="Error", message="Time is not within a valid range")
        else:
            return (str(new_time))
    except ValueError:
        showinfo(title="Error", message="Input is not a valid number, please use only whole numbers")

def time_window():
    # Nested function for closing the window when values have been submited
    def close_top():
        top.destroy()
        top.update()
    # Initialize time select window
    top = Toplevel()
    top.title("Input the desired hour")
    top.resizable(False, False)
    # Get screen size, make the window appear in the center of the screen and set size.
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (300/2))
    y_cordinate = int((screen_height/2) - (100/2))
    top.geometry(f"300x150+{x_cordinate}+{y_cordinate}")
    # Create input fields
    Label(top, text="Night mode time (24h format)", font=("Calibri 10")).pack()
    user_input_night=Entry(top, width=35)
    # The lambda permits us to call the submit func and close the window.
    user_input_night.bind(
        "<Return>",
        (lambda event: [submit(user_input_night.get(), user_input_light.get()), close_top()]) 
    )
    user_input_night.pack()

    Label(top, text="Light mode time (24h format)", font=("Calibri 10")).pack()
    user_input_light=Entry(top, width=35)
    user_input_light.bind(
        "<Return>",
       (lambda event: [submit(user_input_night.get(), user_input_light.get()), close_top()])
    )
    user_input_light.pack()
    # Create Submit Button
    button = ttk.Button(
        top,
        text="Submit",
        command=(lambda : [submit(user_input_night.get(), user_input_light.get()), close_top()])
    )
    button.pack(side=tkinter.TOP)

if __name__ == '__main__':
    # Check if configuration file exists or create it.
    create_configuration()
    # Initialize Root Window
    root = tkinter.Tk()
    root.title("Theme changer configuration")
    root.resizable(False, False)
    # Get screen size, make the window appear in the center of the screen and set size.
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (300/2))
    y_cordinate = int((screen_height/2) - (100/2))
    root.geometry(f"370x100+{x_cordinate}+{y_cordinate}")
    # Create Buttons, the lambda allows us to pass an argument to the dunction acting as command.
    light_button = ttk.Button(
        root,
        text= "Light Mode Wallpaper",
        command= lambda: choose_image("light") 
    )
    light_button.pack(expand=True, side=tkinter.LEFT)

    night_button = ttk.Button(
        root,
        text= "Night Mode Wallpaper",
        command= lambda: choose_image("night") 
    )
    night_button.pack(expand=True, side=tkinter.RIGHT)

    time_button = ttk.Button(
        root,
        text= "Select Time",
        command=time_window 
    )
    time_button.pack(expand=True, side=tkinter.TOP)

    root.mainloop()