# Firebase 設定說明

若要為此服務啟用 Firebase 整合，您需要提供您的 Firebase 專案的服務帳戶憑證。

## 步驟：

1.  **前往您的 Firebase 專案設定：**
    *   前往 [Firebase 控制台](https://console.firebase.google.com/)。
    *   選擇您的專案。
    *   點擊「專案總覽」(Project Overview) 旁邊的齒輪圖示 (⚙️)，然後選擇「專案設定」(Project settings)。

2.  **產生新的私鑰：**
    *   在專案設定中，前往「服務帳戶」(Service accounts) 分頁。
    *   點擊「產生新的私鑰」(Generate new private key) 按鈕。
    *   將會出現一個確認對話框，點擊「產生金鑰」(Generate key)。

3.  **儲存憑證檔案：**
    *   一個 JSON 檔案將會被下載到您的電腦。此檔案包含您專案的私密憑證。**請像對待密碼一樣安全地保管此檔案。**
    *   將下載的檔案重新命名為 `firebase-credentials.json`。

4.  **將檔案放置在正確的目錄中：**
    *   將 `firebase-credentials.json` 檔案移動到本專案的 `core_processing_service/` 目錄下。

`firebase_setup.py` 模組被設計為會自動載入此檔案。該檔名已經被列在 `.gitignore` 中，所以它不會被提交到您的版本控制歷史記錄中。

一旦檔案就緒，應用程式啟動時將能夠連接到您的 Firestore 資料庫。
