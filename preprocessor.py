# import numpy as np
import pandas as pd
import re

def datetime_conv(x):
    x=x.split(",")
    date=x[0]
    time=x[1].strip()
    time=time.split(' ')[0]
    return date,time

def preprocess(data):
    pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    months={'1':'January',
        "2":'February',
        "3":'March',
        "4":"April",
        "5":"May",
        "6":"June",
        "7":"July",
        "8":'August',
        "9":"September",
        "10":'October',
        "11":"November",
        "12":"December"}
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'user_messages': messages,'message_date': dates})
    
    date=[]
    time=[]
    arr=df['message_date'].apply(lambda x:datetime_conv(x))
    for i in arr:
        date.append(i[0])
        time.append(i[1])
    df['date']=date
    df['time']=time
    df.drop('message_date',axis=1,inplace=True)
    
    users=[]
    messages=[]

    for x in df['user_messages']:
        entry=re.split('([\w\W]+?):\s',x)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user']=users
    df['message']=messages
    df.drop('user_messages',axis=1,inplace=True)
    
    day=[]
    month=[]
    year=[]
    for x in df["date"]:
        x=x.split('/')
        day.append(x[1])
        month.append(x[0])
        year.append(x[2])
    df['day']=day
    df['month']=month
    df['year']=year
    df.replace({"month":months},inplace=True)
    
    hour=[]
    minute=[]
    for x in df["time"]:
        x=x.split(":")
        hour.append(x[0])
        minute.append(x[1])
    df["hour"]=hour
    df['minute']=minute
    df.drop({'time'},axis=1,inplace=True)
    date_num=[]
    for x in df['date']:
        x=x.split('/')
        date_num.append(x[1])
    
    df['month_num']=date_num
    
    return df