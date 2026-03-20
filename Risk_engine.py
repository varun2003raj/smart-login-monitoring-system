
known_ips = set()

def check_new_ip(ip):
    global known_ips

    if ip == "local" or ip == "unknown":
        return False

    if ip not in known_ips:
        known_ips.add(ip)
        return True

    return False


def classify_login(ip, failed_count, unusual_time):
    if ip == "local" or ip == "unknown":
        if failed_count >= 3 or unusual_time:
            return "Suspicious"
        return "Normal"

    if ip not in known_ips:
        known_ips.add(ip)
        return "Suspicious"

    if failed_count >= 3:
        return "Suspicious"

    if unusual_time:
        return "Suspicious"

    return "Normal"


def assign_risk(ip, failed_count, unusual_time, threshold):
    if failed_count >= threshold:
        return "High"

    if ip == "local" or ip == "unknown":
        if failed_count == 0 and not unusual_time:
            return "Low"
        elif failed_count < 3 or unusual_time:
            return "Medium"
        else:
            return "High"

    if ip not in known_ips:
        return "Medium"

    if failed_count == 0 and not unusual_time:
        return "Low"

    if failed_count < 3 or unusual_time:
        return "Medium"

    return "High"
                 
