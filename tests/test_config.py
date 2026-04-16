from src.config import resolve_embedding_model


def test_resolve_embedding_model_aliases():
    assert resolve_embedding_model("bge-large") == "BAAI/bge-large-en-v1.5"
    assert resolve_embedding_model("bge-small-en") == "BAAI/bge-small-en-v1.5"


def test_resolve_embedding_model_passthrough():
    custom = "custom/model"
    assert resolve_embedding_model(custom) == custom
