<a name="readme-top"></a>

![GitHub contributors](https://img.shields.io/github/contributors/albertoibernon/Autonomous_Surveillance_Robot)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
<br />
<div align="center">
  
  <h3 align="center">Urban-flow-management-using-fuzzy-controlled-traffic-lights</h3>

  <p align="center">
    Appliacation of fuzzy control to traffic lights of an urban scenario to test the improvement of its impleation in area such as waitting time and avg speed
    <br />
    <a href="https://github.com/Drq13112/Urban-flow-management-using-fuzzy-controlled-traffic-lights/main/report.pdf"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#usage">View Demo</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This work is part of the course of *Artifical Inteligence* of the Master in Automatics and Robotics of the Polytechnic University of Madrid (UPM).

The aim of the work is to design an intelligent traffic management model. Traffic jams are a recurrent problem in large cities, and one possible solution is the development of a system that optimises the waiting time of vehicles and pedestrians, giving priority to the busiest avenues. To control the actual traffic, statistical studies are usually carried out to determine the usual flow of vehicles on each street in a city, so that traffic light times are adjusted according to this data.

This work aims to go one step further by creating a global system that allows to know how many vehicles and pedestrians there are in each street in real time. The system will be able to react and modify the waiting times of each traffic light according with he waiting times of each traffic light. 

To do this, it is necessary to sensor the roads and pavements, thus informing the number of users on each street. We are aware that this premise is a great difficulty when it comes to implementing this system in real cities, as it would mean placing cameras and sensors in each street. For this reason, the work will consist of recreating a world with a few roads, in which it will be possible to see how traffic is automatically regulated according to the number of vehicles.

The framework used was SUMO; https://eclipse.dev/sumo/

![Basic map](./figs/Basic.png)
*Figure 1: Basic pedestrian crossing *

Simple pedestrian crossing to test the dynamics of the Sumo simulator. It is also intended to examine whether the implementation of a fuzzy control offers immediate improvements.

![Map of testing](figs/map.png)
*Figure 2: Map of testing.*

## Usage
The following is a short video demonstrating the operation of the developed project.
![The gif](./figs/demo.gif)

In case someone wants to use it, it is necessary to install the sumo simulator and the scripst.py. Once downloaded and configured, set the execution path for the .py scripts and run them.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the BSD 3-Clause License. See `LICENSE.txt` for more information.
