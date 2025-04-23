import serial
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import re

matplotlib.use('TkAgg')

PORT = "COM10"  # עדכני לפי הפורט הנכון
BAUD_RATE = 115200
TIMEOUT = 5

# דפוס regex עם בדיקה לכל ארבעת הערכים ב-rxmatch3
PATTERN = re.compile(r"rxmatch3:\s*(\d+),(\d+),(\d+),\s*\"(\[.*\])\"")

def read_and_plot_heatmap(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    heatmap_data = []  # רשימה לאחסון הערכים לאורך זמן

    plt.ion()
    fig, ax = plt.subplots()
    heatmap = None

    try:
        print("Reading data and updating heatmap... Press Ctrl+C to stop.")
        while True:
            line_data = ser.readline().decode("utf-8").strip()
            print(f"{line_data}")

            match = PATTERN.search(line_data)
            if match:
                try:
                    values = [int(match.group(i)) for i in range(1, 4)]  # חילוץ שלושת הערכים הראשונים
                    print(f"Matched values: {values}")

                    # הוספת הערכים לטבלת החום
                    heatmap_data.append(values)
                    if len(heatmap_data) > 50:  # הגבלת מספר השורות בטבלה
                        heatmap_data.pop(0)

                    # המרה למערך NumPy לעדכון ה-Heatmap
                    heatmap_array = np.array(heatmap_data)

                    # עדכון טבלת החום
                    if heatmap is None:
                        heatmap = ax.imshow(heatmap_array.T, aspect="auto", cmap="viridis", interpolation="nearest")
                        plt.colorbar(heatmap, ax=ax)
                        ax.set_xlabel("Time (samples)")
                        ax.set_ylabel("rxmatch3 Values")
                        ax.set_yticks(range(len(values)))
                        ax.set_yticklabels([f"Value {i+1}" for i in range(len(values))])
                    else:
                        heatmap.set_data(heatmap_array.T)
                        ax.set_xlim(0, len(heatmap_data))
                        ax.set_ylim(-0.5, len(values) - 0.5)

                    plt.draw()
                    plt.pause(0.1)
                except ValueError as e:
                    print(f"Error parsing values: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        plt.ioff()
        plt.show()

read_and_plot_heatmap(PORT, BAUD_RATE, TIMEOUT)
