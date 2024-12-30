import yfinance as yf
from app import create_app, db
from app.models import Company
from datetime import datetime

def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetch historical stock data for a given ticker.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    if data.empty:
        print(f"No data found for {ticker}.")
    return data

def update_company_data(ticker):
    """
    Fetch stock data and update the database for a specific company.
    """
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now().replace(year=datetime.now().year - 1)).strftime('%Y-%m-%d')
    data = fetch_stock_data(ticker, start_date, end_date)

    if data.empty:
        print(f"Skipping {ticker}: No data available.")
        return

    # Calculate performance metrics
    initial_price = data['Close'].iloc[0]
    latest_price = data['Close'].iloc[-1]
    percent_change = ((latest_price - initial_price) / initial_price) * 100

    # Update the company record
    company = Company.query.filter_by(ticker=ticker).first()
    if company:
        company.percent_change_1yr = percent_change
        company.last_updated = datetime.utcnow()
        db.session.commit()
        print(f"Updated {ticker}: {percent_change:.2f}% change.")

def update_all_companies():
    """
    Update stock data for all companies in the database.
    """
    companies = Company.query.all()
    for company in companies:
        try:
            print(f"Fetching data for {company.ticker}...")
            update_company_data(company.ticker)
        except Exception as e:
            print(f"Error updating {company.ticker}: {e}")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        update_all_companies()
        # Example: Fetch data for Apple (AAPL)
        '''
        ticker = "CRSP"
        print(f"Fetching data for {ticker}...")
        print(f"Percent change: {update_company_data(ticker):.2f}%")
        '''
#monk