<div >
    <img src="assets/owl.jpg" align="left" height="40px" width="40px"/>
    <img src="assets/medusa.png" align="right" height="40px" width="40px"/>
    <h1 align="center" > Theme-Changer - Python automatic theme changer for Windows </h1>
</div>

## About 
<img src="assets/python.png"  align=right width="65" height="75" />
Windows 11 automatic dark/light mode changer with gui written in python.

## Features

- GUI to select time of day in which you want light/dark mode to activate

- Select a wallpaper for each theme 


## Why?

I just wanted a lazy way to change themes in Windows because apparently it's to hard for such a small indie company to add such function and took is as an opportunity to practice some python.

## Requirements

- Python installed in your system and the pillow module or just downloading the release version (only tested locally as it's a bootleg personal project)
- 'Accent Colors' option in the Personalization > Colors section of the Windows Settings app should be set to automatic.

<figure align="center">
    <img src="assets/Settings.png" style="max-width: 50%; height: auto;" />
    <figcaption style="text-align:center">Mechanicus Wallpaper FTW</figcaption>
</figure>

## Usage

- Clone the repo and move it to the desired path.
```bash
git clone https://github.com/Alpharivs/theme-changer.git
```
- Run the GUI script for the initial setup or you compile it yourself with Pyinstaller.
```bash
python .\theme_changer.py
```
- Select the times and wallpapers that you want.

<figure align="center">
    <img src="assets/main.png" />
    <figcaption>Main Window</figcaption>
</figure>
<figure align="center">
    <img src="assets/time.png" />
    <figcaption style="text-align:center">Time Selection Window</figcaption>
</figure>




- Create a Scheduled Task to run the script I might update the program to create it automatically but for the time being a task the following settings:
    - Actions:
```
"start a program" action [path to your python.exe] argument [path to the theme_changer_task.py script]
```
<figure align="center">
    <img src="assets/example_action.png" />
    <figcaption style="text-align:center">Example action</figcaption>
</figure>

```bash
# You can get the path to your python.exe running python in the terminal and doing the following:
>>> import sys
>>> print(sys.executable)
```

- Triggers:
```
trigger set to at logon and repeat 1 hour should work without issues, don't worry if it's not time to change theme the app will exit without trying to change anything!
```
<figure align="center">
    <img src="assets/example_trigger.png" style="max-width: 40%; height: auto;"/>
    <figcaption style="text-align:center">Example action</figcaption>
</figure>



<h2 align="center" > LVX-SIT </h2>
<h3 align="center" > MMDCCLXXVII -- Ab urbe condita </h3>