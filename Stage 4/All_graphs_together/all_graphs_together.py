import serial
import matplotlib.pyplot as plt
import threading
import re
import math

# הגדרות לפורט
PORT = "COM10"
BAUD_RATE = 115200
TIMEOUT = 5

# אובייקט לאחסון הנתונים
DATA = {}

# מקסימום דגימות לתצוגה
MAX_SAMPLES = 50

# רשימת המפתחות (באותיות קטנות) שרוצים להציג
ALLOWED_KEYS = {
    "rx_seq",    # הוסף את rx_seq
    "s_count",   # הוסף את s_count
    "rssi", 
    "rate", 
    "timestamp", 
    "sig_len", 
    "rx_state", 
    "channel", 
    "cur_bb_format", 
    "cur_single_mpdu", 
    "noise_floor", 
    "rxend_state", 
    "second", 
    "rx_channel_estimate_info_vld", 
    "rx_channel_estimate_len", 
    "he_siga1", 
    "he_siga2", 
    "he_sigb_len", 
    "is_group", 
    "rxmatch0", 
    "rxmatch1", 
    "rxmatch2", 
    "rxmatch3"
}

def parse_data(line):
    """פונקציה לשליפת כל הנתונים מה-Serial.
    מסננת ומכניסה למילון DATA רק את המפתחות שב-ALLOWED_KEYS.
    המרת המפתח לאותיות קטנות מבטיחה שהסינון יהיה עקבי."""
    matches = re.findall(r"(\w+):\s*(-?\d+)", line)
    
    if matches:
        for key, value in matches:
            # המרת המפתח לאותיות קטנות
            key = key.lower()
            
            # אם המפתח אינו מופיע ברשימת המפתחות המורשים – דלג עליו
            if key not in ALLOWED_KEYS:
                continue

            if key not in DATA:
                DATA[key] = []
            # הוספת ערך חדש ונדחף את הערך הישן ביותר אם יש יותר מדי דגימות
            DATA[key].append(int(value))
            if len(DATA[key]) > MAX_SAMPLES:
                DATA[key].pop(0)

def read_serial():
    """קורא נתונים מה-Serial ושומר אותם במילון DATA"""
    ser = serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT)
    print("Starting to read from serial...")
    try:
        while True:
            line = ser.readline().decode("utf-8").strip()
            print(f"{line}")  # הדפסה למעקב
            parse_data(line)
    except KeyboardInterrupt:
        ser.close()

# יצירת חלון גרפים
plt.figure(figsize=(15, 10))
axes = []
lines = []

def init_graphs():
    """יוצר גרפים לכל המפתחות שנמצאו (לפי ALLOWED_KEYS)"""
    plt.clf()
    
    num_graphs = len(DATA)
    if num_graphs == 0:
        return
    
    # חישוב מספר העמודות והשורות כך שיהיו קרובים לריבוע
    cols = int(math.ceil(math.sqrt(num_graphs)))
    rows = math.ceil(num_graphs / cols)

    global axes, lines
    axes.clear()
    lines.clear()

    for i, key in enumerate(DATA.keys()):
        ax = plt.subplot(rows, cols, i + 1)
        # אין שימוש ב-label לעקומה כדי שלא יוצג legend
        line, = ax.plot([], [], linewidth=2)

        ax.set_xlim(0, MAX_SAMPLES)
        ax.set_ylim(-100, 100)
        ax.set_title(key, fontsize=10)
        ax.grid()

        axes.append(ax)
        lines.append(line)

# יצירת שרשור לקריאת Serial ברקע
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()

# לולאת עדכון הגרפים בזמן אמת
while True:
    # במידה ונוספו נתונים חדשים (מפתחות חדשים) – אתחל את הגרפים מחדש
    if DATA and (len(DATA) != len(axes)):
        print("Initializing graphs...")
        init_graphs()

    for i, key in enumerate(DATA.keys()):
        if DATA[key]:
            # עדכון גרף לכל מפתח
            lines[i].set_xdata(range(len(DATA[key])))  # הגדרת ציר ה-X
            lines[i].set_ydata(DATA[key])  # הגדרת ציר ה-Y
            # עדכון תחום הצירים כך שהגרף יתעדכן לפי הדגימות האחרונות
            axes[i].set_xlim(0, len(DATA[key]))  # הגדרת תחום ציר ה-X
            axes[i].set_ylim(min(DATA[key]) - 10, max(DATA[key]) + 10)

    plt.tight_layout()
    plt.draw()
    plt.pause(0.1)
