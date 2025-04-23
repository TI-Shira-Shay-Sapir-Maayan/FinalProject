import serial
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import re

# הגדרת הפורט הסיריאלי
port = "COM6"
baud_rate = 115200

# פתיחת חיבור סיריאלי
ser = serial.Serial(port, baud_rate, timeout=1)

# השהיה של זמן קטן על מנת לוודא שהחיבור הסיריאלי מוכן
time.sleep(2)

# יצירת הגרף
plt.ion()  # מצב אינטרקטיבי (לא יתחיל להמתין)
fig, ax = plt.subplots()
ax.set_title('RSSI over Time')
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('RSSI (dBm)')

# יצירת עיגול מואר בצד ימין למעלה
circle = patches.Circle((0.95, 0.95), 0.05, transform=ax.transAxes, color='gray')
ax.add_patch(circle)

# פונקציה להמיר ערך RSSI לצבע
def rssi_to_color(rssi):
    if rssi > -50:
        return (1, 0, 0)  # אדום (חוזק אות מאוד גבוה)
    elif rssi > -60:
        return (1, 0.27, 0)  # כתום כהה
    elif rssi > -70:
        return (1, 0.65, 0)  # כתום
    elif rssi > -80:
        return (1, 1, 0)  # צהוב
    elif rssi > -85:
        return (0.68, 1, 0.18)  # ירוק בהיר
    elif rssi > -90:
        return (0, 1, 0)  # ירוק
    else:
        return (0, 0, 1)  # כחול


# קריאה מהחיבור הסיריאלי
start_time = time.time()  # זמן התחלה

# יצירת הגרף הראשוני (רק קווים, ללא נקודות)
line_plot, = ax.plot([], [], label='RSSI')  # הגרף לא יציג נתונים כי לא נוספו נתונים
ax.legend()

# רשימות לצורך שמירת הנתונים
rssi_data = []
timestamps = []

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()  # קריאה ושינוי לפורמט טקסט
        print(f"Raw data: {line}")  # הדפסת הנתונים הגולמיים
        
        # שימוש ברגולר אקספרשן כדי לחלץ את הערך המספרי (RSSI)
        match = re.search(r'(-?\d+)', line)
        
        if match:
            try:
                rssi_value = int(match.group(1))  # אם זה ערך RSSI
                print(f"Received RSSI: {rssi_value} dBm")
                
                # הוספת נתונים לגרף
                current_time = time.time() - start_time
                rssi_data.append(rssi_value)
                timestamps.append(current_time)
                
                # עדכון הגרף (רק קווים)
                line_plot.set_xdata(timestamps)  # עדכון ציר ה-X
                line_plot.set_ydata(rssi_data)  # עדכון ציר ה-Y
                ax.relim()  # עדכון גבולות הצירים
                ax.autoscale_view()  # התאמת הצירים

                # שינוי צבע של העיגול לפי RSSI
                color = rssi_to_color(rssi_value)
                circle.set_facecolor(color)

                # שינוי צבע של הקו לפי RSSI
                line_plot.set_color(color)
                
                plt.draw()
                plt.pause(0.1)  # השהיה קלה על מנת לא להעמיס על המערכת
            except ValueError:
                print("Invalid RSSI value, skipping...")  # הודעה במקרה של שגיאה בהמרת נתונים
        else:
            print("No valid RSSI found, skipping...")  # הודעה אם לא נמצא ערך RSSI מתאים

plt.show()  # הוספת קריאה ל-plt.show() כדי להציג את הגרף
