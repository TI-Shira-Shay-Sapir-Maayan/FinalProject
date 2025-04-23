import serial
import matplotlib.pyplot as plt

# הגדרות Serial
PORT = "COM10"  # עדכן את הפורט לפי המערכת שלך
BAUD_RATE = 115200
TIMEOUT = 5

def read_and_plot_timestamp(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    timestamp_data = []  # רשימה לאחסון נתוני ה-timestamp
    
    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="Timestamp", color="green", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X (50 דגימות)
    ax.set_ylim(0, 100)  # טווח ראשוני עבור ציר ה-Y
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("Timestamp")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating timestamp graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"{line_data}")  # הצגת כל שורה שמתקבלת
            
            # אם יש את המילה "timestamp:" בשורה, ננסה לחלץ את הערך
            if "timestamp:" in line_data:
                try:
                    # חילוץ ה-timestamp מתוך השורה
                    timestamp = float(line_data.split("timestamp:")[1].split(",")[0].strip())
                    print(f"Parsed timestamp: {timestamp}")  # הדפסה של ה-timestamp שפורק
                    
                    timestamp_data.append(timestamp)
                    
                    # אם יש יותר מ-50 ערכים, נוריד את הראשון
                    if len(timestamp_data) > 50:
                        timestamp_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(timestamp_data)))  # עדכון ציר ה-X
                    line.set_ydata(timestamp_data)  # עדכון ציר ה-Y
                    ax.set_xlim(0, 50)  # הגבלת טווח ציר ה-X ל-50
                    ax.set_ylim(0, max(timestamp_data) * 1.1 if timestamp_data else 100)  # עדכון טווח ציר ה-Y
                    plt.draw()  # גרום לממשק הגרפי להישאר פעיל
                    plt.pause(0.1)  # עדכון הגרף
                except ValueError as e:
                    print(f"Error parsing timestamp: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        ser.close()
        plt.ioff()  # סיום מצב אינטראקטיבי
        plt.show()

# קריאה והפעלת הגרף
read_and_plot_timestamp(PORT, BAUD_RATE, TIMEOUT)
