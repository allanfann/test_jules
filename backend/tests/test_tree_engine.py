import pytest
from unittest.mock import MagicMock

from app.services.tree_engine import (
    DecisionTreeEngine,
    InvalidAnswer,
    NodeNotFound,
    NotDecisionNode,
    TreeNotFound,
)


@pytest.fixture
def mock_db():
    """A pytest fixture that provides a mock Firestore client."""
    return MagicMock()


@pytest.fixture
def tree_engine(mock_db):
    """A pytest fixture that provides an initialized DecisionTreeEngine with a mock DB."""
    return DecisionTreeEngine(db=mock_db)


# --- Test Cases ---


def test_get_start_node_success(tree_engine, mock_db):
    """Test successfully getting the start node of a tree."""
    # 1. Setup Mocks
    mock_tree_doc = MagicMock(exists=True, to_dict=lambda: {"root_node_id": "root"})
    mock_root_node_data = {
        "type": "DECISION",
        "text": "Is this a test?",
        "children": [],
    }
    mock_root_node = MagicMock(
        id="root", exists=True, to_dict=lambda: mock_root_node_data
    )

    # Configure the mock call chain
    mock_db.collection.return_value.document.return_value.get.return_value = (
        mock_tree_doc
    )
    mock_db.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value = (
        mock_root_node
    )

    # 2. Call the code
    start_node = tree_engine.get_start_node("test-tree")

    # 3. Assert
    assert start_node["id"] == "root"
    assert start_node["type"] == "DECISION"


def test_get_start_node_tree_not_found(tree_engine, mock_db):
    """Test that TreeNotFound is raised for a non-existent tree."""
    # Configure the mock to return a non-existent document
    mock_db.collection.return_value.document.return_value.get.return_value.exists = False

    with pytest.raises(TreeNotFound):
        tree_engine.get_start_node("unknown-tree")


def test_get_next_node_success(tree_engine, mock_db):
    """Test successfully getting the next node."""
    mock_root_node = MagicMock(
        id="root",
        exists=True,
        to_dict=lambda: {
            "type": "DECISION",
            "text": "Is this a test?",
            "children": [{"answer_text": "Yes", "next_node_id": "outcome_yes"}],
        },
    )
    mock_yes_node = MagicMock(
        id="outcome_yes",
        exists=True,
        to_dict=lambda: {"type": "OUTCOME", "text": "Success!"},
    )

    def nodes_side_effect(doc_id):
        if doc_id == "root":
            return MagicMock(get=lambda: mock_root_node)
        if doc_id == "outcome_yes":
            return MagicMock(get=lambda: mock_yes_node)
        return MagicMock(get=MagicMock(exists=False))

    mock_db.collection.return_value.document.return_value.collection.return_value.document.side_effect = (
        nodes_side_effect
    )

    next_node = tree_engine.get_next_node("test-tree", "root", "Yes")

    assert next_node["id"] == "outcome_yes"
    assert next_node["type"] == "OUTCOME"


def test_get_next_node_invalid_answer(tree_engine, mock_db):
    """Test that InvalidAnswer is raised for a wrong answer."""
    mock_root_node = MagicMock(
        id="root",
        exists=True,
        to_dict=lambda: {
            "type": "DECISION",
            "text": "Is this a test?",
            "children": [{"answer_text": "Yes", "next_node_id": "outcome_yes"}],
        },
    )
    mock_db.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value = (
        mock_root_node
    )

    with pytest.raises(InvalidAnswer):
        tree_engine.get_next_node("test-tree", "root", "Maybe")


def test_get_next_node_from_outcome_node(tree_engine, mock_db):
    """Test that NotDecisionNode is raised when traversing from an outcome."""
    mock_outcome_node = MagicMock(
        id="outcome", exists=True, to_dict=lambda: {"type": "OUTCOME"}
    )
    mock_db.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value = (
        mock_outcome_node
    )

    with pytest.raises(NotDecisionNode):
        tree_engine.get_next_node("test-tree", "outcome", "any answer")


def test_engine_init_fails_if_db_is_none():
    """Test that the engine raises an error if the DB client is None."""
    with pytest.raises(ConnectionError):
        DecisionTreeEngine(db=None)