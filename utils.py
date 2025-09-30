import json
from datetime import datetime

def format_message(sender, message):
    data = {
        "sender": sender,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message
    }
    return json.dumps(data)

def validate_message(raw_msg):
    try:
        data = json.loads(raw_msg)
        return "message" in data
    except:
        return False
