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

## 安裝與設定

請依照以下步驟設定並執行 `core_processing_service`。

1.  **進入核心處理服務目錄**

    ```bash
    cd core_processing_service
    ```

2.  **建立虛擬環境**

    本專案建議使用 `uv` 來管理虛擬環境與套件。請先確保您已安裝 `uv`。

    使用 `uv` 建立一個名為 `.venv` 的虛擬環境：
    ```bash
    uv venv
    ```

3.  **啟用虛擬環境**

    ```bash
    source .venv/bin/activate
    ```
    啟用後，您的終端機提示符前應會顯示 `(.venv)`。

4.  **安裝依賴套件**

    使用 `uv` 安裝 `requirements.txt` 中定義的套件：
    ```bash
    uv pip install -r requirements.txt
    ```

## 執行服務

在啟用虛擬環境並安裝完所有依賴套件後，您可以使用 `uvicorn` 來啟動本地開發伺服器。

```bash
uv run uvicorn main:app --reload
```

`--reload` 參數會讓伺服器在偵測到程式碼變更時自動重啟，非常適合開發環境。

服務啟動後，您可以前往 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 查看自動產生的 API 文件。
