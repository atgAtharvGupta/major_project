from unittest.mock import patch, MagicMock
from src.search import fetch_article_content, search_and_extract, search_financial_news

@patch("src.search.requests.get")
def test_search_financial_news(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": [{"title": "Test", "link": "http://moneycontrol.com/test"}]}
    mock_get.return_value = mock_response
    
    res = search_financial_news("test")
    assert len(res) == 1
    assert res[0]["title"] == "Test"

@patch("src.search.requests.get")
def test_search_financial_news_fail(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response
    
    res = search_financial_news("test")
    assert res == []


@patch("src.search.requests.get")
def test_fetch_article_content_filters_domains(mock_get):
    assert fetch_article_content("https://example.com/article") == ""
    mock_get.assert_not_called()


@patch("src.search.extract_entities")
@patch("src.search.fetch_article_content")
@patch("src.search.search_financial_news")
def test_search_and_extract(mock_search_news, mock_fetch_article_content, mock_extract_entities):
    mock_search_news.return_value = [{"title": "Test", "link": "http://moneycontrol.com/test"}]
    mock_fetch_article_content.return_value = "a" * 500
    mock_extract_entities.return_value = {"entities": [{"name": "Apple"}], "relationships": []}
    result = search_and_extract("apple outlook")
    assert result[0]["graph_data"]["entities"][0]["name"] == "Apple"
