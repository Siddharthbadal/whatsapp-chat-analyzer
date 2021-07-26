import re
import pandas as pd

def preprocessor(data):

    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s" 
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_messages':messages,"message_date":dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format = "%d/%m/%Y, %H:%M - ")
    df.rename(columns={'message_date': "Date"}, inplace=True)

    users = []
    messages = []
    for message in df['user_messages']:
        txt = re.split("([\w\W]+?):\s", message)
        if txt[1:]:
            users.append(txt[1])
            messages.append(txt[2])
        else:
            users.append('group_notification')
            messages.append(txt[0])
    
    df['User'] = users
    df['Message'] = messages
    df.drop(columns=['user_messages'], inplace=True)

    df['Year'] = df['Date'].dt.year
    df['month_number'] = df['Date'].dt.month
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day
    df['Every_day']= df['Date'].dt.date
    df['DayName'] = df['Date'].dt.day_name()
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute

    return df


