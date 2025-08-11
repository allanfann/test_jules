import sys
import argparse
from firebase_setup import get_firestore_db

# --- Data for the 5 Example Decision Trees ---

TREES_DATA = {
    "get-married": {
        "name": "是否要與眼前的伴侶結婚",
        "description": "一個幫助評估結婚這項複雜決策的決策樹。",
        "root_node_id": "root",
        "nodes": {
            "root": {"type": "DECISION", "text": "核心價值觀契合嗎？", "children": [{"answer_text": "是", "next_node_id": "q_future"}, {"answer_text": "否", "next_node_id": "out_no"}]},
            "q_future": {"type": "DECISION", "text": "對未來規劃有共識嗎？", "children": [{"answer_text": "是", "next_node_id": "q_communication"}, {"answer_text": "否", "next_node_id": "out_wait"}]},
            "q_communication": {"type": "DECISION", "text": "溝通順暢且能解決衝突嗎？", "children": [{"answer_text": "是", "next_node_id": "out_yes"}, {"answer_text": "否", "next_node_id": "out_wait"}]},
            "out_no": {"type": "OUTCOME", "text": "不結婚"},
            "out_wait": {"type": "OUTCOME", "text": "再觀察"},
            "out_yes": {"type": "OUTCOME", "text": "結婚"}
        }
    },
    "buy-tsmc": {
        "name": "買的台積電股票是否正確",
        "description": "一個評估當下是否為買入台積電(TSMC)股票好時機的決策樹。",
        "root_node_id": "root",
        "nodes": {
            "root": {"type": "DECISION", "text": "有閒置資金嗎？", "children": [{"answer_text": "是", "next_node_id": "q_risk"}, {"answer_text": "否", "next_node_id": "out_dont_buy"}]},
            "q_risk": {"type": "DECISION", "text": "風險承受能力高？", "children": [{"answer_text": "是", "next_node_id": "q_fundamentals"}, {"answer_text": "否", "next_node_id": "out_dont_buy"}]},
            "q_fundamentals": {"type": "DECISION", "text": "公司基本面健康？", "children": [{"answer_text": "是", "next_node_id": "q_market"}, {"answer_text": "否", "next_node_id": "out_wait"}]},
            "q_market": {"type": "DECISION", "text": "市場趨勢向上？", "children": [{"answer_text": "是", "next_node_id": "out_buy"}, {"answer_text": "否", "next_node_id": "out_wait"}]},
            "out_dont_buy": {"type": "OUTCOME", "text": "不買"},
            "out_wait": {"type": "OUTCOME", "text": "觀望"},
            "out_buy": {"type": "OUTCOME", "text": "買入"}
        }
    },
    "change-jobs": {
        "name": "是否要換工作",
        "description": "一個評估換工作利弊的決策樹。",
        "root_node_id": "root",
        "nodes": {
            "root": {"type": "DECISION", "text": "已收到新Offer？", "children": [{"answer_text": "是", "next_node_id": "q_better"}, {"answer_text": "否", "next_node_id": "out_stay"}]},
            "q_better": {"type": "DECISION", "text": "新工作薪資更高或發展性更好？", "children": [{"answer_text": "是", "next_node_id": "q_dissatisfied"}, {"answer_text": "否", "next_node_id": "out_stay"}]},
            "q_dissatisfied": {"type": "DECISION", "text": "對現況不滿意？", "children": [{"answer_text": "是", "next_node_id": "out_change"}, {"answer_text": "否", "next_node_id": "out_decline"}]},
            "out_stay": {"type": "OUTCOME", "text": "留在原職"},
            "out_change": {"type": "OUTCOME", "text": "換工作"},
            "out_decline": {"type": "OUTCOME", "text": "婉拒Offer, 留原職"}
        }
    },
    "choose-major": {
        "name": "基於聯考要選哪個科系",
        "description": "一個協助考生根據分數、興趣和就業市場來選擇大學科系的決策樹。",
        "root_node_id": "root",
        "nodes": {
            "root": {"type": "DECISION", "text": "分數是否達標？", "children": [{"answer_text": "是", "next_node_id": "q_interest"}, {"answer_text": "否", "next_node_id": "out_other"}]},
            "q_interest": {"type": "DECISION", "text": "對該領域有興趣？", "children": [{"answer_text": "是", "next_node_id": "q_prospects"}, {"answer_text": "否", "next_node_id": "out_other"}]},
            "q_prospects": {"type": "DECISION", "text": "未來就業前景好？", "children": [{"answer_text": "是", "next_node_id": "out_choose"}, {"answer_text": "否", "next_node_id": "q_risk"}]},
            "q_risk": {"type": "DECISION", "text": "願意承擔風險？", "children": [{"answer_text": "是", "next_node_id": "out_choose"}, {"answer_text": "否", "next_node_id": "out_other"}]},
            "out_other": {"type": "OUTCOME", "text": "考慮其他科系"},
            "out_choose": {"type": "OUTCOME", "text": "選擇該科系"}
        }
    },
    "have-child": {
        "name": "該不該生小孩",
        "description": "一個從務實層面評估生小孩決策的決策樹。",
        "root_node_id": "root",
        "nodes": {
            "root": {"type": "DECISION", "text": "夫妻雙方都有共識？", "children": [{"answer_text": "是", "next_node_id": "q_finance"}, {"answer_text": "否", "next_node_id": "out_no"}]},
            "q_finance": {"type": "DECISION", "text": "經濟狀況能負擔？", "children": [{"answer_text": "是", "next_node_id": "q_support"}, {"answer_text": "否", "next_node_id": "out_wait"}]},
            "q_support": {"type": "DECISION", "text": "有後援系統支持？", "children": [{"answer_text": "是", "next_node_id": "out_yes"}, {"answer_text": "否", "next_node_id": "q_sacrifice"}]},
            "q_sacrifice": {"type": "DECISION", "text": "願意犧牲更多時間精力？", "children": [{"answer_text": "是", "next_node_id": "out_yes"}, {"answer_text": "否", "next_node_id": "out_wait"}]},
            "out_no": {"type": "OUTCOME", "text": "不生"},
            "out_wait": {"type": "OUTCOME", "text": "過幾年再說"},
            "out_yes": {"type": "OUTCOME", "text": "生"}
        }
    }
}

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

