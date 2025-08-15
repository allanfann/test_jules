from firebase_setup import get_firestore_db

# --- Custom Exceptions for the Engine ---

class TreeNotFound(Exception):
    """Raised when a decision tree with the given ID is not found."""
    pass

class NodeNotFound(Exception):
    """Raised when a node with the given ID is not found within a tree."""
    pass

class InvalidAnswer(Exception):
    """Raised when a provided answer is not a valid option for a decision node."""
    pass

class NotDecisionNode(Exception):
    """Raised when trying to get the next node from an outcome node."""
    pass


class DecisionTreeEngine:
    """
    A class to handle the logic of fetching and traversing decision trees
    stored in Firestore.
    """
    def __init__(self):
        """
        Initializes the engine and gets the Firestore database client.
        """
        self.db = get_firestore_db()
        if not self.db:
            raise ConnectionError("Firestore database is not initialized. Cannot create DecisionTreeEngine.")

    def get_start_node(self, tree_id: str) -> dict:
        """
        Fetches the root node of a specified decision tree.

        Args:
            tree_id: The ID of the decision tree.

        Returns:
            A dictionary containing the data of the root node.

        Raises:
            TreeNotFound: If the tree_id does not exist or is malformed.
            NodeNotFound: If the root node specified in the tree document does not exist.
        """
        tree_ref = self.db.collection("decision_trees").document(tree_id)
        tree_doc = tree_ref.get()

        if not tree_doc.exists:
            raise TreeNotFound(f"Decision tree with ID '{tree_id}' not found.")

        tree_data = tree_doc.to_dict()
        root_node_id = tree_data.get("root_node_id")

        if not root_node_id:
            raise TreeNotFound(f"Tree '{tree_id}' is malformed and does not have a 'root_node_id'.")

        return self.get_node_by_id(tree_id, root_node_id)

    def get_node_by_id(self, tree_id: str, node_id: str) -> dict:
        """
        Fetches a specific node by its ID from a given tree.

        Args:
            tree_id: The ID of the decision tree.
            node_id: The ID of the node to fetch.

        Returns:
            A dictionary containing the node's data.

        Raises:
            NodeNotFound: If the node is not found in the specified tree.
        """
        node_ref = self.db.collection("decision_trees").document(tree_id).collection("nodes").document(node_id)
        node_doc = node_ref.get()

        if not node_doc.exists:
            raise NodeNotFound(f"Node '{node_id}' not found for tree '{tree_id}'.")

        node_data = node_doc.to_dict()
        node_data['id'] = node_doc.id  # Add the node's ID to the dict for convenience
        return node_data

    def get_next_node(self, tree_id: str, current_node_id: str, answer: str) -> dict:
        """
        Determines the next node based on the user's answer to the current node.

        Args:
            tree_id: The ID of the decision tree.
            current_node_id: The ID of the current node.
            answer: The user's answer to the question at the current node.

        Returns:
            A dictionary containing the data of the next node.

        Raises:
            NotDecisionNode: If the current node is an OUTCOME node.
            InvalidAnswer: If the provided answer is not a valid choice.
            NodeNotFound: If the current node or the next node does not exist.
        """
        current_node_data = self.get_node_by_id(tree_id, current_node_id)

        if current_node_data.get("type") != "DECISION":
            raise NotDecisionNode("The current node is an outcome node and has no children.")

        children = current_node_data.get("children", [])
        next_node_id = None
        for child in children:
            if child.get("answer_text") == answer:
                next_node_id = child.get("next_node_id")
                break

        if not next_node_id:
            valid_answers = [child.get('answer_text') for child in children]
            raise InvalidAnswer(f"'{answer}' is not a valid answer for this node. Please choose from: {valid_answers}")

        return self.get_node_by_id(tree_id, next_node_id)
