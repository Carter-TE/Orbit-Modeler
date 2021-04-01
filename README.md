# Orbit-Modeler
Program that can plot and animate orbits and satellite positions as well as calculate transfer orbits. Works best with orbits that have shorter periods (<=12 hrs). 

Alpha v 2.3

*Optimization needed for periods >6 hrs*

##Inspiration
I have always found orbital mechanics intersting and wanted to take deeper dive to understanding them. In my preliminary research I gained a fascination for transfer orbits and what it takes to get two satelites to meet at a point at the same time. 

##Features:

###Primary 
- Graph the shape of ip to 2 sattellite orbits in the equatorial plane 
- Plot Hohmann manuvers between two satellites
- Animate normal orbits and Hohmann transfers

###Secondary
- Predict future satellite positions
- Determine time until next possible Hohmann transfer orbit 

##Dependencies
This program was developed on Python3 and utilizes the following libraries:
- PyQt5
- matplotlib
- numpy
- Scipy

##How to Use

This standalone program can be exucted from command line by first navigating to the directory where the .py files are saved and then excuting GUI.py file with the command `Python GUI.py`


The startup screen is shown below
![Startup Screen](./README![StartUp](https://user-images.githubusercontent.com/56568421/113329818-e81e0100-92d2-11eb-8da9-ef248710a33a.jpg)

After clicking "Begin" you will be brought to the main screen where you can input orbital and planetary parameters and selecta plotting feature. The default input values are set to model a spacecraft transfering from a higher orbit to the International Space Station around Earth. These default values highlight the functionaloty of the application well. 

The main screen is shown below

![InputScreen](https://user-images.githubusercontent.com/56568421/113331170-747cf380-92d4-11eb-9caa-e76dea399fb6.jpg)

After inputting the desired orbiatal values and selecting a plotting feature, a window will pop up with with the staelite orbits. It may take a moment to initialize the sattelite values. Console printouts will detail the current stage in this process. 

Below are the printouts and plots for the transfer orbit using the default values.

![ConsolePrintouts](https://user-images.githubusercontent.com/56568421/113332952-b870f800-92d6-11eb-950e-24e8806a535b.jpg)

The values printed out after the transfer orbit is calculated are as follows:

\[initial position of transferring satellite, initial position of other sat, delta t of the transfer, time until transfer window from inputted initial values]

![GraphedTransfer](https://user-images.githubusercontent.com/56568421/113332974-bdce4280-92d6-11eb-92c9-943d4d18ce89.jpg)



