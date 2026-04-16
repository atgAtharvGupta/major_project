import pandas as pd
from unittest.mock import patch

from src.market_data import get_monthly_summary, get_yearly_summary, search_ticker

def test_search_ticker_mapping():
    assert search_ticker("reliance industries") == "RELIANCE.NS"
    assert search_ticker("apple stock") == "AAPL"

def test_search_ticker_fallback():
    assert search_ticker("buy TSLA today") == "TSLA"
    assert search_ticker("random words") == ""


@patch("src.market_data.get_ticker_data")
def test_get_monthly_summary(mock_get_ticker_data):
    index = pd.date_range("2024-01-01", periods=60, freq="D")
    mock_get_ticker_data.return_value = pd.DataFrame({"Close": range(60)}, index=index)
    summary = get_monthly_summary("RELIANCE.NS")
    assert "latest_close" in summary


@patch("src.market_data.get_ticker_data")
def test_get_yearly_summary(mock_get_ticker_data):
    index = pd.date_range("2020-01-01", periods=800, freq="D")
    mock_get_ticker_data.return_value = pd.DataFrame({"Close": range(800)}, index=index)
    summary = get_yearly_summary("RELIANCE.NS")
    assert "1y_return" in summary
