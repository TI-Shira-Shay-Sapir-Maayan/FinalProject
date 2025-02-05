# FinalProject Overview

This project began by experimenting with predefined example codes to familiarize ourselves with the development environment and basic functionality. In the initial phase, we ran the following example programs:

- **Hello World**: A simple program to ensure the development setup is correctly configured.
- **Blink**: A basic LED blinking program to verify the board and GPIO functionality.
- **Fast Scan**: A test program that performs a fast scan to evaluate the scanning capabilities of the board with rssi data.
- **Blink&Fast Scan**:  Later, we merged these two codes and created a graph that represents the RSSI (Received Signal Strength Indicator) data collected at the moment. The LED blinked in different colors whenever the RSSI data exceeded a certain threshold, it was also shown at the graph.

## Phase 2: CSI Data Collection

In the second phase, we advanced to collecting **CSI (Channel State Information)** data. We ran the code on two different board models:
- **ESP32-S3**
- **ESP32-C6**

The code for collecting **CSI** data on the **ESP32-S3** was provided by Espressif. We ran the provided code on the ESP32-S3 board, and based on that code, we modified and adapted it to make it compatible with the **ESP32-C6** board. These boards were then used to gather CSI data for further analysis and exploration.

## Phase 3: Graphical Representation of CSI Features
In the third phase, we are focused on visualizing the changes in various CSI features over time. Specifically, we are creating graphs that represent the features of CSI data (like the Amplitude & Phase, RSSI, rate, timestamp and more). 
all the main code are on file **"Graps of CSI data"**. 

These visualizations help us better understand the behavior of the wireless environment and the dynamic properties of the channel.

## Phase 4: Merging Graphs and Analyzing CSI Data
In this phase, we merged all the graphs into a single file that displays all the data simultaneously. Additionally, we created a heatmap for the CSI (Channel State Information) data, illustrating changes in amplitude and phase. The objective of this step was to identify changes related to CSI and compare them with changes that are related to the physical environment of the room. By analyzing the changes in CSI data in relation to external factors in the room, we aim to better understand the dynamic behavior of the wireless channel and optimize it for the environment we are working in.

## Code Files and Setup

For the current phase of the project, we have only included the `main` files in the repository. To run the code successfully, you will need to add additional files and configurations.

### Required Files and Configurations

You can download the necessary files and configurations from the official Espressif website or GitHub repository.

- [Espressif Official Website](https://www.espressif.com)
- [Espressif GitHub Repository](https://github.com/espressif)

Please ensure that you have the appropriate configuration files and libraries set up before running the code.

## Instructions for Running the Code

1. Download the necessary files from the official Espressif sources.
2. Place the required files in the correct directories within the project folder.
3. Configure your development environment according to the board you are using (ESP32-S3 or ESP32-C6).
4. Compile and upload the code to the selected board.
5. Monitor the output to verify that the data collection is running correctly.

## Conclusion

This project is an ongoing effort to explore and utilize the capabilities of the ESP32-S3 and ESP32-C6 boards for collecting and analyzing Channel State Information (CSI). Future work will focus on further data analysis and optimization of the code for better performance across different environments.
