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

# ביטוי רגולרי לזיהוי הערך של rxmatch0
PATTERN = re.compile(r"rxmatch0:\s*(\d+)")

def read_and_plot_rxmatch0(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    rxmatch0_data = []  

    # הגדרת גרף
    plt.ion()  
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="rxmatch0 Values", color="blue", linewidth=2)
    ax.set_xlim(0, 50)  
    ax.set_ylim(0, 10)  
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("rxmatch0 Value")
    ax.legend()
    ax.grid()

    try:
        print("Reading data and updating rxmatch0 graph... Press Ctrl+C to stop.")
        while True:
            line_data = ser.readline().decode("utf-8").strip()
            print(f"Received line: {line_data}")  
            
            # חיפוש ערך rxmatch0
            match = PATTERN.search(line_data)
            if match:
                try:
                    value = int(match.group(1))
                    print(f"Parsed rxmatch0: {value}")  
                        
                    rxmatch0_data.append(value)
                    
                    # אם יש יותר מ-50 ערכים, נמחק את הערך הישן ביותר
                    if len(rxmatch0_data) > 50:
                        rxmatch0_data.pop(0)
                    
                    # עדכון הגרף
                    line.set_xdata(range(len(rxmatch0_data)))
                    line.set_ydata(rxmatch0_data)
                    ax.set_xlim(0, len(rxmatch0_data))  
                    ax.set_ylim(min(rxmatch0_data, default=0) - 1, max(rxmatch0_data, default=1) + 1)  
                    plt.draw()
                    plt.pause(0.1)  # שהייה קריטית למניעת קריסת הגרף
                except ValueError as e:
                    print(f"Error parsing rxmatch0: {line_data} | {e}")
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        plt.ioff()
        plt.show()

# קריאה להפעלת הקוד
read_and_plot_rxmatch0(PORT, BAUD_RATE, TIMEOUT)
