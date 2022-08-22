# from urlextract import URLExtract
# extract=URLExtract()
import pandas as pd
# import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import emoji

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
        
    words=[]
    for message in df['message']:
        words.extend(message.split())
    total_words=len(words)
    
    total__messages=df.shape[0] 
    
    num_media_msg=df[df['message']=='<Media omitted>\n'].shape[0] 
    
    # links= []
    # for message in df['message']:
    #     extractor=URLExtract()
    #     urls=extractor.find_urls(message)
    #     links.extend(urls)
    # total__links=len(links)
    return total__messages,total_words,num_media_msg

def most_busy_users(df):
    x = df['user'].value_counts().head(10)
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df


def create_wc(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    
    f=open('stop_hinglish.txt',"r")
    stop_words=f.read()
    
    df=df[df['user']!='group_notification']
    df=df[df['message']!='<Media omitted>\n']
    
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df['message'] = df['message'].apply(remove_stop_words)
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc
    
def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    
    words=[]
    
    df=df[df['user']!='group_notification']
    df=df[df['message']!='<Media omitted>\n']
    
    f=open('stop_hinglish.txt',"r")
    stop_words=f.read()
    
    for message in df["message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    return pd.DataFrame(Counter(words).most_common(20))

def emoji_counter(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
        
    emojis =[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.distinct_emoji_list(message) ])
        
    return pd.DataFrame(Counter(emojis).most_common(100))

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
        
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-'+str(timeline['year'][i]))
        
    timeline['time']=time
    
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']==selected_user]
    daily_timeline=df.groupby('day').count()['message'].reset_index()
    
    return daily_timeline