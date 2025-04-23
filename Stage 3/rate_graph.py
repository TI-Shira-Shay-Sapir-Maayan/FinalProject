import serial
import matplotlib.pyplot as plt

# הגדרות Serial
PORT = "COM10"  # עדכן את הפורט לפי המערכת שלך
BAUD_RATE = 115200
TIMEOUT = 5

def read_and_plot_rate(port, baud_rate, timeout):
    
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    rate_data = []  # רשימה לאחסון נתוני ה-Rate

    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="Rate", color="blue", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X (50 דגימות)
    ax.set_ylim(0, 100)  # טווח ראשוני עבור ציר ה-Y
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("Rate")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating rate graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"{line_data}")  # הצגת כל שורה שמתקבלת
            
            # אם יש את המילה "rate:" בשורה, ננסה לחלץ את הערך
            if "rate:" in line_data:
                try:
                    # חילוץ ה-rate מתוך השורה
                    rate = float(line_data.split("rate:")[1].split(",")[0].strip())
                    print(f"Parsed rate: {rate}")  # הדפסה של ה-Rate שפורק
                    
                    rate_data.append(rate)
                    
                    # אם יש יותר מ-50 ערכים, נוריד את הראשון
                    if len(rate_data) > 50:
                        rate_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(rate_data)))  # עדכון ציר ה-X
                    line.set_ydata(rate_data)  # עדכון ציר ה-Y
                    ax.set_xlim(0, 50)  # הגבלת טווח ציר ה-X ל-50
                    ax.set_ylim(0, max(rate_data) * 1.1 if rate_data else 100)  # עדכון טווח ציר ה-Y
                    plt.draw()  # גרום לממשק הגרפי להישאר פעיל
                    plt.pause(0.1)  # עדכון הגרף
                except ValueError as e:
                    print(f"Error parsing rate: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        ser.close()
        plt.ioff()  # סיום מצב אינטראקטיבי
        plt.show()

# קריאה והפעלת הגרף
read_and_plot_rate(PORT, BAUD_RATE, TIMEOUT)
