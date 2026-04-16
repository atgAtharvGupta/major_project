from unittest.mock import patch

from src.embeddings import compute_similarity, get_embedding


@patch("src.embeddings.get_model")
def test_get_embedding_empty_model(mock_get_model):
    mock_get_model.return_value = False
    assert get_embedding("hello") == []


@patch("src.embeddings.get_embedding")
def test_compute_similarity(mock_get_embedding):
    mock_get_embedding.side_effect = [[1.0, 0.0], [1.0, 0.0]]
    assert compute_similarity("a", "b") == 1.0
