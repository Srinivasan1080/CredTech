import streamlit as st
import yfinance as yf
import pandas as pandas

st.set_page_config(page_title="Explainable Credit Scorecard", layout="wide")
st.title("Explainable Credit Scorecard (MVP)")

st.info("If you can see this message, your environment and Streamlit setup are working ✅")

# Temporary UI elements
company = st.selectbox("Pick a company (ticker)", ["AAPL", "MSFT", "TSLA"])
st.write(f"You selected: {company}")
ticker = yf.Ticker(company)
hist = ticker.history(period="1mo")  
if len(hist) >= 5:
    last_price = hist['Close'][-1]
    week_ago_price = hist['Close'][-5]
    week_change = ((last_price - week_ago_price) / week_ago_price) * 100
else:
    last_price = None
    week_change = 0


col1, col2 = st.columns(2)
with col1:
    st.metric("Last Price (USD)", f"{last_price:.2f}" if last_price else "N/A")
with col2:
    st.metric("1-week Change", f"{week_change:.2f}%")

st.caption("Next step: we'll connect real stock data here.")
# --- Simple scoring engine ---
score = 70  # start with a base score

# Rule 1: penalize large negative weekly change
if week_change < -5:
    score -= 10
elif week_change > 5:
    score += 5

# Rule 2: penalize very low stock price (optional simple risk signal)
if last_price and last_price < 50:
    score -= 10

# Keep score within 0–100 range
score = max(0, min(100, score))
st.subheader("Credit Score")
st.metric("Score (0-100)", score)
st.subheader("Stock Price Trend (Last 1 Month)")
st.line_chart(hist['Close'])
# Placeholder for sentiment score (to be added by teammate)
sentiment_score = 0.0  # default
st.subheader("News Sentiment (placeholder)")
st.write("Sentiment Score:", sentiment_score)
# Placeholder for explanation text (to be added by teammate)
explanation = "Score is currently rule-based on stock data. News + events will be added here."
st.subheader("Explanation")
st.write(explanation)
# Calculate simple volatility (standard deviation of returns over last 7 days)
if len(hist) >= 7:
    daily_returns = hist['Close'].pct_change().dropna()
    volatility = daily_returns[-7:].std()
else:
    volatility = 0
st.metric("Volatility (7d)", f"{volatility:.3f}")