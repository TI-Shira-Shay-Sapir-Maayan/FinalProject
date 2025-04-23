import serial
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# הגדרת ה-backend של matplotlib (אם יש צורך)
matplotlib.use('TkAgg')  # או 'Agg' אם אין תמיכה ב-Tkinter

# הגדרות Serial
PORT = "COM10"  # עדכן את הפורט לפי המערכת שלך
BAUD_RATE = 115200
TIMEOUT = 5

def read_and_plot_rx_channel_estimate_len(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    rx_channel_estimate_len_data = []  # רשימה לאחסון הנתונים
    
    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="rx_channel_estimate_len", color="green", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X (50 דגימות)
    ax.set_ylim(120, 140)  # טווח ראשוני עבור ציר ה-Y
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("rx_channel_estimate_len")
    ax.legend()
    ax.grid()

    # הגדרת קפיצות של 0.5 בציר ה-Y
    yticks = np.arange(120, 140.5, 0.5)  # קפיצות של 0.5
    ax.set_yticks(yticks)

    try:
        print("Reading data and updating rx_channel_estimate_len graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"Received line: {line_data}")  # הצגת כל שורה שמתקבלת

            # אם יש את המילה "rx_channel_estimate_len:" בשורה, ננסה לחלץ את הערך
            if "rx_channel_estimate_len:" in line_data:
                try:
                    # חילוץ rx_channel_estimate_len מתוך השורה
                    rx_channel_estimate_len = float(line_data.split("rx_channel_estimate_len:")[1].split(",")[0].strip())
                    print(f"Parsed rx_channel_estimate_len: {rx_channel_estimate_len}")  # הדפסה של הערך שפורק
                    
                    rx_channel_estimate_len_data.append(rx_channel_estimate_len)
                    
                    # אם יש יותר מ-50 ערכים, נוריד את הראשון
                    if len(rx_channel_estimate_len_data) > 50:
                        rx_channel_estimate_len_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(rx_channel_estimate_len_data)))  # עדכון ציר ה-X
                    line.set_ydata(rx_channel_estimate_len_data)  # עדכון ציר ה-Y
                    ax.set_xlim(0, 50)  # הגבלת טווח ציר ה-X ל-50
                    
                    # עדכון טווח ציר ה-Y כך שיכלול את הערכים הקיימים
                    ax.set_ylim(min(rx_channel_estimate_len_data) - 1, max(rx_channel_estimate_len_data) + 1)
                    
                    plt.draw()  # גרום לממשק הגרפי להישאר פעיל
                    plt.pause(0.1)  # עדכון הגרף
                except ValueError as e:
                    print(f"Error parsing rx_channel_estimate_len: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        plt.ioff()  # סיום מצב אינטראקטיבי
        plt.show()  # הוצאת הגרף בסוף התוכנית

# קריאה והפעלת הגרף
read_and_plot_rx_channel_estimate_len(PORT, BAUD_RATE, TIMEOUT)
