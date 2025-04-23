import serial
import matplotlib
import matplotlib.pyplot as plt
import re

# שימוש ב-TkAgg כדי להימנע מבעיות תצוגה
matplotlib.use('TkAgg')

# הגדרות Serial
PORT = "COM10"  # יש לעדכן לפי הפורט המתאים
BAUD_RATE = 115200
TIMEOUT = 5

# ביטוי רגולרי לזיהוי הערך של rxmatch1
PATTERN = re.compile(r"rxmatch1:\s*(\d+)")

def read_and_plot_rxmatch1(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    rxmatch1_data = []  

    # הגדרת גרף
    plt.ion()  
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="rxmatch1 Values", color="orange", linewidth=2)
    ax.set_xlim(0, 50)  
    ax.set_ylim(0, 10)  
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("rxmatch1 Value")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating rxmatch1 graph... Press Ctrl+C to stop.")
        while True:
            line_data = ser.readline().decode("utf-8").strip()
            print(f"Received line: {line_data}")  
            
            # חיפוש ערך rxmatch1
            match = PATTERN.search(line_data)
            if match:
                try:
                    value = int(match.group(1))
                    print(f"Parsed rxmatch1: {value}")  
                        
                    rxmatch1_data.append(value)
                    
                    # אם יש יותר מ-50 ערכים, נמחק את הערך הישן ביותר
                    if len(rxmatch1_data) > 50:
                        rxmatch1_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(rxmatch1_data)))
                    line.set_ydata(rxmatch1_data)
                    ax.set_xlim(0, len(rxmatch1_data))  
                    ax.set_ylim(min(rxmatch1_data, default=0) - 1, max(rxmatch1_data, default=1) + 1)  
                    plt.draw()
                    plt.pause(0.1)  # שהייה קריטית למניעת קריסת הגרף
                except ValueError as e:
                    print(f"Error parsing rxmatch1: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        plt.ioff()
        plt.show()

# קריאה להפעלת הקוד
read_and_plot_rxmatch1(PORT, BAUD_RATE, TIMEOUT)
    