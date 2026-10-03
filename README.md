# 🍫 土庫驛可可莊園 (Tukuyi Cocoa) - AI 行銷企劃大師工作台

> **企業內部培訓專屬交付成果**  
> 《AI 應用於行銷企劃撰寫與簡報提案技巧》（6小時工作坊）課後實用工具  
> 遵循 **BYOK (Bring Your Own Key) 零成本原則**，免付費啟動，支援 GitHub 與 Streamlit Community Cloud 一鍵部署。

---

## 🌟 核心特色與價值 (What You Take Away)

1. **土庫驛 CI/VI 視覺底層自動約束**：
   - 內建品牌標準色（頂級可可棕 `#3B2314`、典雅香檳金 `#D4AF37`、絲滑奶霜白 `#FDFBF7`）。
   - 自動將「Tree-to-Bar 13道慢磨工藝」與「為父造莊園地方創生」初心融入企劃與提案。
2. **3 大簡報場景與受眾心理切換**：
   - 40% 內部決策會議（公司主管：ROI、毛利、產能風險、排程）。
   - 40% 企業客戶提案（福委 / 總務 / 採購：員工滿意、低糖健康、常溫/低溫配送容錯）。
   - 20% 異業結盟夥伴（高階主管 / 老闆：品牌雙贏、VIP 專屬私宴、ESG 文化厚度）。
3. **ChatGPT Images 2.5 視覺生圖實驗室**：
   - 包含商品攝影圖、聖誕禮盒 3D 擬真渲染圖、一頁式企劃資訊圖卡 (Infographic) 專業提示詞公式。
4. **多格式商業交付一鍵匯出**：
   - 原生 16:9 PowerPoint 簡報 (`.pptx`)
   - 獨立高奢品牌互動簡報 (`.html`)
   - 結構化企劃書 (`.md` 附帶 SHA-256 驗證指紋)
   - 系統整合結構資料 (`.json`)
   - 歷年 B2B 虛擬銷售數據包 (`.csv`)
5. **BYOK 雙軌運行模式**：
   - 支援免費 Google Gemini API Key。
   - 內建「高擬真模擬模式」，學員無需金鑰亦可完整體驗生成成果。

---

## 🚀 快速啟動指南 (Local Running)

### 1. 安裝環境依賴
```bash
pip install -r requirements.txt
```

### 2. 本機啟動 Streamlit
```bash
streamlit run app.py
```
啟動後，瀏覽器將自動開啟 `http://localhost:8501`。

---

## ☁️ Streamlit Community Cloud 0元免費部署步驟

1. 將本專案資料夾推送到您的個人或企業 **GitHub Repository**。
2. 登入 [Streamlit Community Cloud](https://share.streamlit.io/)。
3. 點選 **New app**，選擇剛才建立的 GitHub Repo 與 `app.py`。
4. 點選 **Deploy**，約 1~2 分鐘即可獲得全體學員皆可連線存取的專屬網址！
5. 學員開啟網頁後，即可自行輸入免費 Google Gemini API Key 或直接切換模擬模式使用。

---

## 🔑 免費取得 Google Gemini API Key 說明

1. 前往 [Google AI Studio](https://aistudio.google.com/)。
2. 以個人或企業 Google 帳號登入。
3. 點擊畫面左上角或右上角的 **"Get API key"** -> **"Create API key"**。
4. 複製獲得的 API Key，貼入 Web App 側邊欄即可。
*(依據 Google 官方方案，每分鐘享有 15 次免費請求額度，企業演練與日常企劃完全 0 元成本)*

---

## 📁 檔案結構說明

```text
tukuyi-ai-marketing-app/
├── app.py                  # Streamlit 主程式 (全功能頁籤導航與互動介面)
├── sample_data.py          # 土庫驛 CI/VI 規範、教學案例、受眾 Persona、提示詞總庫與虛擬數據包
├── export_helpers.py       # Markdown/JSON/HTML/CSV 多格式匯出與 SHA-256 指紋演算法
├── generate_pptx.py        # 原生 16:9 品牌 CI/VI PPTX 簡報生成引擎
├── style.css               # 土庫驛奢華巧克力大地色視覺主題樣式表
├── test_suite.py           # 自動化測試套件 (涵蓋資料完整性、匯出檢驗與語法檢查)
├── requirements.txt        # Python 依賴清單
├── .streamlit/
│   └── config.toml         # Streamlit 品牌配色與伺服器最佳化配置
└── README.md               # 專案說明與操作手冊
```

---
*土庫驛可可莊園 (Tukuyi Cocoa) 企業內部教育訓練成果交付*
