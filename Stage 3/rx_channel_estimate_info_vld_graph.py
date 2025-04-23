import serial
import matplotlib
import matplotlib.pyplot as plt

# הגדרת ה-backend של matplotlib (אם יש צורך)
matplotlib.use('TkAgg')  # או 'Agg' אם אין תמיכה ב-Tkinter

# הגדרות Serial
PORT = "COM10"  # עדכן את הפורט לפי המערכת שלך
BAUD_RATE = 115200
TIMEOUT = 5

def read_and_plot_rate(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    rx_channel_estimate_info_vld_data = []  # רשימה לאחסון נתוני rx_channel_estimate_info_vld
    
    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="rx_channel_estimate_info_vld", color="blue", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X (50 דגימות)
    ax.set_ylim(0, 2)  # טווח ראשוני עבור ציר ה-Y (נניח שזה ייראה כמו boolean או אינדקסים 0-1-2)
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("rx_channel_estimate_info_vld")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating rx_channel_estimate_info_vld graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"{line_data}")  # הצגת כל שורה שמתקבלת

            # אם יש את המילה "rx_channel_estimate_info_vld:" בשורה, ננסה לחלץ את הערך
            if "rx_channel_estimate_info_vld:" in line_data:
                try:
                    # חילוץ ה-rx_channel_estimate_info_vld מתוך השורה, והמרה ל-int
                    rx_channel_estimate_info_vld = int(line_data.split("rx_channel_estimate_info_vld:")[1].split(",")[0].strip())
                    print(f"Parsed rx_channel_estimate_info_vld: {rx_channel_estimate_info_vld}")  # הדפסה של rx_channel_estimate_info_vld שפורק
                    
                    rx_channel_estimate_info_vld_data.append(rx_channel_estimate_info_vld)
                    
                    # אם יש יותר מ-50 ערכים, נוריד את הראשון
                    if len(rx_channel_estimate_info_vld_data) > 50:
                        rx_channel_estimate_info_vld_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(rx_channel_estimate_info_vld_data)))  # עדכון ציר ה-X
                    line.set_ydata(rx_channel_estimate_info_vld_data)  # עדכון ציר ה-Y
                    ax.set_xlim(0, 50)  # הגבלת טווח ציר ה-X ל-50
                    
                    # עדכון טווח ציר ה-Y כך שיכלול את הערכים הקיימים
                    ax.set_ylim(min(rx_channel_estimate_info_vld_data) - 0.5, max(rx_channel_estimate_info_vld_data) + 0.5)  # עדכון טווח ה-Y כך שיכלול את הערכים
                    
                    plt.draw()  # גרום לממשק הגרפי להישאר פעיל
                    plt.pause(0.1)  # עדכון הגרף
                except ValueError as e:
                    print(f"Error parsing rx_channel_estimate_info_vld: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        plt.ioff()  # סיום מצב אינטראקטיבי
        plt.show()  # הוצאת הגרף בסוף התוכנית

# קריאה והפעלת הגרף
read_and_plot_rate(PORT, BAUD_RATE, TIMEOUT)
