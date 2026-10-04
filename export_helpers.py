"""
匯出輔助函式庫 (Export Helpers v2.1)
支援 Markdown、JSON、HTML 互動式簡報、CSV 數據下載與 SHA-256 數位指紋產生
深度整合 STP、4P、P&L 損益、Persona、同理心地圖與 NSDB 分析模型
所有權人：BOSS / 院長 / Eric 潘穩安博士
"""

import hashlib
import json
import csv
import io
from datetime import datetime
from sample_data import SYSTEM_OWNERSHIP, TUKUYI_BRAND_IDENTITY, VIRTUAL_SALES_DATA

def compute_sha256(content: str) -> str:
    """計算字串內容之 SHA-256 雜湊碼作為企劃版本防篡改指紋"""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def export_proposal_json(data: dict) -> str:
    """匯出結構化 JSON 字串"""
    export_payload = {
        "document_type": "tukuyi_marketing_proposal_v2.1",
        "system_owner": SYSTEM_OWNERSHIP["owner"],
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "brand": TUKUYI_BRAND_IDENTITY["brand_name"],
        "version": SYSTEM_OWNERSHIP["version"],
        "data": data
    }
    return json.dumps(export_payload, ensure_ascii=False, indent=2)

def export_proposal_markdown(data: dict) -> str:
    """匯出符合 GitHub Flavored Markdown 規範之完整企劃書"""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title = data.get("title", "土庫驛 B2B 節慶企業禮盒行銷企劃案")
    audience = data.get("audience_name", "企業客戶提案 (福委 / 總務 / 採購)")
    festival = data.get("festival", "聖誕節年終感恩")
    
    # 預先計算內文指紋
    raw_content = f"{title}-{audience}-{festival}-{data.get('summary', '')}"
    fingerprint = compute_sha256(raw_content)[:16]

    md = f"""---
title: "{title}"
owner: "{SYSTEM_OWNERSHIP['owner']}"
brand: "土庫驛可可莊園 (Tukuyi Cocoa)"
festival: "{festival}"
audience: "{audience}"
generated_at: "{now_str}"
verification_fingerprint: "SHA256-{fingerprint}"
confidentiality: "土庫驛內部培訓與實務演練專用 • 嚴禁未經授權之第三方轉售"
---

# 🍫 {title}

> **【系統所有權人】**：{SYSTEM_OWNERSHIP['owner']}  
> **【企劃版本防偽指紋】**：`SHA256-{fingerprint}`  
> **【提案品牌】**：土庫驛可可莊園 (Tukuyi Cocoa)  
> **【目標受眾】**：{audience}  
> **【節慶專案】**：{festival}  
> **【建立時間】**：{now_str}  

---

## 📌 一、 執行摘要 (Executive Summary)
{data.get("summary", "本企劃旨在以土庫驛頂級 Tree-to-Bar 可可莊園的職人故事與 0 反式脂肪純黑巧，突破傳統節慶送禮同質化紅海。")}

---

## 🏛️ 二、 Phase 01 品牌底蘊與 P&L 財務損益結構
* **品牌願景與初心**：{data.get("brand_origin", "創辦人為失智父親返鄉打造 Tree-to-Bar 可可創生莊園，做純淨無添加巧克力給父親吃。")}
* **核心工藝**：{data.get("brand_craft", "13道工序慢磨、100%天然可可脂、零反式脂肪、在地小農契作。")}
* **P&L 損益與營收指標**：
  - 專案營收規模：`{data.get("kpi_revenue", "NT$ 2,200,000")}`
  - 目標銷售盒數：`{data.get("kpi_boxes", "2,000 盒")}`
  - 預估毛利率：`{data.get("kpi_margin", "57.2%")}`
  - 預估營業淨利率：`{data.get("pnl_net_margin", "38.5%")}`
  - 關鍵成本結構：{data.get("pnl_notes", "原物料與工廠慢磨製程佔 42.8%，客製燙金腰封與溫控物流佔 11.5%，營業費用佔 7.2%。")}

---

## 🎯 三、 產品市場定位策略 (STP)
* **市場區隔 (Market Segmentation)**：{data.get("stp_s", "以重視 ESG 永續、員工健康、高美學質感的科技半導體與外商金融企業為核心。")}
* **目標市場 (Targeting)**：{data.get("stp_t", "鎖定客單價 $800 - $1,500 區間之年終福委及 VIP 外部客戶禮盒。")}
* **品牌定位 (Positioning)**：{data.get("stp_p", "『雲林在地創生 x 米其林級頂級可可』之尊榮商務賀禮。")}

---

## 📦 四、 4P 行銷組合落地策略
* **產品策略 (Product)**：{data.get("p_product", "85% 生巧克力 + 小山園抹茶生巧 + 莊園可可豆茶包，冷藏常溫彈性配搭。")}
* **定價策略 (Price)**：{data.get("p_price", "三階梯定價：分享款 $699 / 尊爵款 $1,099 / 旗艦奢華款 $1,680。")}
* **通路策略 (Place)**：{data.get("p_place", "專人 B2B 顧問一對一試吃配送、企業專屬線上大宗試算下單頁面。")}
* **推廣策略 (Promotion)**：{data.get("p_promotion", "早鳥滿額免運溫控、免費客製燙金腰封與企業 Logo 雷雕、附贈地方創生小卡。")}

---

## 👥 五、 Phase 02 目標受眾 Persona、同理心與 NSDB 說服架構
* **Persona 角色模型**：{data.get("persona_desc", "科技業福委主委與行政總務，注重同仁口碑與預算防線。")}
* **同理心地圖痛點 (Empathy Map)**：{data.get("empathy_pains", "員工嫌傳統月餅油膩熱量高；冷藏保存困難且公司冰箱爆滿；預算死板卡在特定區間。")}
* **NSDB 說服切角矩陣**：
  - **Need (受眾深層需求)**：{data.get("nsdb_n", "健康無負擔、送禮有面子、行政省事無客訴。")}
  - **Solution (核心解方)**：{data.get("nsdb_s", "米其林級無糖黑巧 + 莊園可可豆茶，搭配常溫低溫雙軌配送。")}
  - **Differentiation (獨特差異)**：{data.get("nsdb_d", "Tree-to-Bar 13道工序慢磨、創生孝心故事、免費客製燙金。")}
  - **Benefit (綜合效益)**：{data.get("nsdb_b", "同仁滿意度 95% 以上，減輕總務 60% 配送負擔，提升企業 ESG 永續形象。")}

---

## 🎨 六、 Phase 03 視覺生圖提示詞 (ChatGPT & Gemini 通用)
```text
{data.get("image_prompt", "Commercial luxury food photography of Tukuyi Cocoa gift box.")}
```

---
*本報告由「土庫驛 AI 行銷企劃工作台」自動生成，所有權人：Eric 潘穩安博士，對齊土庫驛品牌識別指南 (CI/VI)*
"""
    return md

