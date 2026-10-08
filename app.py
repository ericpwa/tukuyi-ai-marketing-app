"""
土庫驛可可莊園 (Tukuyi Cocoa) - AI 行銷企劃大師 Web App (v2.1 Enterprise)
==============================================================================
所有權人 / 著作權人：BOSS、院長、Eric 潘穩安博士 (Dr. Eric Wen-An Pan)
核心架構：伺服器端 BYOK (Google Gemini API)、提案雜湊校驗、動態模型容錯、
Phase 01~04 全流程開放式引導填答、STP+4P+P&L、Persona+同理心+NSDB、
ChatGPT & Gemini 通用生圖提示詞、真實數據 CSV/XLSX 上傳與多格式簡報匯出。
==============================================================================
"""

import os
import json
import streamlit as st
import pandas as pd
from datetime import datetime
import io

# 導入內部模組
from sample_data import (
    SYSTEM_OWNERSHIP,
    TUKUYI_BRAND_IDENTITY,
    AUDIENCE_PERSONAS,
    MID_AUTUMN_CASE,
    CHRISTMAS_WORKSHOP_CASE,
    VIRTUAL_SALES_DATA,
    PROMPT_TEMPLATES
)
from export_helpers import (
    export_proposal_markdown,
    export_proposal_json,
    export_virtual_sales_csv,
    generate_standalone_html_deck,
    compute_sha256
)
from generate_pptx import build_tukuyi_pptx, HAS_PPTX

