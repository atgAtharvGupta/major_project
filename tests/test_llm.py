import pytest
from unittest.mock import patch
from src.llm import extract_entities, generate_search_queries, generate_summary_report, is_finance_related

@patch("src.llm.call_groq")
def test_is_finance_related_true(mock_call):
    mock_call.return_value = "YES"
    assert is_finance_related("How is TSLA doing?") == True

@patch("src.llm.call_groq")
def test_is_finance_related_false(mock_call):
    mock_call.return_value = "NO"
    assert is_finance_related("What is the recipe for cake?") == False

@patch("src.llm.call_groq")
def test_extract_entities_valid_json(mock_call):
    mock_call.return_value = '```json\n{"entities": [{"name": "Apple"}], "relationships": []}\n```'
    data = extract_entities("some text")
    assert len(data["entities"]) == 1
    assert data["entities"][0]["name"] == "Apple"

@patch("src.llm.call_groq")
def test_generate_search_queries(mock_call):
    mock_call.return_value = '["nifty 50 today", "sensex crash"]'
    queries = generate_search_queries("indian market status")
    assert isinstance(queries, list)
    assert len(queries) == 2


@patch("src.llm.call_groq")
def test_generate_search_queries_fallback(mock_call):
    mock_call.return_value = "not-json"
    queries = generate_search_queries("banking outlook")
    assert len(queries) >= 1


@patch("src.llm.call_groq")
def test_generate_summary_report_fallback(mock_call):
    mock_call.return_value = ""
    report = generate_summary_report("graph context", "query")
    assert "Executive Summary" in report
