# 自然語言處理之資料處理與推論平台

本專案是基於提供的系統規格書所實現的「自然語言處理之資料處理與推論平台」。

## 系統架構

以下為本系統的架構圖。這些圖表是透過 Mermaid.js 從文字語法渲染而成。

### 高階元件圖

```mermaid
graph TD
    User\["使用者/外部應用程式"\] --> APIGateway\["API 閘道"\]
    InternalService\["內部服務"\] --> APIGateway

    APIGateway --> CoreProcessingService\["核心處理服務"\]
    CoreProcessingService --> MLInferenceService\["機器學習推論服務"\]
    MLInferenceService --> CoreProcessingService

    CoreProcessingService --> RawTextStore\["原始文字儲存 (非結構化)"\]
    CoreProcessingService --> ProcessedDataStore\["處理後資料儲存 (結構化)"\]
    MLInferenceService --> ProcessedDataStore

    APIGateway --> AuthZService\["認證/授權服務"\]
    AuthZService --> APIGateway

    subgraph Data Pipelines
        DataSources\["資料來源 (如：對話日誌)"\] --> DataIngestionPipeline\["資料攝取管道"\]
        DataIngestionPipeline --> RawTextStore
    end

    APIGateway -- 記錄請求 --> LoggingMonitoringSystem\["日誌記錄與監控系統"\]
    CoreProcessingService -- 記錄處理事件 --> LoggingMonitoringSystem
    MLInferenceService -- 記錄推論事件 --> LoggingMonitoringSystem
    AuthZService -- 記錄認證/授權事件 --> LoggingMonitoringSystem

    style User fill:#f9f,stroke:#333,stroke-width:2px
    style APIGateway fill:#bbf,stroke:#333,stroke-width:2px
    style CoreProcessingService fill:#bfb,stroke:#333,stroke-width:2px
    style MLInferenceService fill:#ffb,stroke:#333,stroke-width:2px
    style RawTextStore fill:#ddd,stroke:#333,stroke-width:2px
    style ProcessedDataStore fill:#ddd,stroke:#333,stroke-width:2px
    style LoggingMonitoringSystem fill:#fcc,stroke:#333,stroke-width:2px
    style AuthZService fill:#cff,stroke:#333,stroke-width:2px
    style DataSources fill:#f9f,stroke:#333,stroke-width:2px
    style DataIngestionPipeline fill:#bfb,stroke:#333,stroke-width:2px
    style InternalService fill:#f9f,stroke:#333,stroke-width:2px
```

### 資料流圖

```mermaid
graph TD
    A\[使用者/外部系統\] -- 1. 提交原始文字 (API 請求) --> B(API 閘道)
    B -- 2. 轉發請求並驗證 --> C{認證/授權服務}
    C -- 3. 驗證結果 --> B
    B -- 4. 轉發原始文字 --> D\[核心處理服務\]

    D -- 5. 文字預處理 --> E\[預處理模組\]
    E -- 6. 輸出預處理文字 --> F\[資訊提取/意圖分類模組\]
    F -- 7. 提取特徵/意圖 --> G\[機器學習推論服務\]

    G -- 8. 執行模型推論 --> H\[模型推論引擎\]
    H -- 9. 返回推論結果 --> G
    G -- 10. 返回結構化結果 --> D

    D -- 11. 儲存原始文字 --> I\[原始文字儲存\]
    D -- 12. 儲存處理後資料/結構化輸出 --> J\[處理後資料儲存\]

    D -- 13. 記錄處理日誌 --> K\[集中式日誌記錄系統\]
    G -- 14. 記錄推論日誌 --> K
    B -- 15. 記錄 API 存取日誌 --> K
    C -- 16. 記錄認證/授權日誌 --> K

    J -- 17. 資料用於模型再訓練 (MLOps) --> L\[模型訓練管道\]
    L -- 18. 部署新模型版本 --> G

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#cff,stroke:#333,stroke-width:2px
    style D fill:#bfb,stroke:#333,stroke-width:2px
    style E fill:#e6e6fa,stroke:#333,stroke-width:1px
    style F fill:#e6e6fa,stroke:#333,stroke-width:1px
    style G fill:#ffb,stroke:#333,stroke-width:2px
    style H fill:#e6e6fa,stroke:#333,stroke-width:1px
    style I fill:#ddd,stroke:#333,stroke-width:2px
    style J fill:#ddd,stroke:#333,stroke-width:2px
    style K fill:#fcc,stroke:#333,stroke-width:2px
    style L fill:#bbf,stroke:#333,stroke-width:2px
```

## 後端服務 (`backend/`)

此目錄包含使用 FastAPI 建置的核心後端服務。

### 本地開發

#### 環境需求

-   Python 3.12
-   虛擬環境管理工具 (例如 `venv` 或 `uv`)

#### 設定與執行服務

1.  **進入後端服務目錄**

    ```bash
    cd backend
    ```

2.  **啟用虛擬環境**

    本專案已包含一個預先設定好的虛擬環境。執行以下指令來啟用它：
    ```bash
    source .venv/bin/activate
    ```
    啟用後，您的終端機提示符前應會顯示 `(.venv)`。

3.  **安裝依賴套件**

    啟用虛擬環境後，安裝所需的套件。
    (建議使用 `uv`)
    ```bash
    uv pip install -r requirements.txt
    ```
    或者，您也可以使用 `pip`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **設定 Firebase 憑證 (若有需要)**

    如果服務需要連接到 Firebase，請遵循 `INSTRUCTIONS_FIREBASE.zh-TW.md` 中的說明，在此目錄中設定您的 `firebase-credentials.json` 檔案。

5.  **執行開發伺服器**

    使用 `uvicorn` 來執行 FastAPI 應用程式。`--reload` 參數會在偵測到程式碼變更時自動重啟。
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

    服務啟動後，您可以前往 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 查看自動產生的 API 文件。

### 執行測試

若要執行自動化測試，請使用以下指令：

```bash
python3 -m unittest backend/tests/test_tree_engine.py
```

### 填充 Firestore 資料庫

您可以執行填充指令碼，將初始資料填入您的 Firestore 資料庫。在執行此操作前，請確保您的 Firebase 憑證已正確設定。

```bash
python3 backend/scripts/seed_firestore.py
```

此指令碼會在您的 Firestore 資料庫中建立必要的集合與文件。如果資料已存在，腳本不會進行覆寫。
