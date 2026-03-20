from telegram_alert import send_telegram
from log_reader import get_log_stream
from  risk_engine import classify_login, assign_risk
from config import BRUTE_FORCE_THRESHOLD, UNUSUAL_START, UNUSUAL_END, LOG_SOURCE

import subprocess
import re

failed_attempts = {}
brute_alert_sent = {}
history_file = "login_history.txt"
suspicious_file = "suspicious_logins.txt"

known_ips=set()


process = get_log_stream()

print(f"Monitoring login activity on {LOG_SOURCE}...\n")

def is_unusual_time(time_str):
    try:
        hour = int(time_str.split()[2].split(":")[0])
        return UNUSUAL_START <= hour < UNUSUAL_END
    except:
        return False


# save login

def save_login_history(message):
    with open(history_file, "a") as file:
        file.write(message + "\n")
        file.write("-" * 50 + "\n")

# save suspicious

def save_suspicious_event(message):
    with open(suspicious_file, "a") as file:
        file.write(message + "\n")
        file.write("=" * 50 + "\n")

for line in process.stdout:

    line_lower = line.lower()

    # extract time (first part of line)
    time = " ".join(line.split()[:3])

    # extract username
    user_match = re.search(r"user[= ](\w+)", line_lower)
    user = user_match.group(1) if user_match else "unknown"

    # extract IP
    ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
    ip = ip_match.group(1) if ip_match else "local"

    if ip == "local":
        login_type = "Local Login"
    else:
        login_type = "Remote Login"

    # failed login
    if "authentication failure" in line_lower:
        failed_attempts[ip] = failed_attempts.get(ip, 0) + 1
        attempts = failed_attempts[ip]

        if attempts >= BRUTE_FORCE_THRESHOLD:
            risk  = "High"

            if not brute_alert_sent.get(ip, False):
                brute_alert_sent[ip] = True

                message = f"""🚨 Brute Force Alert
    User: {user}
    IP: {ip}
    Type: {login_type}
    Attempts: {attempts}
    Time: {time}
    Risk: High
    Reason: Multiple failed login attempts detected"""

            print(message)
            send_telegram(message)
            save_login_history(message)
            save_suspicious_event(message)

        else:
            risk = "Medium"
            message = f"""❌ Failed Login
    User: {user}
    IP: {ip}
    Type: {login_type}
    Attempts: {attempts}
    Time: {time}
    Risk: {risk}"""
            print(message)
            send_telegram(message)
            save_login_history(message)

    # successful login
    if "session opened for user" in line_lower:
        unusual = is_unusual_time(time)
        failed_count = failed_attempts.get(ip, 0)
        status = classify_login(ip, failed_count, unusual)
        risk = assign_risk(ip, failed_count, unusual, BRUTE_FORCE_THRESHOLD)

        message = f"""✅ Successful Login
    User: {user}
    IP: {ip}
    Type: {login_type}
    Time: {time}
    Status: {status}
    Risk: {risk}"""

        print(message)
        send_telegram(message)
        save_login_history(message)

        if status == "Suspicious" and risk != "High":
            alert = f"""⚠️ Suspicious Login Alert
    User: {user}
    IP: {ip}
    Type: {login_type}
    Time: {time}
    Failed Attempts: {failed_count}
    Risk: {risk}
    Reason: New IP / unusual time / repeated failures"""
            print(alert)
            send_telegram(alert)
            save_login_history(alert)
            save_suspicious_event(alert)

        elif risk == "High":
            alert = f"""🚨 High Risk Login Alert
    User: {user}
    IP: {ip}
    Type: {login_type}
    Time: {time}
    Failed Attempts: {failed_count}
    Risk: {risk}
    Reason: Strong suspicious activity"""
            print(alert)
            send_telegram(alert)
            save_login_history(alert)
            save_suspicious_event(alert)

        failed_attempts[ip] = 0