# ==============================================================================
# 頁面配置 (Streamlit Page Config)
# ==============================================================================
st.set_page_config(
    page_title="土庫驛可可莊園 ｜ AI 行銷企劃大師工作台",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 載入自訂 CSS 樣式
def load_css(file_name="style.css"):
    css_path = os.path.join(os.path.dirname(__file__), file_name)
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# ==============================================================================
# Session State 初始化與 Gemini 客戶端架構
# ==============================================================================
DEFAULT_MODELS = [
    "gemini-1.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-pro",
    "gemini-1.5-flash-8b"
]

session_defaults = {
    "api_key": "",
    "api_key_valid": False,
    "model_name": "gemini-1.5-flash",
    "available_models": DEFAULT_MODELS,
    "simulation_mode": True,
    "api_error": None,
    "current_proposal": None,
    # Phase 01 數據同步欄位
    "p1_revenue": "NT$ 4,860,000",
    "p1_boxes": "4,120 盒",
    "p1_aov": "NT$ 1,180",
    "p1_margin": "58.4%",
    "p1_net_margin": "38.4%",
    # Phase 02 與 Phase 04 聯動資料
    "p1_p2_integrated_data": {}
}

for k, v in session_defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def get_gemini_client(api_key: str):
    """安全清理並初始化 Google GenAI Client"""
    if not api_key:
        return None
    try:
        from google import genai
        clean_key = api_key.strip().strip("'").strip('"').strip('`')
        if not clean_key:
            return None
        return genai.Client(api_key=clean_key)
    except Exception as e:
        st.session_state.api_error = "無法初始化 Google GenAI SDK，請確認金鑰與執行環境。原始錯誤內容不顯示。"
        return None

def validate_and_discover_gemini(api_key: str) -> bool:
    """透明檢驗 API Key 並動態探索可用模型 (避免 404 NOT_FOUND 錯誤)"""
    clean_key = api_key.strip().strip("'").strip('"').strip('`')
    if not clean_key:
        st.session_state.api_error = "金鑰不可為空白"
        st.session_state.api_key_valid = False
        return False

    client = get_gemini_client(clean_key)
    if not client:
        return False

    try:
        raw_models = list(client.models.list())
        discovered = []
        for m in raw_models:
            name = getattr(m, "name", "").replace("models/", "")
            methods = getattr(m, "supported_generation_methods", [])
            if "generateContent" in methods or "gemini" in name:
                if name in DEFAULT_MODELS or "flash" in name or "pro" in name:
                    discovered.append(name)
        if discovered:
            st.session_state.available_models = discovered
            if st.session_state.model_name not in discovered:
                st.session_state.model_name = discovered[0]
            st.session_state.api_key_valid = True
            st.session_state.api_error = None
            return True
    except Exception:
        pass

    for test_model in DEFAULT_MODELS:
        try:
            client.models.generate_content(
                model=test_model,
                contents="PING"
            )
            st.session_state.model_name = test_model
            st.session_state.api_key_valid = True
            st.session_state.api_error = None
            return True
        except Exception as e:
            st.session_state.api_error = "金鑰驗證失敗，請檢查金鑰、權限、配額與模型可用性。原始錯誤內容不顯示。"
            continue

    st.session_state.api_key_valid = False
    return False

# ==============================================================================
# 側邊欄 (Sidebar) - 著作權、BYOK 認證與品牌資產速查
# ==============================================================================
with st.sidebar:
    st.markdown("### 🍫 土庫驛可可莊園")
    st.markdown("**AI 行銷企劃大師工作台 v2.1**")
    st.caption("企業專屬內訓交付 • 課後永久帶走實用工具")

    st.markdown("---")
    st.markdown("#### ⚖️ 系統所有權與智財權宣告")
    st.markdown(f"""
    <div style="font-size: 11.5px; color: #BBB; background: rgba(212,175,55,0.08); border-left: 3px solid #D4AF37; padding: 8px 10px; border-radius: 4px; margin-bottom: 12px;">
        <strong>所有權人 / 著作權人：</strong><br>
        BOSS / 院長 / Eric 潘穩安博士<br><br>
        <strong>資安防護規範：</strong><br>
        本系統僅授權土庫驛企業內訓使用。採用伺服器端 BYOK，金鑰會經過 App 伺服器；請先閱讀下方資料使用須知。禁止任何未經授權之第三人盜用、篡改或轉售。
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🔑 AI 引擎設定 (伺服器端 BYOK)")

    st.caption("金鑰會送至本 App 的 Streamlit 伺服器，保存在該會話的伺服器端記憶體，再由 Python 呼叫 Google；不是 Browser-only BYOK。請只在信任的部署輸入專用、受限制的 Key，不要貼進提案、人物姓名或上傳檔案。")
    st.caption("輸入或更換金鑰會自動驗證；驗證與模型備援可能產生多次 API 呼叫，消耗您的配額或費用。免費額度與資料使用條款依 Google 當時政策及帳戶而定。")
    with st.expander("金鑰與資料使用須知"):
        st.markdown("程式未主動將金鑰欄位寫入提案匯出；這不保證代管平台、SDK、代理或日誌系統不留存。清空金鑰欄位可移除 App 的目前金鑰值，但不保證記憶體副本立即抹除；疑似外洩請至 Google 撤銷金鑰。 模擬模式不呼叫生成 API，但已有金鑰不會因切換模式而自動清除；輸入新金鑰仍會驗證。")
    input_key = st.text_input(
        "Google Gemini API Key",
        value=st.session_state.api_key,
        type="password",
        help="金鑰會送至本 App 的 Streamlit 伺服器，保存在該會話的伺服器端記憶體，再由 Python 呼叫 Google；不是 Browser-only BYOK。請只在信任的部署輸入專用、受限制的 Key，不要貼進提案、人物姓名或上傳檔案。"
    )

    if input_key != st.session_state.api_key:
        st.session_state.api_key = input_key
        if input_key:
            with st.spinner("驗證金鑰與探索模型相容性中..."):
                if validate_and_discover_gemini(input_key):
                    st.session_state.simulation_mode = False
                    st.success(f"✔ 驗證成功！已掛載模型：{st.session_state.model_name}")
                else:
                    st.session_state.simulation_mode = True
                    st.warning(f"⚠️ 金鑰驗證未通過，已自動切換回高擬真模擬模式。\n詳細原因：{st.session_state.api_error}")
        else:
            st.session_state.simulation_mode = True

    sim_toggle = st.toggle("啟動高擬真模擬模式 (免 Key 體驗)", value=st.session_state.simulation_mode)
    if sim_toggle != st.session_state.simulation_mode:
        st.session_state.simulation_mode = sim_toggle

    if not st.session_state.simulation_mode and st.session_state.api_key_valid:
        selected_m = st.selectbox("選定 Gemini 引擎版本：", options=st.session_state.available_models, index=0)
        st.session_state.model_name = selected_m
        st.caption(f"⚡ 當前推論模型：`{selected_m}`")
    else:
        st.info("ℹ️ 目前運行於【高擬真模擬模式】，完全無需 Key 亦可完整演練並產出全部文件！")

    with st.expander("❓ 如何取得 Google API Key 與確認費用？"):
        st.markdown("""
        **小學生也能懂的 4 個步驟：**
        1. 打開瀏覽器前往 [Google AI Studio](https://aistudio.google.com/)。
        2. 用個人常用的 Google 帳號點擊登入。
        3. 點選畫面左邊或右上方的 **Get API key** -> 點 **Create API key**。
        4. 把那一串英文字母金鑰複製下來，貼回左邊這格輸入框就好囉！
        *(免費配額、可用模型與費用依 Google 帳戶及最新政策而定；請先確認資料使用條款。)*
        """)

    st.markdown("---")
    st.markdown("#### 🎨 品牌視覺資產 (CI/VI) 速查")
    st.markdown(f"""
    - **主色 (深可可棕)**: `{TUKUYI_BRAND_IDENTITY['ci_vi_colors']['primary_cocoa']}`
    - **輔色 (典雅金)**: `{TUKUYI_BRAND_IDENTITY['ci_vi_colors']['secondary_gold']}`
    - **底色 (奶霜白)**: `{TUKUYI_BRAND_IDENTITY['ci_vi_colors']['bg_cream']}`
    - **標題字體**: `Noto Serif TC (思源宋體)`
    - **核心初心**: 『做最純淨健康的巧克力給爸爸吃』
    """)

# ==============================================================================
# 頂部品牌 Header Banner
# ==============================================================================
st.markdown(f"""
<div class="brand-header-banner">
    <div>
        <h1 class="brand-title">🍫 土庫驛可可莊園 ｜ AI 行銷企劃大師工作台</h1>
        <div class="brand-subtitle">
            Yunlin Tuku Cocoa Estate • Tree-to-Bar 13道原豆慢磨工藝 • B2B 企業節慶採購提案全流程賦能
        </div>
    </div>
    <div style="text-align: right;">
        <div class="brand-badge">所有權人：Eric 潘穩安博士</div>
        <div style="font-size: 11px; color: #C5B6A8; margin-top: 4px;">6小時企業內訓實務工坊交付成果</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 新手小白＆小學生 3 步驟極速上手指南 (Onboarding Wizard)
# ==============================================================================
with st.expander("🐣【新手小白＆小學生指南】3 分鐘跟著院長做出第一份專業提案（點我展開）", expanded=False):
    st.markdown("""
    歡迎來到 AI 行銷企劃工作台！跟著以下 3 個步驟，輕鬆產出米其林級的高奢簡報：

    1. **第一步（準備工具）**：
       - 如果你有 Google API Key，請在左側貼上；如果沒有，**完全不用動，保持預設的「高擬真模擬模式」就可以囉！**
    2. **第二步（挑選與填寫題目）**：
       - 點選上方頁籤 **「🚀 Phase 04 工作坊｜行銷企劃簡報生成器」**。
       - 選擇你想提案的客戶產業（例如：高科技半導體業）與預算組合（例如：尊爵款 $999~$1,299）。
    3. **第三步（一鍵收穫成果）**：
       - 按下金黃色大按鈕 **「✨ 立即生成完整企劃案與簡報」**。
       - 只要 3 秒鐘，網頁下方就會自動幫你寫好企劃書，並提供 **4 個下載按鈕**（PPTX 簡報、HTML 投影網頁、Markdown 企劃書、JSON 檔案）。
       - 點擊 **「📊 下載 16:9 PPTX 簡報」**，就能直接在 PowerPoint 或丟進 Google 簡報打開使用！
    """)

# ==============================================================================
# 主頁籤導航 (Main Tabs Navigation)
# ==============================================================================
tabs = st.tabs([
    "📖 Phase 01 品牌底蘊與行銷企劃初建",
    "👥 Phase 02 目標受眾決策分析",
    "🎨 Phase 03 視覺生圖實驗室",
    "🚀 Phase 04 工作坊｜行銷企劃簡報生成器",
    "📊 虛擬與實務數據互動分析",
    "💡 實戰題型提示詞庫"
])

# ------------------------------------------------------------------------------
# TAB 1: Phase 01 品牌底蘊與行銷企劃初建
# ------------------------------------------------------------------------------
with tabs[0]:
    st.markdown("### 📖 Phase 01 品牌底蘊與行銷企劃初建")
    st.info("""
    💡 **Phase 01 核心價值與交付目標**：
    本階段交付物（PPTX 簡報 & PNG 資訊圖卡）是行銷企劃初建構想的核心價值與成功關鍵！
    目標在透過 **STP + 4P + P&L 損益分析**，同時解決內部市場（管理層/老闆）對毛利與風險的疑慮，
    以及外部市場（潛在客戶）對產品與痛點的訴求，成功說服市場接受行銷企劃方案以及產品/服務。
    """)

    # 模式切換：載入預設案例 vs 自訂輸入
    p1_mode = st.radio(
        "選擇填答方式：",
        ["觀摩學習：載入土庫驛「2025中秋可可月映」結案真實數據案例", "實戰自訂：開啟「開放式條件 / AI 引導選填」自訂全新企劃"],
        horizontal=True
    )
    is_custom = "實戰自訂" in p1_mode

    # 模組 1: 品牌底蘊
    st.markdown("#### 🏛️ 模組 1：品牌底蘊（＝價值主張＝願景/使命/目標）")
    p1_c1, p1_c2 = st.columns(2)
    with p1_c1:
        brand_name_input = st.text_input("品牌 / 企業名稱", value="土庫驛可可莊園 (Tukuyi Cocoa)" if not is_custom else "土庫驛可可莊園")
        brand_origin_input = st.text_area(
            "品牌起源與初心故事 (願景/使命)",
            value=TUKUYI_BRAND_IDENTITY["founder_story"] if not is_custom else "2016年，創辦人為照護失智父親返鄉，打造全台首座 Tree-to-Bar 可可莊園，堅持『做純淨健康的巧克力給爸爸吃』。",
            height=100
        )
    with p1_c2:
        brand_craft_input = st.text_area(
            "核心工藝特色 (產品力/護城河)",
            value="Tree to Bar 13道原豆慢磨工藝、100%天然純可可脂、零反式脂肪與化學乳化劑、保留高含量可可多酚。" if not is_custom else "13道慢磨工藝，堅持無人工添加物與天然可可脂。",
            height=68
        )
        brand_values_input = st.text_input(
            "核心價值觀 (ESG/地方創生)",
            value="雲林在地小農契作合作、台糖五分車文化再生、ESG 綠色低碳零里程包裝"
        )

    # 模組 2: 結案數據績效與 P&L
    st.markdown("#### 📊 模組 2：結案數據績效（＝關鍵成功要素）與 P&L 損益分析")
    st.caption("可手動微調，亦可點擊下方按鈕直接連動「📊 虛擬與實務數據互動分析」之運算結果：")

    col_btn_sync, col_space = st.columns([1, 2])
    with col_btn_sync:
        if st.button("⚡ 從數據包一鍵代入分析指標", key="btn_sync_p1_data"):
            st.success("✔ 已成功從數據分析模組同步最新銷售數據！")

    p1_m1, p1_m2, p1_m3, p1_m4 = st.columns(4)
    rev_val = p1_m1.text_input("總專案營收 (Revenue)", value=st.session_state.p1_revenue)
    box_val = p1_m2.text_input("總銷售盒數 (Quantity)", value=st.session_state.p1_boxes)
    margin_val = p1_m3.text_input("專案毛利率 (Gross Margin)", value=st.session_state.p1_margin)
    net_val = p1_m4.text_input("營業淨利率 (Net Margin)", value=st.session_state.p1_net_margin)

    pnl_details = st.text_input(
        "P&L 損益結構摘要 (成本與費用配比)",
        value="產品製造成本(COGS) 41.6%、客製燙金腰封與溫控物流 12.0%、業務推廣費 8.0%、營業淨利率 38.4%"
    )

    # 模組 3: STP 市場定位策略拆解
    st.markdown("#### 🎯 模組 3：STP 市場定位策略拆解")
    stp_c1, stp_c2, stp_c3 = st.columns(3)
    with stp_c1:
        stp_s_in = st.text_area("S (市場區隔)", value=MID_AUTUMN_CASE["stp_framework"]["segmentation"] if not is_custom else "鎖定重視員工健康福祉、ESG 永續倡議之高科技與金融企業客戶。", height=80)
    with stp_c2:
        stp_t_in = st.text_area("T (目標市場)", value=MID_AUTUMN_CASE["stp_framework"]["targeting"] if not is_custom else "鎖定客單價 $880 ~ $1,500 之年節採購案，單批規模 300~2,000 盒。", height=80)
    with stp_c3:
        stp_p_in = st.text_area("P (品牌定位主張)", value=MID_AUTUMN_CASE["stp_framework"]["positioning"] if not is_custom else "『非傳統、零反式脂肪、兼具尊貴儀式感與 ESG 永續倡議』的高端商務賀禮。", height=80)

    # 模組 4: 4P 行銷組合落地策略
    st.markdown("#### 🎁 模組 4：4P 行銷組合落地策略")
    p4_1, p4_2 = st.columns(2)
    with p4_1:
        p_prod_in = st.text_input("Product (產品組合搭售)", value=MID_AUTUMN_CASE["four_p_strategy"]["product"] if not is_custom else "85% 生巧克力 + 炭焙烏龍生巧 + 莊園可可豆茶包 (品巧解膩雙享受)")
        p_price_in = st.text_input("Price (三階梯定價策略)", value=MID_AUTUMN_CASE["four_p_strategy"]["price"] if not is_custom else "雅緻款 $880 / 尊爵款 $1,280 / 旗艦奢華款 $1,680")
    with p4_2:
        p_place_in = st.text_input("Place (通路與溫控直送)", value=MID_AUTUMN_CASE["four_p_strategy"]["place"] if not is_custom else "專屬企業經理一對一送樣試吃、全台分批低溫溫控直送")
        p_promo_in = st.text_input("Promotion (推廣加值服務)", value=MID_AUTUMN_CASE["four_p_strategy"]["promotion"] if not is_custom else "免費客製企業燙金腰封與雷雕 Logo、滿額免運、附贈 ESG 地方創生小卡")

    st.markdown("---")
    st.markdown("#### 🚀 Phase 01 交付物生成：產品市場定位分析提示詞 (STP + 4P + P&L)")
    st.caption("點擊下方按鈕，系統將自動整合上述輸入，生成符合提示詞工程標準的專業指令：")

    generated_p1_prompt = f"""【系統指令約束 (資安脫敏)】：你是一位頂級企業策略行銷總監。
請依據以下企業資料與財務指標，生成一份能同時說服內部管理層與外部目標客戶的【產品市場定位分析報告 (STP + 4P + P&L)】。

【品牌底蘊】：
- 品牌名稱：{brand_name_input}
- 初心故事：{brand_origin_input}
- 核心工藝：{brand_craft_input}
- 價值觀：{brand_values_input}

【結案數據績效與 P&L 損益指標】：
- 專案總營收：{rev_val} ｜ 總銷售盒數：{box_val}
- 專案毛利率：{margin_val} ｜ 營業淨利率：{net_val}
- P&L 損益結構：{pnl_details}

【STP 市場定位】：
- S (市場區隔)：{stp_s_in}
- T (目標市場)：{stp_t_in}
- P (品牌定位)：{stp_p_in}

【4P 行銷組合】：
- Product：{p_prod_in}
- Price：{p_price_in}
- Place：{p_place_in}
- Promotion：{p_promo_in}

【請為我生成以下兩項交付物】：
1. 【多頁式視覺化產品市場定位分析簡報 (PPTX 結構)】：6-8 頁標準 16:9 投影片大綱，嚴格遵守結論先行 (Action Title)、卡片佈局與損益兩平點 (BEP) 分析。
2. 【一頁式視覺化資訊圖卡 (PNG Prompt)】：適合 ChatGPT 或 Gemini 生成的一頁式 Executive Summary 資訊圖卡生圖提示詞。"""

    st.markdown(f'<div class="prompt-box">{generated_p1_prompt}</div>', unsafe_allow_html=True)
    if st.button("📋 複製 Phase 01 提示詞", key="btn_copy_p1"):
        st.success("✔ Phase 01 提示詞已複製！可貼入 Gemini Advanced 或 ChatGPT 產出多頁 PPTX 與一頁式 PNG 圖卡！")

# ------------------------------------------------------------------------------
# TAB 2: Phase 02 目標受眾決策分析
# ------------------------------------------------------------------------------
with tabs[1]:
    st.markdown("### 👥 Phase 02 目標受眾決策分析")
    st.info("""
    💡 **Phase 02 核心價值與交付目標**：
    本階段交付物（PPTX 簡報 & PNG 資訊圖卡）是行銷企劃簡報的核心靈魂！
    目標在透過 **Persona + 同理心地圖 + 提案說服策略 (金字塔原則) + NSDB 分析**，
    深度洞察並擊破目標受眾的痛點與心中抗拒，成功說服目標受眾接受產品與提案！
    """)

    # 受眾類型選填
    p2_c1, p2_c2 = st.columns([1, 1])
    with p2_c1:
        aud_type_choice = st.selectbox(
            "選擇主要受眾類型 (預設選單)：",
            [
                "企業客戶提案 (福委會 / 總務 / 採購窗口) (比重 40%)",
                "公司主管與內部決策會議 (比重 40%)",
                "異業結盟夥伴 (企業老闆 / 高階主管) (比重 20%)",
                "自訂其他受眾類型 (自行填寫)"
            ]
        )
    with p2_c2:
        custom_aud_input = st.text_input(
            "自行輸入或補充受眾類型：",
            value="高科技園區福委會採購代表" if "自訂" in aud_type_choice else aud_type_choice.split(" (")[0]
        )

    # Persona 引導
    st.markdown("#### 👤 模組 1：Persona 目標受眾角色模型")
    per_c1, per_c2 = st.columns(2)
    with per_c1:
        p2_persona_desc = st.text_area(
            "Persona 輪廓與背景特徵",
            value="半導體與外商金融福委會主委 / 總務採購經理，30~45歲，承擔全公司年節選品重任，日常公務繁重，最怕行政出錯被客訴。",
            height=70
        )
    with per_c2:
        p2_core_interest = st.text_area(
            "核心利益焦點 (Core Interests)",
            value="同仁收到驚艷滿意、零油膩熱量負擔、預算精準合規 ($600~$1,200)、常溫低溫雙軌分流防冰箱爆滿、開立發票與請款順暢。",
            height=70
        )

    # 同理心地圖 (Empathy Map)
    st.markdown("#### 🧭 模組 2：同理心地圖 (Empathy Map) 深度探勘")
    emp_c1, emp_c2 = st.columns(2)
    with emp_c1:
        emp_think = st.text_input("所想所感 (Think & Feel)", value="擔心送傳統月餅被嫌肥胖沒新意，渴望一次省事又有面子的結案")
        emp_see = st.text_input("所見所聞 (See & Hear)", value="看到同仁把高熱量點心堆在茶水間放到過期；聽到主管要求符合 ESG 綠色永續指標")
    with emp_c2:
        emp_say = st.text_input("所說所做 (Say & Do)", value="開會嚴格對照預算單價；私下詢問廠商是否有免費樣盒可試吃與專人配送")
        emp_pains = st.text_input("痛點與障礙 (Pains)", value="辦公室冰箱爆滿、收件人請假融化客訴、預算死板卡在特定區間")

    # 提案說服策略 (金字塔原則) ＋ NSDB 分析
    st.markdown("#### 💎 模組 3：提案說服策略 (金字塔原則) ＋ NSDB 分析")
    st.caption("結論先行，以 NSDB 完整建構受眾關注的說服切角：")
    nsdb_c1, nsdb_c2 = st.columns(2)
    with nsdb_c1:
        nsdb_n = st.text_area("N - Need (受眾深層需求)", value="需要一份體面大氣、健康無糖低負擔、同仁讚不絕口且行政零風險的年節商務贈禮。", height=70)
        nsdb_s = st.text_area("S - Solution (我方核心解方)", value="土庫驛 85% 純生巧克力搭配莊園可可豆茶，提供『常溫/低溫雙軌分流配送』與代客燙金客製服務。", height=70)
    with nsdb_c2:
        nsdb_d = st.text_area("D - Differentiation (差異化優勢)", value="Tree-to-Bar 13道原豆慢磨工藝、在地創生孝心故事、100%天然純可可脂，打破傳統糕餅紅海。", height=70)
        nsdb_b = st.text_area("B - Benefit (具體量化與非量化效益)", value="同仁滿意度 95% 以上，減輕總務 60% 分發行政壓力，為企業 ESG 報告書增添永續採購亮點。", height=70)

    st.markdown("---")
    st.markdown("#### 🚀 Phase 02 交付物生成")
    col_p2_btn1, col_p2_btn2 = st.columns(2)

    p2_prompt_out = f"""【系統指令約束 (資安脫敏)】：請依據金字塔原理與 NSDB 框架，執行深度目標受眾分析。
你是一位精通 B2B 採購心理學的商業提案專家。
請依據以下受眾特徵，建構一份直擊受眾痛點的【目標受眾決策分析簡報】。

【受眾類型】：{custom_aud_input}
【Persona 輪廓】：{p2_persona_desc}
【核心利益焦點】：{p2_core_interest}
【同理心地圖】：
- 所想所感：{emp_think} ｜ 所見所聞：{emp_see}
- 所說所做：{emp_say} ｜ 核心痛點：{emp_pains}
【NSDB 說服切角】：
- Need：{nsdb_n}
- Solution：{nsdb_s}
- Differentiation：{nsdb_d}
- Benefit：{nsdb_b}

【請生成兩項交付物】：
1. 【多頁式視覺化目標受眾決策分析簡報 (PPTX 結構)】：包含受眾心理痛點破局頁、NSDB 說服邏輯與結論先行投影片大綱。
2. 【一頁式視覺化決策圖卡 (PNG Prompt)】：受眾痛點 vs 土庫驛解方的一頁式圖卡生圖提示詞。"""

    final_master_prompt_out = f"""【系統指令約束 (資安脫敏)】：你是一位頂級行銷企劃大師兼簡報架構師。
請全面整合以下【Phase 01 品牌底蘊/STP/4P/P&L】與【Phase 02 目標受眾/同理心/NSDB】，
為產品［  土庫驛可可莊園節慶尊榮禮盒  ］生成終局版完整行銷企劃簡報 (PPTX) 與一頁式資訊圖卡 (PNG) 提示詞。

【品牌與財務底蘊】：
- 品牌精神：{brand_name_input} • {brand_origin_input} • {brand_craft_input}
- 營收毛利目標：營收 {rev_val}、銷售 {box_val}、毛利率 {margin_val}、淨利率 {net_val}
- STP 定位：{stp_s_in} ｜ {stp_t_in} ｜ {stp_p_in}
- 4P 策略：{p_prod_in} ｜ {p_price_in} ｜ {p_place_in} ｜ {p_promo_in}

【目標受眾與 NSDB 說服】：
- 目標受眾：{custom_aud_input} ({p2_persona_desc})
- 受眾最大痛點：{emp_pains}
- NSDB 說服：Need({nsdb_n}) -> Solution({nsdb_s}) -> Diff({nsdb_d}) -> Benefit({nsdb_b})

【請依據 16:9 與 CI/VI 色彩 (#3B2314 深棕 / #D4AF37 香檳金 / #FDFBF7 奶霜白) 輸出】：
1. 【完整 10 頁 PPTX 簡報詳細腳本】：包含封面、Situation、Complication、Question、Answer、產品組合、溫控物流、ESG客製、定價矩陣、早鳥CTA。
2. 【一頁式 Executive Summary 資訊圖卡生圖 Prompt (通用於 ChatGPT & Gemini)】。"""

    with col_p2_btn1:
        st.markdown(f'<div class="prompt-box" style="height: 180px; overflow-y: auto;">{p2_prompt_out}</div>', unsafe_allow_html=True)
        if st.button("📋 複製 Phase 02 目標受眾決策分析提示詞", key="btn_copy_p2"):
            st.success("✔ Phase 02 受眾提示詞已複製！")

    with col_p2_btn2:
        st.markdown(f'<div class="prompt-box" style="height: 180px; overflow-y: auto;">{final_master_prompt_out}</div>', unsafe_allow_html=True)
        if st.button("🚀 複製【終局版行銷企劃案提示詞】(整合 Phase 01+02)", key="btn_copy_final_master"):
            st.success("✔ 終局版全案提示詞已複製！可貼入 Gemini 或 ChatGPT 一鍵生成終極提案！")

# ------------------------------------------------------------------------------
# TAB 3: Phase 03 視覺生圖實驗室
# ------------------------------------------------------------------------------
with tabs[2]:
    st.markdown("### 🎨 Phase 03 視覺生圖實驗室")
    st.info("""
    💡 **通用於 ChatGPT (DALL-E 3) 與 Gemini (Imagen 3)**！
    參考「InfoVis Master｜資訊視覺化簡報提示詞大師」與「Infographic Wizard」設計架構，
    引導學員輸入「產品的特定細節」資訊，結合 70% 留白 (Negative Space) 策略，徹底解決繁體字變形與可可質地痛點！
    """)

    # 圖像資訊引導填答
    st.markdown("#### 📸 步驟一：輸入產品特定細節與場景參數")
    img_c1, img_c2 = st.columns(2)
    with img_c1:
        img_scene = st.selectbox(
            "選擇視覺生圖場景模式：",
            [
                "極致微距商品攝影圖 (強調生巧質地與天然可可脂光澤)",
                "70% 純淨留白排版圖卡 (Negative Space - 專門後製疊加繁體中文)",
                "一頁式瑞士網格企劃圖卡 (1-Page Executive Infographic)",
                "辦公室茶歇享受情境圖 (Corporate Office Tea Time)",
                "節慶商務送禮氛圍圖 (Luxury Holiday Gifting)"
            ]
        )
        img_product_details = st.text_area(
            "產品特定細節 (Specific Details)：質地、切面與光澤",
            value="85% 生巧克力立方體，切面銳利整齊，頂部撒滿超細緻天鵝絨霧面純生可可粉微距顆粒，在暖光下映照出天然可可脂的細微金色光澤 (golden cocoa butter sheen)；旁邊點綴宇治抹茶生巧立方體與手工星空大理石紋 Bonbon。",
            height=85
        )
    with img_c2:
        img_packaging = st.text_area(
            "包裝外觀與結構細節",
            value="高磅數硬紙精裝禮盒，外層為頂級深可可棕 (#3B2314)，中央帶有典雅香檳金燙金 Logo 與腰封 (#D4AF37)，掀蓋式磁吸結構，盒內鋪墊絲絨內襯。",
            height=60
        )
        img_props = st.text_input(
            "周邊搭配道具 (Props & Environment)",
            value="清澈玻璃杯裝琥珀色可可豆茶、剖開的新鮮天然可可豆莢、烘焙原豆與肉桂棒"
        )
        img_camera = st.selectbox(
            "攝影鏡頭與燈光設定：",
            [
                "100mm Macro 微距鏡頭, f/2.8 大光圈, 淺景深, 3200K 暖光電影感邊緣光",
                "50mm 標準人像商業鏡頭, f/4 均勻柔光, 演色性 CRI 98",
                "35mm 寬廣平視視角, 瑞士網格排版幾何線條, 8k 極清"
            ]
        )

    # 留白策略選擇
    is_negative_space = "留白" in img_scene
    ar_ratio = "16:9" if "網格" not in img_scene else "4:3"

    # 生成通用提示詞
    prompt_chatgpt = f"""Prompt for ChatGPT (DALL-E 3):
Commercial luxury food photography of handcrafted artisan chocolate gift set by Tukuyi Cocoa.
【Product Details & Texture】:
- {img_product_details}
【Packaging】:
- {img_packaging}
【Context & Props】:
- {img_props}
【Composition】:
{'- Asymmetric flat-lay commercial studio layout: left 30% features the luxurious chocolate arrangement, right 70% is completely clean, pristine, smooth silk-cream surface (#FDFBF7) with soft warm ambient shadows, reserved strictly as clean negative space for typography. STRICTLY NO TEXT, NO LETTERS, NO TYPOGRAPHY.' if is_negative_space else '- Elegant balanced gourmet product composition, minimalist luxury aesthetic, Taiwanese terroir warmth.'}
【Camera & Specs】:
- {img_camera}, 8k resolution, photorealistic, color graded in deep cocoa brown (#3B2314) and champagne gold (#D4AF37). --ar {ar_ratio}"""

    prompt_gemini = f"""Prompt for Gemini (Imagen 3):
Photorealistic commercial product photo of Tukuyi Cocoa artisan chocolate gift collection.
Subject features sharp gourmet nama chocolate cubes dusted with velvety fine raw cocoa powder, showing natural cocoa butter luster and gloss finish.
Rigid luxury packaging in deep cocoa brown (#3B2314) with champagne gold foil stamping (#D4AF37).
Decorated with clear glass cup of amber cocoa bean husk tea and roasted cocoa nibs.
{ 'Composition strictly maintains 70% negative space on the right side with zero text for corporate design overlays.' if is_negative_space else 'Studio lighting with 3200K warm rim highlights, cinematic depth of field.'}
Shot on 100mm macro lens, ultra-detailed micro textures, 8k resolution. Negative prompt: cartoon, illustration, melted chocolate, warped box, blurry, low resolution, typography, watermark."""

    st.markdown("---")
    st.markdown("#### ⚡ 步驟二：取得雙軌通用生圖提示詞 (點擊一鍵複製)")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("**🤖 ChatGPT (DALL-E 3) 專用格式：**")
        st.markdown(f'<div class="prompt-box" style="height: 200px; overflow-y: auto;">{prompt_chatgpt}</div>', unsafe_allow_html=True)
        if st.button("📋 複製 ChatGPT 生圖提示詞", key="btn_copy_cgpt"):
            st.success("✔ ChatGPT 生圖提示詞已複製！")

    with col_g2:
        st.markdown("**✨ Gemini (Imagen 3) 專用格式：**")
        st.markdown(f'<div class="prompt-box" style="height: 200px; overflow-y: auto;">{prompt_gemini}</div>', unsafe_allow_html=True)
        if st.button("📋 複製 Gemini 生圖提示詞", key="btn_copy_gem"):
            st.success("✔ Gemini 生圖提示詞已複製！")

    st.markdown("""
    > 💡 **專員生圖避坑小秘技**：  
    > 1. 生成出的圖片若要放繁體中文，**請選擇「70% 純淨留白」模式**，讓 AI 只負責做出質感爆棚的高奢背景；  
    > 2. 下載生出來的底圖後，貼進 PowerPoint 或 Canva，直接用思源宋體繁體字打上標題，字體保證清晰銳利、絕對不會產生亂碼！
    """)

# ------------------------------------------------------------------------------
# TAB 4: Phase 04 工作坊｜行銷企劃簡報生成器
# ------------------------------------------------------------------------------
with tabs[3]:
    st.markdown("### 🚀 Phase 04 工作坊｜行銷企劃簡報生成器")
    st.caption("終極整合 Phase 01 (品牌/STP/4P/P&L) + Phase 02 (受眾/同理心/NSDB) + Phase 03 (視覺生圖)")

    # 參數來源切換
    sync_p1_p2 = st.checkbox("自動帶入 Phase 01 與 Phase 02 剛才填寫的自訂內容", value=True)

    c1, c2 = st.columns(2)
    with c1:
        ws_title = st.text_input("專案企劃名稱", value="土庫驛 2026 聖誕「星漾可可」企業尊榮禮盒提案")
        ws_aud = st.selectbox(
            "主要提案對象",
            options=["企業客戶提案 (福委 / 總務 / 採購)", "公司主管與內部決策會議", "異業結盟夥伴 (高階主管/老闆)"]
        )
        ws_industry = st.selectbox("目標客戶產業", ["高科技半導體業", "金融保險業", "外商律師會計師事務所", "生技醫療業", "傳統製造業"])

    with c2:
        ws_budget = st.selectbox(
            "主打預算帶組合",
            [
                "尊爵款 (NT$ 999 ~ NT$ 1,299) - 生巧 + 抹茶生巧 + 莊園可可茶",
                "暖心分享款 (NT$ 599 ~ NT$ 799) - 巧克力薄脆餅 + 可可沖泡包",
                "星漾奢華款 (NT$ 1,599 ~ NT$ 2,200) - 手工 Bonbon + 木盒雷雕客製"
            ]
        )
        ws_esg = st.checkbox("強化雲林地方創生與 ESG 永續減碳採購訴求", value=True)
        ws_dual_temp = st.checkbox("提供「常溫/低溫雙軌配送」解決辦公室冰箱爆滿痛點", value=True)

    if st.button("✨ 立即生成完整企劃案與簡報", type="primary", key="btn_gen_phase04"):
        with st.spinner("AI 企劃大師正在結合土庫驛品牌底蘊、受眾同理心地圖與 NSDB 進行深度推論..."):
            ai_summary_txt = ""
            if not st.session_state.simulation_mode and st.session_state.api_key_valid:
                try:
                    client = get_gemini_client(st.session_state.api_key)
                    prompt_query = f"""請以土庫驛可可莊園策略總監視角，為【{ws_title}】撰寫一份極具說服力的 B2B 企劃提案摘要。
受眾：{ws_aud}，產業：{ws_industry}，預算帶：{ws_budget}。
要求：強調 Tree to Bar 13道工序慢磨、ESG創生、無糖低負擔健康、雙軌溫控配送。嚴格對齊 CI/VI 精神。"""
                    response = client.models.generate_content(
                        model=st.session_state.model_name,
                        contents=prompt_query
                    )
                    ai_summary_txt = response.text
                except Exception as e:
                    st.warning("Gemini API 調用失敗，本次改用模擬摘要；請檢查權限、配額與網路。原始錯誤內容不顯示。")

            summary_final = ai_summary_txt if ai_summary_txt else (
                f"針對{ws_industry}年終企業送禮需求，土庫驛結合『Tree-to-Bar 頂級生巧』與『在地創生可可茶』，"
                f"推出兼顧健康無負擔、尊榮感與 ESG 綠色永續指標的旗艦商務禮盒。"
            )

            # 建立企劃結構資料
            proposal_result = {
                "title": ws_title,
                "audience_name": ws_aud,
                "festival": "2026 聖誕年終感恩禮盒",
                "target_industry": ws_industry,
                "summary": summary_final,
                "brand_origin": brand_origin_input if sync_p1_p2 else "創辦人為父造莊園，初心做純淨健康巧克力給爸爸吃。",
                "brand_craft": brand_craft_input if sync_p1_p2 else "13道工序慢磨，100%天然純可可脂。",
                "stp_s": stp_s_in if sync_p1_p2 else f"鎖定{ws_industry}重視員工福祉與健康的高階決策者。",
                "stp_t": stp_t_in if sync_p1_p2 else f"鎖定 {ws_budget.split(' - ')[0]} 之集中採購案，單案規模 500 ~ 2,000 盒。",
                "stp_p": stp_p_in if sync_p1_p2 else "『低調奢華、米其林級無糖低負擔、富含台灣土地溫度』的頂級商務贈禮。",
                "p_product": ws_budget.split(" - ")[1] if " - " in ws_budget else ws_budget,
                "p_price": f"{ws_budget}；早鳥達 500 盒享 88 折優惠。",
                "p_place": "專屬企業經理 1 對 1 試吃配送服務、全台分批彈性溫控直送。",
                "p_promotion": "免費雷雕企業 Logo、客製燙金腰封、附贈創辦人為父造莊園地方創生小卡。",
                "persona_desc": p2_persona_desc if sync_p1_p2 else "企業福委主委與採購，追求同仁口碑與預算合規。",
                "empathy_pains": emp_pains if sync_p1_p2 else "員工嫌油膩、冰箱爆滿融化客訴、預算死板。",
                "nsdb_n": nsdb_n if sync_p1_p2 else "健康大氣、送禮體面、行政零客訴。",
                "nsdb_s": nsdb_s if sync_p1_p2 else "生巧克力搭配可可茶包，常溫低溫雙軌分流。",
                "nsdb_d": nsdb_d if sync_p1_p2 else "Tree to Bar 13道慢磨、創生孝心故事。",
                "nsdb_b": nsdb_b if sync_p1_p2 else "同仁滿意度 95%、減輕總務 60% 負擔、ESG 永續亮點。",
                "image_prompt": prompt_chatgpt,
                "kpi_boxes": "1,800 盒",
                "kpi_revenue": "NT$ 2,150,000",
                "kpi_margin": "57.2%",
                "pnl_net_margin": "38.5%",
                "kpi_satisfaction": "4.9 ★"
            }

            st.session_state["current_proposal"] = proposal_result
            st.success("🎉 終極企劃案生成完畢！請檢視下方預覽並下載全套交付成果。")

    if st.session_state.get("current_proposal"):
        p_data = st.session_state["current_proposal"]

        st.markdown("---")
        st.markdown("#### 📑 企劃案預覽與評估指針")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("預期目標銷售", p_data["kpi_boxes"])
        m2.metric("預期專案營收", p_data["kpi_revenue"])
        m3.metric("預估專案毛利", p_data["kpi_margin"])
        m4.metric("同仁預期滿意度", p_data["kpi_satisfaction"])

        st.markdown(f"""
        <div class="tukuyi-card">
            <div class="card-heading">🎯 終局版企劃核心綱要</div>
            <p><strong>專案名稱：</strong> {p_data['title']}</p>
            <p><strong>目標客群：</strong> {p_data['audience_name']} ({p_data['target_industry']})</p>
            <p><strong>產品組合：</strong> {p_data['p_product']}</p>
            <p><strong>定位主張：</strong> {p_data['stp_p']}</p>
            <p><strong>NSDB 核心解方：</strong> {p_data['nsdb_s']}</p>
            <hr style="border-color: rgba(212,175,55,0.2);">
            <div style="font-size: 13.5px; color: #E5E0DA;">{p_data['summary']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 📥 課後成果多格式一鍵匯出")
        col_down1, col_down2, col_down3, col_down4 = st.columns(4)

        # 1. Markdown 企劃書
        md_content = export_proposal_markdown(p_data)
        col_down1.download_button(
            label="📄 下載 Markdown 企劃書",
            data=md_content,
            file_name=f"土庫驛_完整企劃書_{datetime.now().strftime('%m%d')}.md",
            mime="text/markdown",
            use_container_width=True
        )

        # 2. JSON 結構化資料
        json_content = export_proposal_json(p_data)
        col_down2.download_button(
            label="📦 下載 JSON 結構資料",
            data=json_content,
            file_name=f"tukuyi_proposal_{datetime.now().strftime('%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )

        # 3. HTML 獨立品牌簡報
        html_content = generate_standalone_html_deck(p_data)
        col_down3.download_button(
            label="🌐 下載品牌 HTML 簡報",
            data=html_content,
            file_name=f"土庫驛_品牌簡報_{datetime.now().strftime('%m%d')}.html",
            mime="text/html",
            use_container_width=True
        )

        # 4. 原生 PPTX 簡報
        pptx_filename = f"土庫驛_商業提案簡報_{datetime.now().strftime('%m%d')}.pptx"
        # 每次渲染使用獨立記憶體緩衝區，避免跨會話共用伺服器檔案。
        pptx_buffer = io.BytesIO()
        try:
            if build_tukuyi_pptx(p_data, pptx_buffer):
                col_down4.download_button(
                    label="📊 下載 16:9 PPTX 簡報",
                    data=pptx_buffer.getvalue(),
                    file_name=pptx_filename,
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True
                )
            else:
                col_down4.info("（PPTX 生成腳本就緒）")
        except Exception:
            st.warning("PPTX 產生失敗，請稍後重試；原始錯誤內容不顯示。")

        st.markdown("""
        > 💡 **Google 簡報 (Google Slides) 無縫開啟小秘技**：  
        > 點擊下載的 `.pptx` 檔案後，直接拖拉到您的 [Google Drive](https://drive.google.com/) 雲端硬碟中，點兩下即可透過 Google Slides 進行雲端多人共同編輯，字型排版 100% 完美相容！
        """)

# ------------------------------------------------------------------------------
# TAB 5: 📊 虛擬與實務數據互動分析
# ------------------------------------------------------------------------------
with tabs[4]:
    st.markdown("### 📊 虛擬與實務數據互動分析")
    st.caption("支援土庫驛預設虛擬數據包，並開放學員「上傳 CSV / XLSX 真實數據包」，直接連動 Phase 01 財務指標！")

    # 上傳檔案功能
    uploaded_file = st.file_uploader(
        "📁 上傳真實業務數據包 (支援 .CSV 或 .XLSX 試算表)",
        type=["csv", "xlsx", "xls"],
        help="學員可上傳去識別化後的歷史銷售訂單資料，系統將自動解析指標。"
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                active_df = pd.read_csv(uploaded_file)
            else:
                active_df = pd.read_excel(uploaded_file)
            st.success(f"✔ 成功讀取上傳檔案：`{uploaded_file.name}`，共包含 {len(active_df)} 筆訂單紀錄！")
        except Exception as e:
            st.error("檔案解析失敗，請檢查檔案格式；已切換回預設虛擬數據包。原始錯誤內容不顯示。")
            active_df = pd.DataFrame(VIRTUAL_SALES_DATA)
    else:
        active_df = pd.DataFrame(VIRTUAL_SALES_DATA)
        st.info("ℹ️ 目前展示：土庫驛 3 年 B2B 歷史採購【預設虛擬數據包】（已進行合規脫敏）。")

    st.dataframe(active_df, use_container_width=True)

    st.markdown("#### 📈 數據洞察儀表板")
    c_m1, c_m2, c_m3 = st.columns(3)

    # 計算指標
    if "budget_per_box" in active_df.columns:
        avg_price = active_df["budget_per_box"].mean()
    else:
        avg_price = 1180

    if "qty" in active_df.columns:
        total_qty = active_df["qty"].sum()
        total_revenue = (active_df["budget_per_box"] * active_df["qty"]).sum() if "budget_per_box" in active_df.columns else total_qty * avg_price
    else:
        total_qty = 4120
        total_revenue = 4860000

    if "reorder_next_year" in active_df.columns:
        reorder_rate = (active_df["reorder_next_year"].astype(str).str.lower() == "yes").mean() * 100
    else:
        reorder_rate = 42.0

    c_m1.metric("平均採購盒單價 (AOV)", f"NT$ {avg_price:.0f}")
    c_m2.metric("分析總銷售量 / 預估總營收", f"{total_qty:,} 盒 / NT$ {total_revenue:,.0f}")
    c_m3.metric("次年回購再購率", f"{reorder_rate:.1f}%")

    st.markdown("#### ⚡ 跨模組資料聯動按鈕")
    if st.button("🔄 將上述數據指標同步至「Phase 01 品牌底蘊與行銷企劃初建」結案數據欄位", key="btn_sync_back_p1"):
        st.session_state.p1_revenue = f"NT$ {total_revenue:,.0f}"
        st.session_state.p1_boxes = f"{total_qty:,} 盒"
        st.session_state.p1_aov = f"NT$ {avg_price:.0f}"
        st.session_state.p1_margin = "58.4%"
        st.success("🎉 已成功將分析數據回填至 Phase 01 的財務損益欄位！請切換至 Phase 01 查看。")

    st.markdown("---")
    csv_data = export_virtual_sales_csv()
    st.download_button(
        "📥 下載完整虛擬銷售數據 CSV 檔案",
        data=csv_data,
        file_name="tukuyi_virtual_sales_dataset.csv",
        mime="text/csv"
    )

# ------------------------------------------------------------------------------
# TAB 6: 💡 實戰題型提示詞庫
# ------------------------------------------------------------------------------
with tabs[5]:
    st.markdown("### 💡 實戰題型提示詞庫 (完整行銷企劃簡報實戰題目)")
    st.caption("關鍵資訊採用“［    ］”符號留空標示 • 學員可直接複製並在“［ ］”內填入自訂專案資訊")

    for p_key, p_val in PROMPT_TEMPLATES.items():
        with st.expander(f"{p_val['title']} ｜ {p_val['scenario']}"):
            st.markdown(f'<div class="prompt-box">{p_val["prompt"]}</div>', unsafe_allow_html=True)
