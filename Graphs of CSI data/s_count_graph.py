import serial
import matplotlib
import matplotlib.pyplot as plt

# הגדרת ה-backend של matplotlib (אם יש צורך)
matplotlib.use('TkAgg')  # או 'Agg' אם אין תמיכה ב-Tkinter

# הגדרות Serial
PORT = "COM10"  # עדכן את הפורט לפי המערכת שלך
BAUD_RATE = 115200
TIMEOUT = 5

def read_and_plot_s_count(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    s_count_data = []  # רשימה לאחסון נתוני ה-s_count
    
    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="s_count", color="blue", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X
    ax.set_ylim(0, 50000)  # טווח ראשוני עבור ציר ה-Y (תעדכן לפי הצורך)
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("s_count")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating s_count graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"Received line: {line_data}")  # הצגת כל שורה שמתקבלת
            
            # אם יש את המילה "s_count:" בשורה, ננסה לחלץ את הערך
            if "s_count:" in line_data:
                try:
                    # חילוץ ה-s_count מתוך השורה
                    s_count = int(line_data.split("s_count:")[1].split(",")[0].strip())
                    print(f"Parsed s_count: {s_count}")  # הדפסה של ה-s_count שפורק
                    
                    s_count_data.append(s_count)
                    
                    # עדכון הגרף
                    if len(s_count_data) > 50:  # אם יש יותר מ-50 ערכים, נעצור
                        break
                    
                    line.set_xdata(range(len(s_count_data)))
                    line.set_ydata(s_count_data)
                    ax.set_xlim(0, len(s_count_data))  # עדכון טווח ציר ה-X
                    ax.set_ylim(0, max(s_count_data) * 1.1)  # התאמת טווח ציר ה-Y
                    plt.draw()  # גרום לממשק הגרפי להישאר פעיל
                    plt.pause(0.1)  # עדכון הגרף
                except ValueError as e:
                    print(f"Error parsing s_count: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        plt.ioff()  # סיום מצב אינטראקטיבי
        plt.show()  # הוצאת הגרף בסוף התוכנית

# קריאה והפעלת הגרף
read_and_plot_s_count(PORT, BAUD_RATE, TIMEOUT)
