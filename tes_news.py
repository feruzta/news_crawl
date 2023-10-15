import streamlit as st
from newsapi import NewsApiClient
from textblob import TextBlob
import pandas as pd

# Initialize News API client
newsapi = NewsApiClient(api_key='242df6d63af745a09c6acfec7879c7e1')

# Streamlit app
def main():
    st.title("News Listening Tools 🐣")
    
    # Search query input
    query = st.text_input("Enter your search query:")
    
    # Date range input
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    
    # Search button
    if st.button("Search"):
        # Get news articles
        articles = search_news(query, start_date, end_date)
        
        # Display count of news articles
        st.write(f"Total news articles found: {len(articles)}")
        
        # Display news articles
        for article in articles:
            with st.expander(f"**Title:** {article['title']}"):
                st.write(f"**Description:** {article['description']}")
                st.write(f"**Source:** {article['source']['name']}")
                st.write(f"**Published At:** {article['publishedAt']}")
                st.write(f"**Source Link:** [{article['url']}]({article['url']})")
        
        # Sentiment analysis
        sentiment = analyze_sentiment(articles)
        st.write(f"**Sentiment Analysis:** {sentiment}")
        
        # Download button
        download_button(articles)

# Function to search for news articles
def search_news(query, start_date, end_date):
    response = newsapi.get_everything(q=query, language='en', sort_by='relevancy', from_param=start_date, to=end_date)
    articles = response['articles']
    return articles

# Function to perform sentiment analysis
def analyze_sentiment(articles):
    sentiment_scores = []
    for article in articles:
        text = article['title'] + ' ' + article['description']
        blob = TextBlob(text)
        sentiment_scores.append(blob.sentiment.polarity)
    
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    if avg_sentiment > 0:
        return "Positive"
    elif avg_sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

# Function to download the result
def download_button(articles):
    df = pd.DataFrame(articles, columns=['Title', 'Description', 'Source', 'Published At', 'Source Link'])
    df.to_excel("news_result.xlsx", index=False)
    st.download_button(
        label="Download Result",
        data="news_result.xlsx",
        file_name="news_result.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    main()
