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
This program utilizes the following python libraries:
- PyQt5
- matplotlib
- numpy
- Scipy

##How to Use

This program is best ran from an IDE as the file structure needs to be updated to allow for command line execution. It has been tested and ran using the PyCharm IDE.

The startup screen is shown below
![Startup Screen](\REAdME images\StartUp.jpg)
