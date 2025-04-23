import serial
import matplotlib
import matplotlib.pyplot as plt

# הגדרת ה-backend של matplotlib (אם יש צורך)
matplotlib.use('TkAgg')  # או 'Agg' אם אין תמיכה ב-Tkinter

# הגדרות Serial
PORT = "COM10"  # עדכן את הפורט לפי המערכת שלך
BAUD_RATE = 115200
TIMEOUT = 5

def read_and_plot_is_group(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    is_group_data = []  # רשימה לאחסון נתוני ה-is_group
    
    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="is_group", color="green", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X (50 דגימות)
    ax.set_ylim(-1, 2)  # טווח ציר ה-Y (0 או 1)
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("is_group")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating is_group graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"{line_data}")  # הצגת כל שורה שמתקבלת

            # אם יש את המילה "is_group:" בשורה, ננסה לחלץ את הערך
            if "is_group:" in line_data:
                try:
                    # חילוץ ה-is_group מתוך השורה
                    is_group = int(line_data.split("is_group:")[1].split(",")[0].strip())
                    print(f"Parsed is_group: {is_group}")  # הדפסה של ה-is_group שפורק
                    
                    is_group_data.append(is_group)
                    
                    # אם יש יותר מ-50 ערכים, נוריד את הראשון
                    if len(is_group_data) > 50:
                        is_group_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(is_group_data)))  # עדכון ציר ה-X
                    line.set_ydata(is_group_data)  # עדכון ציר ה-Y
                    ax.set_xlim(0, 50)  # הגבלת טווח ציר ה-X ל-50
                    
                    # עדכון טווח ציר ה-Y
                    ax.set_ylim(-1, 2)  # מאחר ו-is_group הוא 0 או 1
                    
                    plt.draw()  # גרום לממשק הגרפי להישאר פעיל
                    plt.pause(0.1)  # עדכון הגרף
                except ValueError as e:
                    print(f"Error parsing is_group: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        plt.ioff()  # סיום מצב אינטראקטיבי
        plt.show()  # הוצאת הגרף בסוף התוכנית

# קריאה והפעלת הגרף
read_and_plot_is_group(PORT, BAUD_RATE, TIMEOUT)
