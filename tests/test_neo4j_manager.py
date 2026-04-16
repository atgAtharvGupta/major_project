from unittest.mock import MagicMock, patch

from src.neo4j_manager import Neo4jManager


@patch.object(Neo4jManager, "_create_constraints")
@patch("src.neo4j_manager.GraphDatabase.driver")
def test_add_financial_data_returns_false_without_driver(_mock_driver, _mock_constraints):
    manager = Neo4jManager()
    manager.driver = None
    assert manager.add_financial_data({"entities": []}, "https://example.com") is False


@patch.object(Neo4jManager, "_create_constraints")
@patch("src.neo4j_manager.GraphDatabase.driver")
@patch("src.neo4j_manager.get_embedding")
def test_add_financial_data_normalizes_entities(mock_embedding, mock_driver, _mock_constraints):
    mock_embedding.return_value = [0.1, 0.2]
    session = MagicMock()
    driver = MagicMock()
    driver.session.return_value.__enter__.return_value = session
    mock_driver.return_value = driver
    manager = Neo4jManager()

    graph_data = {
        "entities": [{"name": " Reliance Industries ", "type": "Company", "description": "Energy conglomerate"}],
        "relationships": [],
    }
    assert manager.add_financial_data(graph_data, "https://moneycontrol.com/article", "title", "content") is True
    assert session.run.call_count >= 2


@patch.object(Neo4jManager, "_create_constraints")
@patch("src.neo4j_manager.GraphDatabase.driver")
def test_query_graph_formats_retrieval_results(_mock_driver, _mock_constraints):
    manager = Neo4jManager()
    manager.retrieve_relevant_subgraph = MagicMock(return_value=[
        {
            "source_name": "Reliance Industries",
            "source_type": "Company",
            "source_description": "Large Indian conglomerate",
            "target_name": "Oil And Gas",
            "relation_type": "OPERATES_IN",
            "relation_description": "Core business exposure",
        }
    ])
    context = manager.query_graph("Reliance sector outlook")
    assert "Reliance Industries" in context
    assert "OPERATES_IN" in context
