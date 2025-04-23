import serial
import matplotlib.pyplot as plt

# הגדרות Serial
PORT = "COM10"  # עדכן את הפורט לפי המערכת שלך
BAUD_RATE = 115200
TIMEOUT = 5

def read_and_plot_channel(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    channel_data = []  # רשימה לאחסון נתוני ה-Channel
    
    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="Channel", color="green", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X (50 דגימות)
    ax.set_ylim(0, 100)  # טווח ראשוני עבור ציר ה-Y
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("Channel")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating channel graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"{line_data}")  # הצגת כל שורה שמתקבלת
            
            # אם יש את המילה "channel:" בשורה, ננסה לחלץ את הערך
            if "channel:" in line_data:
                try:
                    # חילוץ ה-channel מתוך השורה
                    channel = float(line_data.split("channel:")[1].split(",")[0].strip())
                    print(f"Parsed channel: {channel}")  # הדפסה של ה-Channel שפורק
                    
                    channel_data.append(channel)
                    
                    # אם יש יותר מ-50 ערכים, נוריד את הראשון
                    if len(channel_data) > 50:
                        channel_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(channel_data)))  # עדכון ציר ה-X
                    line.set_ydata(channel_data)  # עדכון ציר ה-Y
                    ax.set_xlim(0, 50)  # הגבלת טווח ציר ה-X ל-50
                    ax.set_ylim(0, max(channel_data) * 1.1 if channel_data else 100)  # עדכון טווח ציר ה-Y
                    plt.draw()  # גרום לממשק הגרפי להישאר פעיל
                    plt.pause(0.1)  # עדכון הגרף
                except ValueError as e:
                    print(f"Error parsing channel: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        ser.close()
        plt.ioff()  # סיום מצב אינטראקטיבי
        plt.show()

# קריאה והפעלת הגרף
read_and_plot_channel(PORT, BAUD_RATE, TIMEOUT)
