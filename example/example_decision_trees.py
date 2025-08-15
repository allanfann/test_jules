
"""
This file contains example decision trees for seeding into Firestore.
Each tree is a dictionary following the structure required by seed_firestore.py.
"""

TREES_DATA = [
    {
        "tree_id": "stock_investment_tsmc",
        "description": "評估是否該買台積電股票的決策樹。",
        "nodes": {
            "root": {
                "text": "你的投資策略是長期持有還是短期獲利？",
                "type": "DECISION",
                "children": [
                    {"answer_text": "長期持有", "next_node_id": "long_term"},
                    {"answer_text": "短期獲利", "next_node_id": "short_term"}
                ]
            },
            "long_term": {
                "text": "你是否看好台灣半導體產業的長期發展？",
                "type": "DECISION",
                "children": [
                    {"answer_text": "是，非常看好", "next_node_id": "buy_stock"},
                    {"answer_text": "否，認為有風險", "next_node_id": "observe"}
                ]
            },
            "short_term": {
                "text": "你是否能接受短期股價大幅波動的風險？",
                "type": "DECISION",
                "children": [
                    {"answer_text": "是，願意承擔風險", "next_node_id": "buy_stock_short_term"},
                    {"answer_text": "否，偏好穩健", "next_node_id": "dont_buy"}
                ]
            },
            "buy_stock": {
                "text": "結論：可以考慮在合適價位分批買入，作為長期投資標的。",
                "type": "OUTCOME",
                "children": []
            },
            "buy_stock_short_term": {
                "text": "結論：可以投入部分資金進行短線操作，但需設定好停損點。",
                "type": "OUTCOME",
                "children": []
            },
            "observe": {
                "text": "結論：建議繼續觀察，等待產業前景更明朗或股價回調時再考慮。",
                "type": "OUTCOME",
                "children": []
            },
            "dont_buy": {
                "text": "結論：短期風險較高，建議尋找更穩健的投資標的。",
                "type": "OUTCOME",
                "children": []
            }
        }
    },
    {
        "tree_id": "marriage_decision",
        "description": "評估是否該與眼前的伴侶結婚的決策樹。",
        "nodes": {
            "root": {
                "text": "你們對於未來的生活藍圖（例如：家庭、事業、居住地）有共識嗎？",
                "type": "DECISION",
                "children": [
                    {"answer_text": "是，有清晰的共識", "next_node_id": "values_check"},
                    {"answer_text": "否，想法有很多分歧", "next_node_id": "reconsider_marriage"}
                ]
            },
            "values_check": {
                "text": "你們的核心價值觀（例如：金錢觀、家庭觀）是否契合？",
                "type": "DECISION",
                "children": [
                    {"answer_text": "是，非常契合", "next_node_id": "propose"},
                    {"answer_text": "否，時常因此爭吵", "next_node_id": "communicate_more"}
                ]
            },
            "propose": {
                "text": "結論：你們的關係基礎穩固，前景看好，可以認真考慮走向婚姻。",
                "type": "OUTCOME",
                "children": []
            },
            "communicate_more": {
                "text": "結論：建議進行深度溝通，尋求專業諮商，解決價值觀衝突問題，再考慮婚姻。",
                "type": "OUTCOME",
                "children": []
            },
            "reconsider_marriage": {
                "text": "結論：未來規劃存在重大分歧，建議先解決這些問題，目前不適合馬上結婚。",
                "type": "OUTCOME",
                "children": []
            }
        }
    },
    {
        "tree_id": "career_change",
        "description": "評估是否要換工作的決策樹。",
        "nodes": {
            "root": {
                "text": "你對目前的工作感到不滿的主要原因是什麼？",
                "type": "DECISION",
                "children": [
                    {"answer_text": "薪資福利不符期待", "next_node_id": "salary_issue"},
                    {"answer_text": "缺乏成長與發展空間", "next_node_id": "growth_issue"},
                    {"answer_text": "工作壓力或人際關係", "next_node_id": "environment_issue"}
                ]
            },
            "salary_issue": {
                "text": "你是否已經有獲得薪資更高的錄取通知(Offer)？",
                "type": "DECISION",
                "children": [
                    {"answer_text": "是", "next_node_id": "change_job"},
                    {"answer_text": "否", "next_node_id": "negotiate_or_search"}
                ]
            },
            "growth_issue": {
                "text": "目前的公司內部是否有其他職位或專案的發展機會？",
                "type": "DECISION",
                "children": [
                    {"answer_text": "是，可以爭取", "next_node_id": "stay_and_grow"},
                    {"answer_text": "否，已無空間", "next_node_id": "change_job"}
                ]
            },
            "environment_issue": {
                "text": "這個問題是否可以透過溝通或調整來解決？",
                "type": "DECISION",
                "children": [
                    {"answer_text": "是，願意嘗試", "next_node_id": "stay_and_improve"},
                    {"answer_text": "否，難以改變", "next_node_id": "change_job"}
                ]
            },
            "change_job": {
                "text": "結論：時機成熟，開始積極尋找或接受新的工作機會。",
                "type": "OUTCOME",
                "children": []
            },
            "negotiate_or_search": {
                "text": "結論：建議先與現任主管溝通，爭取調薪，同時開始尋找其他機會。",
                "type": "OUTCOME",
                "children": []
            },
            "stay_and_grow": {
                "text": "結論：建議先在內部尋求發展，爭取新的角色或責任。",
                "type": "OUTCOME",
                "children": []
            },
            "stay_and_improve": {
                "text": "結論：建議先嘗試改善目前的工作環境，如果無效再考慮離開。",
                "type": "OUTCOME",
                "children": []
            }
        }
    },
    {
        "tree_id": "university_major_selection",
        "description": "基於聯考成績選擇大學科系的決策樹。",
        "nodes": {
            "root": {
                "text": "你的興趣偏向文法商，還是理工醫農？",
                "type": "DECISION",
                "children": [
                    {"answer_text": "文法商", "next_node_id": "humanities"},
                    {"answer_text": "理工醫農", "next_node_id": "stem"}
                ]
            },
            "humanities": {
                "text": "你未來想從事與人高度互動的工作，還是偏向獨立研究？",
                "type": "DECISION",
                "children": [
                    {"answer_text": "與人互動", "next_node_id": "business_law"},
                    {"answer_text": "獨立研究", "next_node_id": "literature_history"}
                ]
            },
            "stem": {
                "text": "你對理論科學與基礎研究更有興趣，還是應用科學與工程技術？",
                "type": "DECISION",
                "children": [
                    {"answer_text": "理論科學", "next_node_id": "pure_science"},
                    {"answer_text": "應用科學", "next_node_id": "engineering_medicine"}
                ]
            },
            "business_law": {
                "text": "結論：可以考慮商管、法律、大眾傳播等科系。",
                "type": "OUTCOME",
                "children": []
            },
            "literature_history": {
                "text": "結論：可以考慮文學、歷史、哲學、外語等科系。",
                "type": "OUTCOME",
                "children": []
            },
            "pure_science": {
                "text": "結論：可以考慮物理、化學、數學等基礎科學科系。",
                "type": "OUTCOME",
                "children": []
            },
            "engineering_medicine": {
                "text": "結論：可以考慮資訊工程、電機、機械、醫學、藥學等應用科學科系。",
                "type": "OUTCOME",
                "children": []
            }
        }
    },
    {
        "tree_id": "having_children_decision",
        "description": "評估現階段是否該生小孩的決策樹。",
        "nodes": {
            "root": {
                "text": "你和你的伴侶是否都發自內心想要有小孩？",
                "type": "DECISION",
                "children": [
                    {"answer_text": "是，我們都想要", "next_node_id": "financial_check"},
                    {"answer_text": "否，其中一方或雙方都不確定", "next_node_id": "wait_and_see"}
                ]
            },
            "financial_check": {
                "text": "你們目前的經濟狀況是否穩定，足以支撐育兒的開銷？",
                "type": "DECISION",
                "children": [
                    {"answer_text": "是，經濟狀況穩定", "next_node_id": "ready_for_kids"},
                    {"answer_text": "否，經濟壓力較大", "next_node_id": "prepare_financially"}
                ]
            },
            "support_system_check": {
                "text": "你們是否有足夠的後援系統（如家人、朋友）可以協助育兒？",
                "type": "DECISION",
                "children": [
                    {"answer_text": "是，後援充足", "next_node_id": "ready_for_kids"},
                    {"answer_text": "否，需要靠自己", "next_node_id": "build_support"}
                ]
            },
            "ready_for_kids": {
                "text": "結論：你們在心態、經濟和後援上都準備好了，可以開始規劃迎接新生命。",
                "type": "OUTCOME",
                "children": []
            },
            "prepare_financially": {
                "text": "結論：建議先制定一個儲蓄和理財計畫，為育兒做好經濟準備。",
                "type": "OUTCOME",
                "children": []
            },
            "wait_and_see": {
                "text": "結論：生小孩是重大決定，建議雙方深入溝通，達成共識前不宜草率決定。",
                "type": "OUTCOME",
                "children": []
            },
            "build_support": {
                "text": "結論：建議先規劃好未來的育兒模式，並尋找可能的社會資源或支持系統。",
                "type": "OUTCOME",
                "children": []
            }
        }
    }
]
