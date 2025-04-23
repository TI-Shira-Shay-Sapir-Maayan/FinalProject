import serial
import matplotlib.pyplot as plt

# הגדרות Serial
PORT = "COM10"  # עדכן את הפורט לפי המערכת שלך
BAUD_RATE = 115200
TIMEOUT = 5

def read_and_plot_sig_len(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    sig_len_data = []  # רשימה לאחסון נתוני ה-sig_len
    
    # הגדרת גרף
    plt.ion()  # מצב אינטראקטיבי
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="Signal Length", color="purple", linewidth=2)
    ax.set_xlim(0, 50)  # טווח ראשוני עבור ציר ה-X (50 דגימות)
    ax.set_ylim(0, 100)  # טווח ראשוני עבור ציר ה-Y
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("Signal Length")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating sig_len graph... Press Ctrl+C to stop.")
        while True:
            # קריאה משורת ה-Serial
            line_data = ser.readline().decode("utf-8").strip()
            print(f"{line_data}")  # הצגת כל שורה שמתקבלת
            
            # אם יש את המילה "sig_len:" בשורה, ננסה לחלץ את הערך
            if "sig_len:" in line_data:
                try:
                    # חילוץ ה-sig_len מתוך השורה
                    sig_len = float(line_data.split("sig_len:")[1].split(",")[0].strip())
                    print(f"Parsed sig_len: {sig_len}")  # הדפסה של ה-sig_len שפורק
                    
                    sig_len_data.append(sig_len)
                    
                    # אם יש יותר מ-50 ערכים, נוריד את הראשון
                    if len(sig_len_data) > 50:
                        sig_len_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(sig_len_data)))  # עדכון ציר ה-X
                    line.set_ydata(sig_len_data)  # עדכון ציר ה-Y
                    ax.set_xlim(0, 50)  # הגבלת טווח ציר ה-X ל-50
                    ax.set_ylim(0, max(sig_len_data) * 1.1 if sig_len_data else 100)  # עדכון טווח ציר ה-Y
                    plt.draw()  # גרום לממשק הגרפי להישאר פעיל
                    plt.pause(0.1)  # עדכון הגרף
                except ValueError as e:
                    print(f"Error parsing sig_len: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        ser.close()
        plt.ioff()  # סיום מצב אינטראקטיבי
        plt.show()

# קריאה והפעלת הגרף
read_and_plot_sig_len(PORT, BAUD_RATE, TIMEOUT)
