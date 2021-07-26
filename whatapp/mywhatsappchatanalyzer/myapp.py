import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt


st.sidebar.title("WhatsApp Chat Analyzer")

st.sidebar.subheader("Only 24 hour time format")
st.sidebar.text("If no data, Output will show nothing!")


uploaded_file = st.sidebar.file_uploader("Upload a File")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # bytes data to utf8 to read it in app
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocessor(data)

    
    # finding unique users
    user_list = df['User'].unique().tolist()
    try:
        user_list.remove('group_notification')
    except:
        pass
    user_list.sort()
    user_list.insert(0, "All")

    selected_user = st.sidebar.selectbox("View Analysis for ", user_list)
    

    if st.sidebar.button("View Analysis"):

        number_of_messages, words, number_of_media, urls = helper.fetch_stats(selected_user, df)


        st.title("Chat Statistics")
        # statistics

        col1, col2, col3, col4 = st.beta_columns(4)

        with col1:
            st.header("Total Messages")
            st.title(number_of_messages)

        with col2:
            st.header("Total Words ")
            st.title(words)

        with col3:
            st.header("Total Media")
            st.title(number_of_media)

        with col4:
            st.header("Total URLs")
            st.title(urls)

        # monthly timeline of the chat
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['Time'], timeline['Message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Day Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['Every_day'], daily_timeline['Message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Most active days Map
        col1, col2 = st.beta_columns(2)

        with col1:
            st.header("Most Active Days")
            active_days = helper.active_days_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(active_days.index, active_days.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Active Months")
            active_months = helper.active_months_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(active_months.index, active_months.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)




        # most busy users
        if selected_user == "All":
            
            topFive, top_five_df = helper.top_five_users(df)
            

            fig, ax = plt.subplots()

            col1, col2 = st.beta_columns(2)

            with col1:
                st.title("Top Five Active users")
                ax.bar(topFive.index, topFive.values, color="blue")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.title("Chat Count")
                st.dataframe(topFive[0:5])
                

        #wordcloud
        st.title("WordCloud")
        wc_df = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc_df)
        st.pyplot(fig)



        # most common words
        st.title('Most Common Words')
        col1, col2 = st.beta_columns(2)

        with col1:
            most_commnon_words_df = helper.most_common_words(selected_user, df)
            st.dataframe(most_commnon_words_df) 

        with col2:
            fig, ax = plt.subplots()
            ax.barh(most_commnon_words_df[0], most_commnon_words_df[1])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # emoji analysis
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_analysis(selected_user, df)

        if emoji_df is None:
            print("No emojies")
        else:
            col1, col2 = st.beta_columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(10), labels=emoji_df[0].head(10), autopct="%0.2f")
                st.pyplot(fig)


        
