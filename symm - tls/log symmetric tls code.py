import csv
from datetime import datetime

# Sample data: Replace with your own data if needed
timestamps = [
    ("14-07-2025 15:02", "14-07-2025 15:04"),
    ("14-07-2025 16:38", "14-07-2025 16:39"),
    ("14-07-2025 16:43", "14-07-2025 16:43"),
    ("14-07-2025 16:45", "14-07-2025 16:46"),
    ("16-07-2025 10:07", "16-07-2025 10:08"),
    ("16-07-2025 10:09", "16-07-2025 10:09"),
    ("16-07-2025 10:10", "16-07-2025 10:10"),
    ("16-07-2025 10:11", "16-07-2025 10:11"),
    ("16-07-2025 10:12", "16-07-2025 10:12"),
    ("16-07-2025 10:13", "16-07-2025 10:13")
]

# Output file
output_csv = "log_symm_tls.xlsx"

# Format
time_format = "%d-%m-%Y %H:%M"

# Process and write to CSV
with open(output_csv, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Start Time", "End Time", "Duration (ms)"])
    
    for start, end in timestamps:
        if not start or not end:
            continue  # Skip incomplete rows
        
        try:
            start_dt = datetime.strptime(start, time_format)
            end_dt = datetime.strptime(end, time_format)
            duration_ms = int((end_dt - start_dt).total_seconds() * 1000)
            writer.writerow([start, end, duration_ms])
        except Exception as e:
            print(f"Error parsing: {start} - {end} | {e}")

print(f"✅ Data exported to {output_csv}")
print(f"CSV saved to: {output_csv}")
