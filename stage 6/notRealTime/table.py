import serial
import csv

# הגדרות חיבור Serial
PORT = "COM10"  # עדכני לפורט שבו ה-ESP32 מחובר
BAUD_RATE = 115200  # קצב תואם ל-ESP32
TIMEOUT = 5  # זמן המתנה לקריאה מהחיבור

# קובץ פלט
output_csv = "csi_runs_output.csv"

# פונקציה לקריאת נתוני CSI מה-Serial
def read_csi_data_from_serial(port, baud_rate, timeout):
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    data = []  # רשימה שתכיל את כל הריצות
    current_csi = []  # רשימה לריצה הנוכחית
    csi_index = 1  # מונה ריצות

    try:
        print("Reading data from Serial... Press Ctrl+C to stop.")
        while True:
            line = ser.readline().decode("utf-8").strip()
            
            if line.startswith("Subcarrier"):
                try:
                    # דוגמה לפורמט: "Subcarrier 1: Amplitude = 23.345236, Phase = 0.172191"
                    parts = line.split(":")
                    subcarrier_info = parts[0].split(" ")[1]
                    amplitude_phase = parts[1].split(",")
                    
                    subcarrier = int(subcarrier_info.strip())
                    amplitude = float(amplitude_phase[0].split("=")[1].strip())
                    phase = float(amplitude_phase[1].split("=")[1].strip())
                    
                    current_csi.append((subcarrier, amplitude, phase))
                except (ValueError, IndexError) as e:
                    print(f"Error parsing line: {line} | {e}")

            elif "CSI_DATA-" in line:
                # שמירת הריצה הנוכחית אם יש נתונים
                if current_csi:
                    data.append((csi_index, current_csi))
                    csi_index += 1
                    current_csi = []  # איפוס לריצה הבאה
                print(f"Starting new CSI group: {csi_index}")
    except KeyboardInterrupt:
        # שמירת הריצה האחרונה אם יש נתונים
        if current_csi:
            data.append((csi_index, current_csi))
        print("Stopped reading from Serial.")
    finally:
        ser.close()
    return data

# פונקציה לשמירת הנתונים בקובץ CSV
def save_to_csv(data, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        for csi_index, csi_data in data:
            # כותרת עבור כל ריצה
            writer.writerow([f"CSI Index: {csi_index}"])
            writer.writerow(["Subcarrier", "Amplitude", "Phase"])
            for entry in csi_data:
                writer.writerow(entry)
            # שורה ריקה להפרדה
            writer.writerow([])
    print(f"Data saved to {output_file}")

# קריאה ועיבוד הנתונים מה-Serial
parsed_data = read_csi_data_from_serial(PORT, BAUD_RATE, TIMEOUT)

# שמירה לקובץ CSV
if parsed_data:
    save_to_csv(parsed_data, output_csv)
else:
        print("No data read from Serial.")