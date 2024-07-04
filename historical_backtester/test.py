import yfinance as yf


def fetch_apple_stock_data():
    # Download 5 years of Apple stock data
    apple_data = yf.download("AAPL", start="2017-01-01", end="2022-01-01")
    # Save the data to a CSV file in the data folder
    apple_data.to_csv("data/AAPL_5_year_data.csv")


# Call the function to fetch and save the data
fetch_apple_stock_data()
