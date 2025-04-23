# FinalProject Overview

This project began by experimenting with predefined example codes to familiarize ourselves with the development environment and basic functionality. In the initial phase, we ran the following example programs:

- **Hello World**: A simple program to ensure the development setup is correctly configured.
- **Blink**: A basic LED blinking program to verify the board and GPIO functionality.
- **Fast Scan**: A test program that performs a fast scan to evaluate the scanning capabilities of the board with rssi data.
- **Blink&Fast Scan**:  Later, we merged these two codes and created a graph that represents the RSSI (Received Signal Strength Indicator) data collected at the moment. The LED blinked in different colors whenever the RSSI data exceeded a certain threshold, it was also shown at the graph.

You can find the main code for this phase in the "**Stage 1**" folder.

## Phase 2: CSI Data Collection

In the second phase, we advanced to collecting CSI (Channel State Information) data. We ran the code on two different board models:

- **ESP32-S3**
- **ESP32-C6**

The code for collecting CSI data on the ESP32-S3 was provided by Espressif. We ran the provided code on the ESP32-S3 board, and based on that code, we modified and adapted it to make it compatible with the ESP32-C6 board. These boards were then used to gather CSI data for further analysis and exploration.

Additionally, we printed the collected data from the ESP32-C6 board and visualized it in tables. One table represented all the variables, while a second table focused specifically on the CSI data. This allowed for a clearer understanding of the data and facilitated the exploration of the CSI features.

You can find the main code for this phase in the "**Stage 2**" folder.

## Phase 3: Visualizing CSI Data Features
In this phase, the focus was on visualizing various features of the CSI (Channel State Information) data collected over time. We created detailed graphs to represent key features such as Amplitude & Phase, RSSI, rate, timestamp, and more. These visualizations provided a clearer understanding of how the wireless environment behaves and the dynamic changes within the channel, allowing for a more thorough analysis of the collected data.

You can find the main code for this phase in the "**Stage 3**" folder.

## Phase 4: Integrating Graphs and Heatmap Analysis

Building on the visualizations from Phase 3, we combined all the graphs into a single comprehensive display, enabling real-time monitoring of all the data points in one view. In addition to the graphs, we introduced a heatmap to represent changes in amplitude and phase within the CSI data. The primary goal of this phase was to identify patterns in the CSI data and correlate them with changes in the physical environment, such as room layout and obstacles. By conducting this analysis, we aim to improve the understanding of how physical factors influence the wireless channel, helping to optimize wireless performance in real-world settings.

You can find the main code for this phase in the "**Stage 4**" folder.

## Phase 5: CSI Data Collection in Different Scenarios
In the final phase, we focused on collecting CSI data under different environmental conditions to analyze how movement and occupancy affect the wireless channel. We performed measurements in three different scenarios:

1. People moving in the room – to observe dynamic changes in the wireless signal.

2. People standing still in the room – to analyze the effect of static objects on the CSI data.

3. No people in the room – to establish a baseline for comparison.

Additionally, we implemented a sampling rate measurement to determine how many CSI samples were collected per second. This allowed us to assess the stability and efficiency of the data collection process, ensuring that the system operates at an optimal rate.

You can find the main code for this phase in the "**Stage 5**" folder.


## Code Files and Setup

For the every phase of the project, we have only included the `main` files in the repository. To run the code successfully, you will need to add additional files and configurations.

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