def seed_firestore(overwrite=False):
    """
    Populates Firestore with the 5 example decision trees.
    """
    db = get_firestore_db()
    if not db:
        print("Firestore is not available. Aborting script.", file=sys.stderr)
        print("Please ensure your `firebase-credentials.json` is set up correctly.", file=sys.stderr)
        return

    for tree_id, tree_data in TREES_DATA.items():
        print(f"\nProcessing tree: '{tree_id}'...")
        tree_doc_ref = db.collection("decision_trees").document(tree_id)

        if tree_doc_ref.get().exists:
            if overwrite:
                print(f"  - Tree '{tree_id}' exists. Deleting nodes before writing...")
                delete_collection(tree_doc_ref.collection("nodes"), 50)
            else:
                print(f"  - Tree '{tree_id}' already exists. Use --overwrite to replace it.")
                continue

        # Create the main tree document
        tree_doc_data = {k: v for k, v in tree_data.items() if k != "nodes"}
        tree_doc_ref.set(tree_doc_data)
        print(f"  - Created document for tree '{tree_id}'.")

        # Create the nodes in the sub-collection
        nodes_collection_ref = tree_doc_ref.collection("nodes")
        for node_id, node_data in tree_data["nodes"].items():
            nodes_collection_ref.document(node_id).set(node_data)
            print(f"    - Created node '{node_id}'")

    print("\nFirestore seeding process complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed Firestore database with example decision trees.")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="If set, existing trees with the same ID will be deleted and recreated."
    )
    args = parser.parse_args()

    print("This script will populate your Firestore database with 5 example decision trees.")
    print("--------------------------------------------------------------------------------")
    if args.overwrite:
        print("Overwrite flag is set. Existing data will be replaced.")

    seed_firestore(overwrite=args.overwrite)
