from datetime import datetime

def get_time():
    now = datetime.now()
    return [now.hour, now.minute, now.second]

print(get_time())