def export_virtual_sales_csv() -> str:
    """將虛擬銷售數據包匯出為 CSV 格式字串"""
    output = io.StringIO()
    if not VIRTUAL_SALES_DATA:
        return ""
    fieldnames = list(VIRTUAL_SALES_DATA[0].keys())
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in VIRTUAL_SALES_DATA:
        writer.writerow(row)
    return output.getvalue()

def generate_standalone_html_deck(data: dict) -> str:
    """產生精美、可離線獨立運行的土庫驛品牌簡報 (HTML 互動投影片)"""
    title = data.get("title", "土庫驛 2026 B2B 企業禮盒提案簡報")
    audience = data.get("audience_name", "企業客戶提案 (福委 / 總務 / 採購)")
    summary = data.get("summary", "以 Tree-to-Bar 頂級生巧克力與可可豆茶，為企業客戶帶來極致奢華且健康無負擔的年終賀禮。")

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | 土庫驛可可莊園</title>
  <style>
    :root {{
      --primary-cocoa: #3B2314;
      --secondary-gold: #D4AF37;
      --cream-bg: #FDFBF7;
      --charcoal: #222222;
      --card-bg: #2A180D;
      --card-light: #FFFFFF;
      --text-gold: #F3E5AB;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans TC", sans-serif;
      background: #150E09;
      color: #EAE6E1;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
      padding: 24px;
    }}
    .presentation-container {{
      width: 100%;
      max-width: 1080px;
      background: var(--card-bg);
      border: 2px solid var(--secondary-gold);
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 16px 40px rgba(0,0,0,0.6);
    }}
    .header-bar {{
      background: linear-gradient(135deg, #3B2314 0%, #1F120A 100%);
      padding: 24px 32px;
      border-bottom: 2px solid rgba(212, 175, 55, 0.4);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .header-bar h1 {{
      font-size: 22px;
      color: var(--secondary-gold);
      letter-spacing: 1px;
    }}
    .badge {{
      background: rgba(212, 175, 55, 0.15);
      border: 1px solid var(--secondary-gold);
      color: var(--secondary-gold);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
    }}
    .slide-body {{
      padding: 36px 40px;
      background: radial-gradient(circle at 80% 20%, #351F12 0%, #1D1109 100%);
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-top: 20px;
    }}
    .card {{
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(212, 175, 55, 0.25);
      border-radius: 12px;
      padding: 20px;
      transition: all 0.2s ease;
    }}
    .card:hover {{
      border-color: var(--secondary-gold);
      transform: translateY(-2px);
    }}
    .card-title {{
      color: var(--secondary-gold);
      font-size: 16px;
      font-weight: 700;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .card-text {{
      color: #DDD6CE;
      font-size: 14px;
      line-height: 1.6;
    }}
    .metric-row {{
      display: flex;
      gap: 16px;
      margin-top: 24px;
    }}
    .metric-box {{
      flex: 1;
      background: rgba(212, 175, 55, 0.08);
      border: 1px dashed rgba(212, 175, 55, 0.4);
      border-radius: 10px;
      padding: 16px;
      text-align: center;
    }}
    .metric-value {{
      font-size: 26px;
      font-weight: 800;
      color: var(--secondary-gold);
      margin-bottom: 4px;
    }}
    .metric-label {{
      font-size: 12px;
      color: #BBB0A4;
    }}
    .footer-bar {{
      background: #140C07;
      padding: 16px 32px;
      border-top: 1px solid rgba(255,255,255,0.08);
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      color: #998C80;
    }}
    @media (max-width: 768px) {{
      .grid-2 {{ grid-template-columns: 1fr; }}
      .metric-row {{ flex-direction: column; }}
    }}
  </style>
</head>
<body>
  <div class="presentation-container">
    <div class="header-bar">
      <div>
        <div style="font-size: 12px; color: #A69282; margin-bottom: 4px;">TUKUYI COCOA ESTATE • B2B PROPOSAL • 所有權人：Eric 潘穩安博士</div>
        <h1>{title}</h1>
      </div>
      <div class="badge">目標受眾：{audience}</div>
    </div>

    <div class="slide-body">
      <div style="background: rgba(212,175,55,0.08); border-left: 4px solid var(--secondary-gold); padding: 14px 18px; border-radius: 4px; margin-bottom: 24px;">
        <div style="font-size: 13px; color: var(--secondary-gold); font-weight: 700; margin-bottom: 4px;">💡 專案核心構想</div>
        <div style="font-size: 15px; color: #F0ECE6; line-height: 1.5;">{summary}</div>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="card-title">🎯 STP 市場定位核心</div>
          <div class="card-text">
            <strong>市場區隔：</strong> {data.get("stp_s", "注重 ESG 與同仁健康的企業福委")}<br><br>
            <strong>目標市場：</strong> {data.get("stp_t", "客單價 $800~$1,500 區間採購專案")}<br><br>
            <strong>品牌定位：</strong> {data.get("stp_p", "Tree-to-Bar 雲林創生尊榮商務禮盒")}
          </div>
        </div>

        <div class="card">
          <div class="card-title">💎 NSDB 說服核心架構</div>
          <div class="card-text">
            <strong>Need 需求：</strong> {data.get("nsdb_n", "兼顧星級大氣面子與 0 反式脂肪健康")}<br><br>
            <strong>Solution 解方：</strong> {data.get("nsdb_s", "85% 生巧 + 莊園可可茶常溫冷藏雙軌")}<br><br>
            <strong>Differentiation 差異：</strong> {data.get("nsdb_d", "13道工序慢磨 x 創生孝心故事 x 客製腰封")}<br><br>
            <strong>Benefit 效益：</strong> {data.get("nsdb_b", "同仁滿意度 95% 以上，行政零負擔")}
          </div>
        </div>
      </div>

      <div class="metric-row">
        <div class="metric-box">
          <div class="metric-value">{data.get("kpi_boxes", "2,000 盒")}</div>
          <div class="metric-label">目標採購盒數</div>
        </div>
        <div class="metric-box">
          <div class="metric-value">{data.get("kpi_revenue", "NT$ 2.2M")}</div>
          <div class="metric-label">預期營收規模</div>
        </div>
        <div class="metric-box">
          <div class="metric-value">{data.get("kpi_margin", "56.5%")}</div>
          <div class="metric-label">預估毛利率</div>
        </div>
        <div class="metric-box">
          <div class="metric-value">{data.get("kpi_satisfaction", "4.8 ★")}</div>
          <div class="metric-label">預期同仁滿意度</div>
        </div>
      </div>
    </div>

    <div class="footer-bar">
      <div>🌱 土庫驛可可莊園 • Tree-to-Bar 原豆慢磨工藝 • 雲林地方創生</div>
      <div>系統所有權人：Eric 潘穩安博士 ｜ 規範對齊：Brand CI/VI Guidelines</div>
    </div>
  </div>
</body>
</html>
"""
    return html
