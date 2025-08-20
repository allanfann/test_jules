#!/bin/bash

# API 基礎 URL
BASE_URL="http://127.0.0.1:8000/api/v1"

# --- Analysis Endpoints ---
echo "--- 測試分析相關 API ---"

# 測試 /analysis/personality_analysis
echo "測試：人格分析 (/analysis/personality_analysis)"
curl -X 'POST' \
  "$BASE_URL/analysis/personality_analysis" \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "I am confident that we can achieve our goals. The future looks bright and full of possibilities."
}'
echo -e "\n"

# 測試 /analysis/mbti_analysis
echo "測試：MBTI 分析 (/analysis/mbti_analysis)"
curl -X 'POST' \
  "$BASE_URL/analysis/mbti_analysis" \
  -H 'Content-Type: application/json' \
  -d '{
  "answers": ["E", "N", "F", "P"]
}'
echo -e "\n"


# --- Processing Endpoints ---
echo "--- 測試文字處理相關 API ---"

# 測試 /processing/text-processing
echo "測試：文字處理 (/processing/text-processing)"
curl -X 'POST' \
  "$BASE_URL/processing/text-processing" \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "This is a sample text for BERT processing.",
  "tenant_id": "tenant-123"
}'
echo -e "\n"

# 測試 /processing/information-extraction
echo "測試：資訊擷取 (/processing/information-extraction)"
curl -X 'POST' \
  "$BASE_URL/processing/information-extraction" \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "The quick brown fox jumps over the lazy dog.",
  "tenant_id": "tenant-123"
}'
echo -e "\n"

# 測試 /processing/intent-classification
echo "測試：意圖分類 (/processing/intent-classification)"
curl -X 'POST' \
  "$BASE_URL/processing/intent-classification" \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "請問今天天氣如何？",
  "tenant_id": "tenant-123"
}'
echo -e "\n"

# 測試 /processing/structured-conversion
echo "測試：結構化轉換 (/processing/structured-conversion)"
curl -X 'POST' \
  "$BASE_URL/processing/structured-conversion" \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "姓名: 王小明\n年齡: 30\n職業: 工程師",
  "tenant_id": "tenant-123",
  "schema_id": "user-profile-v1"
}'
echo -e "\n"
