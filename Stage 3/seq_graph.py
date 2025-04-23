import serial
import matplotlib.pyplot as plt

# הגדרות Serial
PORT = "COM10"  # עדכן את הפורט לפי המערכת שלך
BAUD_RATE = 115200
TIMEOUT = 5

def read_and_plot_rx_seq(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    rx_seq_data = []  # רשימה לאחסון נתוני ה-rx_seq
    
    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="RX Seq", color="green", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X (50 דגימות)
    ax.set_ylim(0, 100)  # טווח ראשוני עבור ציר ה-Y
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("RX Seq")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating rx_seq graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"{line_data}")  # הצגת כל שורה שמתקבלת
            
            # אם יש את המילה "rx_seq:" בשורה, ננסה לחלץ את הערך
            if "rx_seq:" in line_data:
                try:
                    # חילוץ ה-rx_seq מתוך השורה
                    rx_seq = float(line_data.split("rx_seq:")[1].split(",")[0].strip())
                    print(f"Parsed rx_seq: {rx_seq}")  # הדפסה של ה-rx_seq שפורק
                    
                    rx_seq_data.append(rx_seq)
                    
                    # אם יש יותר מ-50 ערכים, נוריד את הראשון
                    if len(rx_seq_data) > 50:
                        rx_seq_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(rx_seq_data)))  # עדכון ציר ה-X
                    line.set_ydata(rx_seq_data)  # עדכון ציר ה-Y
                    ax.set_xlim(0, 50)  # הגבלת טווח ציר ה-X ל-50
                    ax.set_ylim(0, max(rx_seq_data) * 1.1 if rx_seq_data else 100)  # עדכון טווח ציר ה-Y
                    plt.draw()  # גרום לממשק הגרפי להישאר פעיל
                    plt.pause(0.1)  # עדכון הגרף
                except ValueError as e:
                    print(f"Error parsing rx_seq: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        ser.close()
        plt.ioff()  # סיום מצב אינטראקטיבי
        plt.show()

# קריאה והפעלת הגרף
read_and_plot_rx_seq(PORT, BAUD_RATE, TIMEOUT)
