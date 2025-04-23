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
    second_data = []  # רשימה לאחסון נתוני second
    
    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="second", color="blue", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X (50 דגימות)
    ax.set_ylim(0, 2)  # טווח ראשוני עבור ציר ה-Y (נניח שזה ייראה כמו boolean או אינדקסים 0-1-2)
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("second")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating second graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"{line_data}")  # הצגת כל שורה שמתקבלת

            # אם יש את המילה "second:" בשורה, ננסה לחלץ את הערך
            if "second:" in line_data:
                try:
                    # חילוץ ה-second מתוך השורה, והמרה ל-int
                    second = int(line_data.split("second:")[1].split(",")[0].strip())
                    print(f"Parsed second: {second}")  # הדפסה של second שפורק
                    
                    second_data.append(second)
                    
                    # אם יש יותר מ-50 ערכים, נוריד את הראשון
                    if len(second_data) > 50:
                        second_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(second_data)))  # עדכון ציר ה-X
                    line.set_ydata(second_data)  # עדכון ציר ה-Y
                    ax.set_xlim(0, 50)  # הגבלת טווח ציר ה-X ל-50
                    
                    # עדכון טווח ציר ה-Y כך שיכלול את הערכים הקיימים
                    ax.set_ylim(min(second_data) - 0.5, max(second_data) + 0.5)  # עדכון טווח ה-Y כך שיכלול את הערכים
                    
                    plt.draw()  # גרום לממשק הגרפי להישאר פעיל
                    plt.pause(0.1)  # עדכון הגרף
                except ValueError as e:
                    print(f"Error parsing second: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        plt.ioff()  # סיום מצב אינטראקטיבי
        plt.show()  # הוצאת הגרף בסוף התוכנית

# קריאה והפעלת הגרף
read_and_plot_rate(PORT, BAUD_RATE, TIMEOUT)
