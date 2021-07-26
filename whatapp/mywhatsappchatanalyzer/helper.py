from urlextract import URLExtract
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
from collections import Counter
import emoji



extract = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != "All":
        df = df[df['User']== selected_user]

    # Total messages
    number_of_messages = df.shape[0]
    
    # Total words
    words = []
    for message in df['Message']:
        words.extend(message.split())


    #media
    number_of_media = df[df['Message'] == "<Media omitted>\n"].shape[0]

    #links
    urls = []
    for message in df['Message']:
        urls.extend(extract.find_urls(message))


    return number_of_messages, len(words),number_of_media, len(urls)


def top_five_users(df):
    # for graph
    topFive = df['User'].value_counts().head()
    df = round((df['User'].value_counts() / df.shape[0]) * 100,2).reset_index().rename(columns={'index': 'Name', 'User':'Chat-Percent'})


    return topFive, df


def create_wordcloud(selected_user, df):

    f = open('chats/hinglish.txt','r', encoding='utf-8')
    stop_words = f.read()

    if selected_user != 'All':
        df = df[df['User']  == selected_user]

    temp = df[df['User'] != 'group_notification']
    temp = temp[temp['Message'] != "<Media omitted>\n"]

    wc = WordCloud(
        width=500, 
        height=600,
        min_font_size = 12,
        background_color = 'white',
        stopwords=stop_words
        )
    wc_df = wc.generate(temp['Message'].str.cat(sep=" "))
    return wc_df


def most_common_words(selected_user, df):

    f = open('chats/hinglish.txt','r', encoding='utf-8')
    stop_words = f.read()

    if selected_user != 'All':
        df = df[df['User']  == selected_user]

    temp = df[df['User'] != 'group_notification']
    temp = temp[temp['Message'] != "<Media omitted>\n"]

    words = []
    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        

    common_words_df = pd.DataFrame(Counter(words).most_common(15))
    return common_words_df


def emoji_analysis(selected_user, df):

    if selected_user != 'All':
        df = df[df['User']  == selected_user]

    emojis_lst = []
    for message in df['Message']:
        emojis_lst.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df= pd.DataFrame(Counter(emojis_lst).most_common(len(Counter(emojis_lst))))

    if emoji_df.size== 0:
            return None

    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'All':
        df = df[df['User']  == selected_user]

    timeline = df.groupby(['Year','month_number', 'Month']).count()['Message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['Time'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'All':
        df = df[df['User']  == selected_user]

    daily_timeline = df.groupby('Every_day').count()['Message'].reset_index()
        
    return daily_timeline


def active_days_map(selected_user, df):
    if selected_user != 'All':
        df = df[df['User']  == selected_user]

    active_day = df['DayName'].value_counts()
    return active_day


def active_months_map(selected_user, df):
    if selected_user != 'All':
        df = df[df['User']  == selected_user]

    active_month = df['Month'].value_counts()
    return active_month