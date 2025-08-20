#!/bin/bash

# API 基礎 URL
BASE_URL="http://127.0.0.1:8000/api/v1"
TREE_ID="stock_investment_tsmc"

# 1. 開始決策樹遍歷 (從根節點開始)
echo "測試：開始決策樹 '$TREE_ID' 的遍歷"
curl -X 'POST' \
  "$BASE_URL/decide" \
  -H 'Content-Type: application/json' \
  -d "{
  \"tree_id\": \"$TREE_ID\"
}"
echo -e "\n"

# -------------------------------------------------------------------
# 注意：
# 您需要從上面的回應中手動複製 \"node_id\" 的值 (例如 \"root\")，
# 並將其貼到下面的 CURRENT_NODE_ID 變數中。
# -------------------------------------------------------------------

# 2. 繼續遍歷 (回答第一個問題)
CURRENT_NODE_ID="root" # <-- 請手動更新此處的 node_id
ANSWER="長期持有"       # <-- 您可以更改這個答案

echo "測試：繼續遍歷，回答 '$ANSWER'"
curl -X 'POST' \
  "$BASE_URL/decision/decide" \
  -H 'Content-Type: application/json' \
  -d "{
  \"tree_id\": \"$TREE_ID\",
  \"current_node_id\": \"$CURRENT_NODE_ID\",
  \"answer\": \"$ANSWER\"
}"
echo -e "\n"
