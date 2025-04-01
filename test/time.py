from datetime import datetime
import time

def get_time():
    now = datetime.now()
    return [now.hour, now.minute, now.second]

print(time.time())