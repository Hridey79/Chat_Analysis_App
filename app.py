# from distutils.command.upload import upload
import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt

st.sidebar.title("Chat-Analyzer")

uploaded_file=st.sidebar.file_uploader('Choose a File')
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocessor.preprocess(data)
    # st.dataframe(df)
    
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    
    selected_user=st.sidebar.selectbox('Show analysis wrt ',user_list)
    if st.sidebar.button("Show Analysis"):
        st.title('Top Statistics')
        col1,col2,col3=st.columns(3);
        
        total_messages,total_words,num_media_msg=helper.fetch_stats(selected_user,df)
        with col1:
            st.header("Total Messages")
            st.title(total_messages)
        
        with col2:
            st.header("Total Words")
            st.title(total_words)
        
        with col3:
            st.header("Media shared")
            st.title(num_media_msg)
        
        # with col4:
        #     st.header("Links shared")
        #     st.title(total_links)
        
        st.title('Monthly Timeline')
        timeline=helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.bar(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        st.title('Daily Timeline')
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['day'],daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
            
        if selected_user=='Overall':
            st.title("Most Busy Users")
            col1,col2=st.columns(2)
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(new_df)
                
        df_wc=helper.create_wc(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.title("Wordcloud")
        st.pyplot(fig)
        
        st.title("Most Common Words")
        most_common_words=helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_common_words[0], most_common_words[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        st.title('Most Used Emojis')
        emoji_df=helper.emoji_counter(selected_user,df)
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
            
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)