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
    rssi_data = []  # רשימה לאחסון נתוני ה-Rssi
    
    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="Rssi", color="blue", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X (50 דגימות)
    ax.set_ylim(-100, 100)  # טווח ראשוני עבור ציר ה-Y (הגדלנו את טווח ה-Y)
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("Rssi")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating Rssi graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"{line_data}")  # הצגת כל שורה שמתקבלת

            # אם יש את המילה "rssi:" בשורה, ננסה לחלץ את הערך
            if "rssi:" in line_data:
                try:
                    # חילוץ ה-rssi מתוך השורה
                    rssi = float(line_data.split("rssi:")[1].split(",")[0].strip())
                    print(f"Parsed rssi: {rssi}")  # הדפסה של ה-Rssi שפורק
                    
                    rssi_data.append(rssi)
                    
                    # אם יש יותר מ-50 ערכים, נוריד את הראשון
                    if len(rssi_data) > 50:
                        rssi_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(rssi_data)))  # עדכון ציר ה-X
                    line.set_ydata(rssi_data)  # עדכון ציר ה-Y
                    ax.set_xlim(0, 50)  # הגבלת טווח ציר ה-X ל-50
                    
                    # עדכון טווח ציר ה-Y כך שיכלול את הערכים הקיימים
                    ax.set_ylim(min(rssi_data) - 10, max(rssi_data) + 10)  # הגדלה של טווח ה-Y כדי לכלול גם ערכים קטנים
                    
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
