# NLP Data Processing and Inference Platform

This project is an implementation of the "NLP Data Processing and Inference Platform" as described in the system specification document.

## System Architecture

Below are the architecture diagrams for the system. These diagrams are rendered from text using Mermaid.js.

### High-Level Component Diagram

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

### Data Flow Diagram

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
