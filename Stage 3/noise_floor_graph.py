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
    noise_floor_data = []  # רשימה לאחסון נתוני noise_floor
    
    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="noise_floor", color="blue", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X (50 דגימות)
    ax.set_ylim(-100, 0)  # טווח ראשוני עבור ציר ה-Y (טווח רגיל עבור Noise Floor)
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("noise_floor")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating noise_floor graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"{line_data}")  # הצגת כל שורה שמתקבלת

            # אם יש את המילה "noise_floor:" בשורה, ננסה לחלץ את הערך
            if "noise_floor:" in line_data:
                try:
                    # חילוץ ה-noise_floor מתוך השורה
                    noise_floor = float(line_data.split("noise_floor:")[1].split(",")[0].strip())
                    print(f"Parsed noise_floor: {noise_floor}")  # הדפסה של noise_floor שפורק
                    
                    noise_floor_data.append(noise_floor)
                    
                    # אם יש יותר מ-50 ערכים, נוריד את הראשון
                    if len(noise_floor_data) > 50:
                        noise_floor_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(noise_floor_data)))  # עדכון ציר ה-X
                    line.set_ydata(noise_floor_data)  # עדכון ציר ה-Y
                    ax.set_xlim(0, 50)  # הגבלת טווח ציר ה-X ל-50
                    
                    # עדכון טווח ציר ה-Y כך שיכלול את הערכים הקיימים
                    ax.set_ylim(min(noise_floor_data) - 10, max(noise_floor_data) + 10)  # הגדלה של טווח ה-Y כדי לכלול גם ערכים קטנים
                    
                    plt.draw()  # גרום לממשק הגרפי להישאר פעיל
                    plt.pause(0.1)  # עדכון הגרף
                except ValueError as e:
                    print(f"Error parsing noise_floor: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        plt.ioff()  # סיום מצב אינטראקטיבי
        plt.show()  # הוצאת הגרף בסוף התוכנית

# קריאה והפעלת הגרף
read_and_plot_rate(PORT, BAUD_RATE, TIMEOUT)
