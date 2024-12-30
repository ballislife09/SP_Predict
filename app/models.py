from app import db

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each company
    ticker = db.Column(db.String(10), nullable=False, unique=True)  # Stock ticker symbol
    name = db.Column(db.String(255), nullable=False)  # Company name
    sector = db.Column(db.String(100))  # Sector (e.g., Tech, Healthcare)
    market_cap = db.Column(db.Float)  # Market capitalization in billions
    last_updated = db.Column(db.DateTime, nullable=False)  # When data was last updated
    percent_change_1yr = db.Column(db.Float)

class TestTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
