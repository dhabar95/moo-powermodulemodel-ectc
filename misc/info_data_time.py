import datetime

def info_date_time():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%m-%d %H:%M:%S")
    
    message = f"[INFO {formatted_datetime}]"
    
    return message
