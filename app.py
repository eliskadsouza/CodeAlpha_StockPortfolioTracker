import io
import pandas as pd
import streamlit as st

# Hardcoded Stock Prices Dictionary
STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "GOOGL": 140.00,
    "MSFT": 410.00,
    "AMZN": 175.00,
    "NVDA": 120.00,
}

# Streamlit Page Setup
st.set_page_config(
    page_title="Stock Portfolio Tracker", page_icon="📈", layout="centered"
)

st.title("📈 Stock Portfolio Tracker")
st.write("Track your total investment value and manage your stock portfolio.")

# Initialize Session State Portfolio
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Available Stock Prices")
    st.table(
        pd.DataFrame(
            list(STOCK_PRICES.items()), columns=["Stock Symbol", "Price ($)"]
        )
    )

    if st.button("🗑️️ Clear Entire Portfolio", use_container_width=True):
        st.session_state.portfolio = {}
        st.rerun()

# Add Stock Form
st.subheader("➕ Add Stocks to Portfolio")
col1, col2 = st.columns(2)

with col1:
    selected_stock = st.selectbox(
        "Select Stock Symbol:", list(STOCK_PRICES.keys())
    )

with col2:
    quantity = st.number_input(
        "Enter Quantity (Shares):", min_value=1, step=1, value=1
    )

if st.button("Add / Update Stock", use_container_width=True):
    if selected_stock in st.session_state.portfolio:
        st.session_state.portfolio[selected_stock] += quantity
    else:
        st.session_state.portfolio[selected_stock] = quantity
    st.success(f"Added {quantity} share(s) of {selected_stock}!")
    st.rerun()

st.markdown("---")

# Portfolio Summary & Metrics
if st.session_state.portfolio:
    st.subheader("📊 Portfolio Breakdown")

    portfolio_data = []
    total_value = 0.0

    for symbol, shares in st.session_state.portfolio.items():
        price = STOCK_PRICES[symbol]
        subtotal = shares * price
        total_value += subtotal
        portfolio_data.append(
            {
                "Stock Symbol": symbol,
                "Price per Share ($)": f"${price:.2f}",
                "Shares Owned": shares,
                "Total Value ($)": subtotal,
            }
        )

    df = pd.DataFrame(portfolio_data)

    # Display Metrics
    st.metric("Total Investment Value", f"${total_value:,.2f}")

    # Display Data Table
    st.dataframe(
        df[["Stock Symbol", "Price per Share ($)", "Shares Owned", "Total Value ($)"]],
        use_container_width=True,
    )

    # Bonus Visual Chart
    chart_df = pd.DataFrame(
        list(st.session_state.portfolio.items()), columns=["Stock", "Shares"]
    ).set_index("Stock")
    st.bar_chart(chart_df)

    # File Export Feature (CSV Export)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()

    st.download_button(
        label="📥 Download Portfolio Summary (.csv)",
        data=csv_data,
        file_name="portfolio_summary.csv",
        mime="text/csv",
        use_container_width=True,
    )
else:
    st.info("Your portfolio is currently empty. Add stocks above to get started!")