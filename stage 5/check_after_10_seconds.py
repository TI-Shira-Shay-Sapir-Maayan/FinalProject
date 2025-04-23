import serial
import re
import csv
import time  # הוספנו את מודול time
import math

# הגדרות חיבור Serial
PORT = "COM10"  # עדכני לפורט שבו ה-ESP32 מחובר (ניתן לבדוק ב-Device Manager)
BAUD_RATE = 115200  # קצב תואם ל-ESP32
TIMEOUT = 2  # זמן המתנה לחיבור

# קובץ פלט
output_csv = "csi_data.csv"

# פונקציה לחישוב אמפליטודה ופאזה
def calculate_amplitude_phase(csi_data):
    # המרת הנתונים לרשימה של מספרים
    csi_data = list(map(int, csi_data))  # המרת כל הערכים למספרים שלמים
    
    # חישוב האמפליטודה והפאזה
    amplitudes = []
    phases = []
    
    for i in range(0, len(csi_data), 2):  # אם יש זוגות של ערכים (חלק ריאלי ודמיוני)
        real = csi_data[i]
        imaginary = csi_data[i + 1] if i + 1 < len(csi_data) else 0  # אם יש רק מספר אחד, נניח שהוא רק ריאלי
        amplitude = math.sqrt(real**2 + imaginary**2)  # חישוב האמפליטודה
        phase = math.atan2(imaginary, real)  # חישוב הפאזה
        amplitudes.append(amplitude)
        phases.append(phase)
    
    return amplitudes, phases

# פונקציה לקריאת נתוני CSI מה-Serial
def read_csi_data_from_serial(port, baud_rate, timeout, max_iterations=5000):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    data = []
    iteration_count = 0  # סופר את מספר האיטרציות
    try:
        while iteration_count < max_iterations:
            line = ser.readline().decode("utf-8").strip()
            if line.startswith("CSI_DATA-"):
                # חלוקה לפי פסיקים
                parts = line.split(",")

                # חילוץ MAC
                mac_match = re.search(r'CSI_DATA- ([0-9a-fA-F:]+)', line)
                mac = mac_match.group(1) if mac_match else "Unknown"

                # חילוץ CSI_Data
                csi_data_match = re.search(r'\[(.*?)\]', line)
                csi_data = csi_data_match.group(1).split(",") if csi_data_match else []

                # חישוב האמפליטודה והפאזה
                amplitudes, phases = calculate_amplitude_phase(csi_data)

                # הכנת מילון עם הערכים
                entry = {
                    "seq": int(parts[1].strip()),
                    "mac": mac,
                    "rssi": int(parts[2].strip()),
                    "rate": int(parts[3].strip()),
                    "timestamp": int(parts[4].strip()),
                    "signal_len": int(parts[5].strip()),
                    "rx_state": int(parts[6].strip()),
                    "channel": int(parts[7].strip()),
                    "secondary_channel": int(parts[8].strip()),
                    "bb_format": int(parts[9].strip()),
                    "single_mpdu": int(parts[10].strip()),
                    "noise_floor": int(parts[11].strip()),
                    "rx_end_state": int(parts[12].strip()),
                    "second": int(parts[13].strip()),
                    "rx_estimate_info_valid": int(parts[14].strip()),
                    "rx_estimate_len": int(parts[15].strip()),
                    "he_siga1": int(parts[16].strip()),
                    "he_siga2": int(parts[17].strip()),
                    "he_sigb_len": int(parts[18].strip()),
                    "is_group": int(parts[19].strip()),
                    "rxmatch0": int(parts[20].strip()),
                    "rxmatch1": int(parts[21].strip()),
                    "rxmatch2": int(parts[22].strip()),
                    "rxmatch3": int(parts[23].strip()),
                    "csi_data": csi_data,
                    "amplitudes": amplitudes,
                    "phases": phases,
                }
                data.append(entry)
                iteration_count += 1  # עדכון מספר האיטרציות
                print(f"Read entry: {entry}")  # אופציונלי להצגת הנתונים בזמן אמת
    except KeyboardInterrupt:
        print("Stopped reading from Serial.")
    finally:
        ser.close()
    return data

# פונקציה לשמירת הנתונים בקובץ CSV
def save_to_csv(data, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # כותרות
        headers = [
            "Seq", "MAC Address", "RSSI", "Rate", "Timestamp", "Signal_Length", 
            "RX_State", "Channel", "Secondary_Channel", "BB_Format", "Single_MPDU",
            "Noise_Floor", "RX_End_State", "Second", "RX_Estimate_Info_Valid",
            "RX_Estimate_Len", "HE_SIG_A1", "HE_SIG_A2", "HE_SIG_B_Len", "Is_Group",
            "RX_Match0", "RX_Match1", "RX_Match2", "RX_Match3", "CSI_Data",
            "Amplitudes", "Phases"
        ]
        writer.writerow(headers)
        
        # כתיבת שורות הנתונים
        for entry in data:
            writer.writerow([ 
                entry["seq"], entry["mac"], entry["rssi"], entry["rate"], entry["timestamp"],
                entry["signal_len"], entry["rx_state"], entry["channel"], entry["secondary_channel"],
                entry["bb_format"], entry["single_mpdu"], entry["noise_floor"], entry["rx_end_state"],
                entry["second"], entry["rx_estimate_info_valid"], entry["rx_estimate_len"],
                entry["he_siga1"], entry["he_siga2"], entry["he_sigb_len"], entry["is_group"],
                entry["rxmatch0"], entry["rxmatch1"], entry["rxmatch2"], entry["rxmatch3"],
                str(entry["csi_data"]),
                str(entry["amplitudes"]),
                str(entry["phases"])
            ])


# הוספת השהיה של 10 שניות לפני הריצה
print("Waiting for 10 seconds before starting...")
time.sleep(10)  # השהיה של 10 שניות

# קריאה ועיבוד הנתונים מה-Serial
parsed_data = read_csi_data_from_serial(PORT, BAUD_RATE, TIMEOUT)

# שמירה לקובץ CSV
save_to_csv(parsed_data, output_csv)

print(f"Data has been saved to {output_csv}")
