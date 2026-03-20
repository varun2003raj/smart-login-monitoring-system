import platform

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

BRUTE_FORCE_THRESHOLD = 5
UNUSUAL_START = 0
UNUSUAL_END = 5

SYSTEM_OS = platform.system()

if SYSTEM_OS == "Windows":
    LOG_SOURCE = "windows"
else:
    LOG_SOURCE = "linux"

