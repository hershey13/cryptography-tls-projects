import sys
from collections import Counter, defaultdict
from datetime import datetime
import re

def parse_log_line(line):
    """
    Parses a single Flask log line.
    Example line:
    2025-07-15 18:35:59,733 [INFO] 127.0.0.1 - - [15/Jul/2025 18:35:59] "GET / HTTP/1.1" 200 -
    """
    try:
        # Regex to extract main fields
        match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ \[.*?\] .*? \[(.*?)\] "(.*?) (.*?) HTTP.*?" (\d+)', line)
        if match:
            log_ts = match.group(1)
            method = match.group(3)
            endpoint = match.group(4)
            status = match.group(5)

            timestamp = datetime.strptime(log_ts, "%Y-%m-%d %H:%M:%S")
            return timestamp, method, endpoint, status
    except Exception as e:
        print("⚠️ Error parsing line:", e)
        return None

def analyze(logfile):
    timestamps = []
    endpoints = []
    status_codes = []
    method_counts = Counter()

    with open(logfile, 'r') as f:
        for line in f:
            parsed = parse_log_line(line)
            if parsed:
                ts, method, endpoint, status = parsed
                timestamps.append(ts)
                endpoints.append(endpoint)
                status_codes.append(status)
                method_counts[method] += 1

    if not timestamps:
        print("No valid entries found in log.")
        return

    # === Basic Stats ===
    print(f"\n📦 Total requests: {len(timestamps)}")
    
    print("\n🌐 Request method breakdown:")
    for method, count in method_counts.items():
        print(f"  {method}: {count}")

    print("\n📁 Top 5 requested endpoints:")
    for ep, count in Counter(endpoints).most_common(5):
        print(f"  {ep}: {count} times")

    print("\n📊 Status code distribution:")
    for code, count in Counter(status_codes).items():
        print(f"  {code}: {count} times")

    # === Time Gap Analysis ===
    timestamps.sort()
    gaps = [(timestamps[i+1] - timestamps[i]).total_seconds() for i in range(len(timestamps)-1)]

    if gaps:
        print(f"\n⏱️ Time gap between requests:")
        print(f"  Average gap: {sum(gaps)/len(gaps):.2f} seconds")
        print(f"  Max gap:     {max(gaps):.2f} seconds")
        print(f"  Min gap:     {min(gaps):.2f} seconds")

    # === Optional: Most active hour ===
    hour_counts = defaultdict(int)
    for ts in timestamps:
        hour_counts[ts.strftime("%Y-%m-%d %H:00")] += 1

    print("\n⏰ Most active hours:")
    for hour, count in sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
        print(f"  {hour}: {count} requests")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_logs.py <log_file_path>")
    else:
        log_path = sys.argv[1]
        analyze(log_path)
