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
    cur_bb_format_data = []  # רשימה לאחסון נתוני cur_bb_format
    
    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="cur_bb_format", color="blue", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X (50 דגימות)
    ax.set_ylim(0, 5)  # טווח ראשוני עבור ציר ה-Y (אם cur_bb_format הוא בין 0 ל-4, לדוגמה)
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("cur_bb_format")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating cur_bb_format graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"{line_data}")  # הצגת כל שורה שמתקבלת

            # אם יש את המילה "cur_bb_format:" בשורה, ננסה לחלץ את הערך
            if "cur_bb_format:" in line_data:
                try:
                    # חילוץ ה-cur_bb_format מתוך השורה
                    cur_bb_format = int(line_data.split("cur_bb_format:")[1].split(",")[0].strip())
                    print(f"Parsed cur_bb_format: {cur_bb_format}")  # הדפסה של cur_bb_format שפורק
                    
                    cur_bb_format_data.append(cur_bb_format)
                    
                    # אם יש יותר מ-50 ערכים, נוריד את הראשון
                    if len(cur_bb_format_data) > 50:
                        cur_bb_format_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(cur_bb_format_data)))  # עדכון ציר ה-X
                    line.set_ydata(cur_bb_format_data)  # עדכון ציר ה-Y
                    ax.set_xlim(0, 50)  # הגבלת טווח ציר ה-X ל-50
                    
                    # עדכון טווח ציר ה-Y כך שיכלול את הערכים הקיימים
                    ax.set_ylim(min(cur_bb_format_data) - 1, max(cur_bb_format_data) + 1)  # הגדלה של טווח ה-Y כדי לכלול גם ערכים קטנים
                    
                    plt.draw()  # גרום לממשק הגרפי להישאר פעיל
                    plt.pause(0.1)  # עדכון הגרף
                except ValueError as e:
                    print(f"Error parsing cur_bb_format: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        plt.ioff()  # סיום מצב אינטראקטיבי
        plt.show()  # הוצאת הגרף בסוף התוכנית

# קריאה והפעלת הגרף
read_and_plot_rate(PORT, BAUD_RATE, TIMEOUT)
