import pytest
from unittest.mock import patch, MagicMock
from core import process_query

@patch("core.is_finance_related")
def test_process_query_non_finance(mock_is_finance):
    mock_is_finance.return_value = False
    res = process_query("tell me a joke")
    assert res["error"] is not None
    assert "finance-related" in res["error"]

@patch("core.is_finance_related")
@patch("core.generate_search_queries")
@patch("core.search_and_extract")
@patch("core.neo4j_manager")
@patch("core.generate_summary_report")
@patch("core.search_ticker")
def test_process_query_success(mock_ticker, mock_report, mock_neo, mock_search, mock_gen_q, mock_finance):
    mock_finance.return_value = True
    mock_gen_q.return_value = ["q1"]
    mock_search.return_value = [{"url": "http://x.com", "graph_data": {"entities": [{"name": "A"}]}}]
    mock_neo.query_graph.return_value = "context"
    mock_neo.retrieve_relevant_subgraph.return_value = [{"source_name": "A", "score": 1.0}]
    mock_neo.add_financial_data.return_value = True
    mock_report.return_value = "report"
    mock_ticker.return_value = ""
    
    res = process_query("finance question")
    assert res["error"] is None
    assert res["report"] == "report"
    assert "http://x.com" in res["sources"]
    assert res["graph_updated"] == True
    assert res["graph_results"][0]["source_name"] == "A"
