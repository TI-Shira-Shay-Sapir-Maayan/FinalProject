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
    rssi_data = []  # רשימה לאחסון נתוני ה-Rate
    
    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="Rssi", color="blue", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X
    ax.set_ylim(0, 100)  # טווח ראשוני עבור ציר ה-Y
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("Rssi")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating Rssi graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"Received line: {line_data}")  # הצגת כל שורה שמתקבלת
            
            # אם יש את המילה "rssi:" בשורה, ננסה לחלץ את הערך
            if "rssi:" in line_data:
                try:
                    # חילוץ ה-rssi מתוך השורה
                    rssi = float(line_data.split("rssi:")[1].split(",")[0].strip())
                    print(f"Parsed rate: {rssi}")  # הדפסה של ה-Rate שפורק
                    
                    rssi_data.append(rssi)
                    
                    # עדכון הגרף
                    if len(rssi_data) > 50:  # אם יש יותר מ-50 ערכים, נעצור
                        break
                    
                    line.set_xdata(range(len(rssi_data)))
                    line.set_ydata(rssi_data)
                    ax.set_xlim(0, len(rssi_data))  # עדכון טווח ציר ה-X
                    ax.set_ylim(0, max(rssi_data) * 1.1)  # התאמת טווח ציר ה-Y
                    plt.draw()  # גרום לממשק הגרפי להישאר פעיל
                    plt.pause(0.1)  # עדכון הגרף
                except ValueError as e:
                    print(f"Error parsing rssi: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        plt.ioff()  # סיום מצב אינטראקטיבי
        plt.show()  # הוצאת הגרף בסוף התוכנית

# קריאה והפעלת הגרף
read_and_plot_rate(PORT, BAUD_RATE, TIMEOUT)
