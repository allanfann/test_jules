import os

# Adjust path to import from the parent directory
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tree_engine import (
    DecisionTreeEngine,
    InvalidAnswer,
    NotDecisionNode,
    TreeNotFound,
)


class TestDecisionTreeEngine(unittest.TestCase):
    # This test no longer uses a class-level setUp, as each test will
    # configure its own mocks for better isolation.

    @patch("tree_engine.get_firestore_db")
    def test_get_start_node_success(self, mock_get_db):
        """Test successfully getting the start node of a tree."""
        # 1. Setup Mocks
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        mock_tree_doc = MagicMock(exists=True, to_dict=lambda: {"root_node_id": "root"})
        mock_root_node = MagicMock(
            id="root",
            exists=True,
            to_dict=lambda: {
                "type": "DECISION",
                "text": "Is this a test?",
                "children": [],
            },
        )

        # Configure the mock call chain
        mock_tree_ref = MagicMock(get=lambda: mock_tree_doc)
        mock_root_ref = MagicMock(get=lambda: mock_root_node)

        mock_nodes_collection = MagicMock(
            document=lambda doc_id: mock_root_ref
            if doc_id == "root"
            else MagicMock(get=MagicMock(exists=False))
        )
        mock_tree_ref.collection.return_value = mock_nodes_collection
        mock_db.collection.return_value.document.return_value = mock_tree_ref

        # 2. Call the code
        engine = DecisionTreeEngine()
        start_node = engine.get_start_node("test-tree")

        # 3. Assert
        self.assertEqual(start_node["id"], "root")
        self.assertEqual(start_node["type"], "DECISION")

    @patch("tree_engine.get_firestore_db")
    def test_get_start_node_tree_not_found(self, mock_get_db):
        """Test that TreeNotFound is raised for a non-existent tree."""
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        # Configure the mock to return a non-existent document
        mock_db.collection.return_value.document.return_value.get.return_value.exists = False

        engine = DecisionTreeEngine()
        with self.assertRaises(TreeNotFound):
            engine.get_start_node("unknown-tree")

    @patch("tree_engine.get_firestore_db")
    def test_get_next_node_success(self, mock_get_db):
        """Test successfully getting the next node."""
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

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

        mock_db.collection.return_value.document.return_value.collection.return_value.document.side_effect = nodes_side_effect

        engine = DecisionTreeEngine()
        next_node = engine.get_next_node("test-tree", "root", "Yes")

        self.assertEqual(next_node["id"], "outcome_yes")
        self.assertEqual(next_node["type"], "OUTCOME")

    @patch("tree_engine.get_firestore_db")
    def test_get_next_node_invalid_answer(self, mock_get_db):
        """Test that InvalidAnswer is raised for a wrong answer."""
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        mock_root_node = MagicMock(
            id="root",
            exists=True,
            to_dict=lambda: {
                "type": "DECISION",
                "text": "Is this a test?",
                "children": [{"answer_text": "Yes", "next_node_id": "outcome_yes"}],
            },
        )
        mock_db.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value = mock_root_node

        engine = DecisionTreeEngine()
        with self.assertRaises(InvalidAnswer):
            engine.get_next_node("test-tree", "root", "Maybe")

    @patch("tree_engine.get_firestore_db")
    def test_get_next_node_from_outcome_node(self, mock_get_db):
        """Test that NotDecisionNode is raised when traversing from an outcome."""
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db

        mock_outcome_node = MagicMock(
            id="outcome", exists=True, to_dict=lambda: {"type": "OUTCOME"}
        )
        mock_db.collection.return_value.document.return_value.collection.return_value.document.return_value.get.return_value = mock_outcome_node

        engine = DecisionTreeEngine()
        with self.assertRaises(NotDecisionNode):
            engine.get_next_node("test-tree", "outcome", "any answer")

    def test_engine_init_fails_if_db_not_available(self):
        """Test that the engine raises an error if Firebase is not initialized."""
        with patch("tree_engine.get_firestore_db", return_value=None):
            with self.assertRaises(ConnectionError):
                DecisionTreeEngine()


if __name__ == "__main__":
    unittest.main()
