import argparse
import os
import sys

import firebase_admin
from firebase_admin import credentials, firestore

# --- Path setup to import from the project root ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- Personalities Data ---
PERSONALITIES_DATA = {
    "optimist": {"keywords": ["happy", "good", "success", "love", "great", "joy", "beautiful", "wonderful", "開心", "好", "成功", "愛", "棒", "喜歡"]},
    "pessimist": {"keywords": ["sad", "bad", "failure", "hate", "terrible", "pain", "awful", "傷心", "不好", "失敗", "討厭", "糟", "痛苦"]},
    "analyst": {"keywords": ["think", "because", "data", "number", "analyze", "reason", "logic", "思考", "因為", "數據", "分析", "邏輯"]},
    "realist": {"keywords": ["practical", "realistic", "grounded", "sensible", "pragmatic", "實際", "現實", "腳踏實地", "明智", "務實"]},
    "idealist": {"keywords": ["dream", "vision", "hope", "ideal", "utopia", "夢想", "願景", "希望", "理想", "烏托邦"]},
    "leader": {"keywords": ["lead", "guide", "direct", "command", "motivate", "領導", "指導", "指揮", "命令", "激勵"]},
    "follower": {"keywords": ["follow", "support", "assist", "obey", "comply", "跟隨", "支持", "協助", "服從", "遵守"]},
    "innovator": {"keywords": ["create", "invent", "new", "original", "pioneer", "創造", "發明", "新的", "原創", "先驅"]},
    "traditionalist": {"keywords": ["tradition", "custom", "heritage", "conservative", "conventional", "傳統", "習俗", "遺產", "保守", "常規"]},
    "adventurer": {"keywords": ["explore", "discover", "risk", "thrill", "journey", "探索", "發現", "風險", "刺激", "旅程"]},
    "nurturer": {"keywords": ["care", "protect", "help", "support", "empathy", "關心", "保護", "幫助", "支持", "同理心"]},
    "scholar": {"keywords": ["study", "learn", "research", "knowledge", "academic", "學習", "研究", "知識", "學術"]},
    "artist": {"keywords": ["art", "creative", "design", "beauty", "expression", "藝術", "創意", "設計", "美", "表達"]},
    "entertainer": {"keywords": ["fun", "joke", "perform", "amuse", "entertain", "有趣", "笑話", "表演", "娛樂"]},
    "guardian": {"keywords": ["protect", "defend", "secure", "watchful", "vigilant", "保護", "防禦", "安全", "警惕", "警覺"]},
    "rebel": {"keywords": ["defy", "resist", "challenge", "question", "break", "反抗", "抵抗", "挑戰", "質疑", "打破"]},
    "peacemaker": {"keywords": ["peace", "harmony", "calm", "resolve", "mediate", "和平", "和諧", "冷靜", "解決", "調解"]},
    "strategist": {"keywords": ["plan", "tactic", "maneuver", "foresight", "scheme", "計劃", "戰術", "策略", "遠見", "計謀"]},
    "mentor": {"keywords": ["guide", "teach", "advise", "counsel", "coach", "指導", "教導", "建議", "諮詢", "教練"]},
    "explorer": {"keywords": ["discover", "investigate", "search", "seek", "wander", "發現", "調查", "搜索", "尋找", "漫遊"]},
}

def initialize_and_get_db():
    """
    Initializes the Firebase Admin SDK for this script and returns a Firestore client.
    """
    if firebase_admin._apps:
        return firestore.client()

    try:
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

def seed_personalities(db: firestore.Client, overwrite: bool = False):
    """
    Populates Firestore with the personalities data.
    """
    if not db:
        print("Firestore is not available. Aborting script.", file=sys.stderr)
        print(
            "Please ensure your `firebase-credentials.json` is set up correctly.",
            file=sys.stderr,
        )
        return

    for personality_id, personality_data in PERSONALITIES_DATA.items():
        print(f"\nProcessing personality: '{personality_id}'...")
        personality_doc_ref = db.collection("personalities").document(personality_id)

        if personality_doc_ref.get().exists and not overwrite:
            print(
                f"  - Personality '{personality_id}' already exists. Use --overwrite to replace it."
            )
            continue

        personality_doc_ref.set(personality_data)
        print(f"  - Created document for personality '{personality_id}'.")

    print("\nFirestore personalities seeding process complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Seed Firestore database with personality data."
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="If set, existing personalities with the same ID will be overwritten.",
    )
    args = parser.parse_args()

    print(
        "This script will populate your Firestore database with personality data."
    )
    print(
        "--------------------------------------------------------------------------------"
    )
    if args.overwrite:
        print("Overwrite flag is set. Existing data will be replaced.")

    db_client = initialize_and_get_db()
    if db_client:
        seed_personalities(db_client, overwrite=args.overwrite)
    else:
        print("Could not initialize database. Aborting.", file=sys.stderr)
        sys.exit(1)
