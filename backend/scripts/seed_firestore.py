import argparse
import os
import sys

import firebase_admin
from firebase_admin import credentials, firestore

# --- Path setup to import from the project root ---
# The project root is two levels up from the script's location (backend/scripts)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


# --- Import and adapt the data from the example file ---
try:
    from example.example_decision_trees import TREES_DATA as trees_list

    # The script expects a dictionary of trees, keyed by tree_id. We convert our list.
    TREES_DATA = {tree["tree_id"]: tree for tree in trees_list}
    print("Successfully loaded 5 example trees from example/example_decision_trees.py")
except ImportError:
    print(
        "Error: Could not import TREES_DATA from example/example_decision_trees.py",
        file=sys.stderr,
    )
    print(
        "Please ensure the file exists and the project is run from its root directory.",
        file=sys.stderr,
    )
    sys.exit(1)


def initialize_and_get_db():
    """
    Initializes the Firebase Admin SDK for this script and returns a Firestore client.
    """
    if firebase_admin._apps:
        return firestore.client()

    try:
        # The credentials file is in the `backend` directory.
        backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        credentials_path = os.path.join(backend_root, "firebase-credentials.json")

        if not os.path.exists(credentials_path):
            print(
                f"ERROR: Firebase credentials file not found at '{credentials_path}'.",
                file=sys.stderr,
            )
            return None

        cred = credentials.Certificate(credentials_path)
        firebase_admin.initialize_app(cred)
        print("Firebase initialized for seeding script.")
        return firestore.client()
    except Exception as e:
        print(f"Error initializing Firebase for seeding: {e}", file=sys.stderr)
        return None


def delete_collection(coll_ref, batch_size):
    """Recursively delete a collection and its subcollections."""
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0
    for doc in docs:
        # Recursively delete subcollections
        for sub_coll_ref in doc.reference.collections():
            delete_collection(sub_coll_ref, batch_size)
        doc.reference.delete()
        deleted += 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)


def seed_firestore(db: firestore.Client, overwrite: bool = False):
    """
    Populates Firestore with the 5 example decision trees.
    """
    if not db:
        print("Firestore is not available. Aborting script.", file=sys.stderr)
        print(
            "Please ensure your `firebase-credentials.json` is set up correctly.",
            file=sys.stderr,
        )
        return

    for tree_id, tree_data in TREES_DATA.items():
        print(f"\nProcessing tree: '{tree_id}'...")
        tree_doc_ref = db.collection("decision_trees").document(tree_id)

        if tree_doc_ref.get().exists:
            if overwrite:
                print(f"  - Tree '{tree_id}' exists. Deleting nodes before writing...")
                nodes_collection_ref = tree_doc_ref.collection("nodes")
                delete_collection(nodes_collection_ref, 50)
            else:
                print(
                    f"  - Tree '{tree_id}' already exists. Use --overwrite to replace it."
                )
                continue

        tree_doc_data = {k: v for k, v in tree_data.items() if k != "nodes"}
        tree_doc_ref.set(tree_doc_data)
        print(f"  - Created document for tree '{tree_id}'.")

        nodes_collection_ref = tree_doc_ref.collection("nodes")
        if "nodes" in tree_data and isinstance(tree_data["nodes"], dict):
            for node_id, node_data in tree_data["nodes"].items():
                nodes_collection_ref.document(node_id).set(node_data)
                print(f"    - Created node '{node_id}'")
        else:
            print(f"  - Warning: No 'nodes' dictionary found for tree '{tree_id}'.")

    print("\nFirestore seeding process complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Seed Firestore database with example decision trees."
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="If set, existing trees with the same ID will be deleted and recreated.",
    )
    args = parser.parse_args()

    print(
        "This script will populate your Firestore database with data from example_decision_trees.py."
    )
    print(
        "--------------------------------------------------------------------------------"
    )
    if args.overwrite:
        print("Overwrite flag is set. Existing data will be replaced.")

    db_client = initialize_and_get_db()
    if db_client:
        seed_firestore(db_client, overwrite=args.overwrite)
    else:
        print("Could not initialize database. Aborting.", file=sys.stderr)
        sys.exit(1)
