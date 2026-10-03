"""
土庫驛可可莊園 (Tukuyi Cocoa) - AI 行銷企劃大師 Web App (v2.0.0 Enterprise)
==============================================================================
所有權人 / 著作權人：BOSS、院長、Eric 潘穩安博士 (Dr. Eric Wen-An Pan)
核心架構：BYOK (Google Gemini API) 零成本部署、防篡改資安機制、動態模型容錯、
土庫驛 CI/VI 視覺底層約束、3大受眾痛點適配、ChatGPT Images 2.5 視覺實驗室與多格式一鍵導出。
==============================================================================
"""

import os
import json
import streamlit as st
import pandas as pd
from datetime import datetime

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
# Session State 初始化與 Gemini 客戶端架構 (參考 Persona Designer 成熟機制)
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
    "current_proposal": None
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
        st.session_state.api_error = f"GenAI SDK 初始化失敗: {str(e)}"
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

    # 策略 1: 動態枚舉可用模型
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

    # 策略 2: PING 測試模型相容性
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
            st.session_state.api_error = str(e)
            continue

    st.session_state.api_key_valid = False
    return False

# ==============================================================================
# 側邊欄 (Sidebar) - 著作權、BYOK 認證與品牌資產速查
# ==============================================================================
with st.sidebar:
    st.markdown("### 🍫 土庫驛可可莊園")
    st.markdown("**AI 行銷企劃大師工作台 v2.0**")
    st.caption("企業專屬內訓交付 • 課後永久帶走實用工具")

    st.markdown("---")
    st.markdown("#### ⚖️ 系統所有權與智財權宣告")
    st.markdown(f"""
    <div style="font-size: 11.5px; color: #BBB; background: rgba(212,175,55,0.08); border-left: 3px solid #D4AF37; padding: 8px 10px; border-radius: 4px; margin-bottom: 12px;">
        <strong>所有權人 / 著作權人：</strong><br>
        BOSS / 院長 / Eric 潘穩安博士<br><br>
        <strong>資安防護規範：</strong><br>
        本系統僅授權土庫驛企業內訓使用。採用純客戶端 BYOK 隔離架構，API Key 絕不落地存檔，禁止任何未經授權之第三人盜用、篡改或轉售。
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🔑 AI 引擎設定 (BYOK 零成本)")

    input_key = st.text_input(
        "Google Gemini API Key",
        value=st.session_state.api_key,
        type="password",
        help="依循 BYOK 原則，至 Google AI Studio 免費申請 API Key（免費額度充裕，企業 0 元維運成本）。"
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

    with st.expander("❓ 新手如何取得 0 元免費 Google API Key？"):
        st.markdown("""
        **小學生也能懂的 4 個步驟：**
        1. 打開瀏覽器前往 [Google AI Studio](https://aistudio.google.com/)。
        2. 用個人常用的 Google 帳號點擊登入。
        3. 點選畫面左邊或右上方的 **Get API key** -> 點 **Create API key**。
        4. 把那一串英文字母金鑰複製下來，貼回左邊這格輸入框就好囉！
        *(完全免費，每分鐘有 15 次調用額度，不用綁信用卡)*
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
        <div style="font-size: 11px; color: #C5B6A8; margin-top: 4px;">6小時企業內訓實務工坊成果</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 新手小白＆小學生 3 步驟極速上手指南 (Onboarding Wizard)
# ==============================================================================
with st.expander("🐣【新手小白＆小學生指南】3 分鐘跟著院長做出第一份專業提案（點我展開）", expanded=False):
    st.markdown("""
    歡迎來到 AI 行銷企劃工作台！別擔心，跟著以下 3 個步驟，小學生也能產出米其林級的高奢簡報：

    1. **第一步（準備工具）**：
       - 如果你有 Google API Key，請在左側貼上；如果沒有，**完全不用動，保持預設的「高擬真模擬模式」就可以囉！**
    2. **第二步（挑選與填寫題目）**：
       - 點選上方頁籤 **「🚀 CH05 聖誕禮盒企劃生成器」**。
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
    "📖 CH01 品牌底蘊與中秋教學案例",
    "👥 CH02 3大受眾決策分析",
    "🎨 CH03 視覺生圖實驗室",
    "🚀 CH05 聖誕禮盒企劃生成器",
    "📊 虛擬數據包互動分析",
    "💡 6大實戰題型提示詞庫"
])

# ------------------------------------------------------------------------------
# TAB 1: 品牌底蘊與中秋教學案例 (CH01 基礎理論與已知實例)
# ------------------------------------------------------------------------------
with tabs[0]:
    st.markdown("### 🏛️ 土庫驛品牌核心故事與已知教學案例")
    st.info("💡 **教學指引**：透過已結案的中秋節真實專案，讓學員理解 STP、4P 與 5W2H 如何轉化為具體的 B2B 商業成果。")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""
        <div class="tukuyi-card">
            <div class="card-heading">🌱 莊園創生與品牌初心</div>
            <p style="font-size: 14px; line-height: 1.6; color: #DDD;">
                {TUKUYI_BRAND_IDENTITY['founder_story']}
            </p>
            <hr style="border-color: rgba(212,175,55,0.2);">
            <div style="font-weight: 700; color: #D4AF37; margin-bottom: 6px;">四大核心承諾：</div>
            <ul style="font-size: 13.5px; color: #CCC; padding-left: 20px;">
                {''.join(f'<li>{v}</li>' for v in TUKUYI_BRAND_IDENTITY['core_values'])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="tukuyi-card">
            <div class="card-heading">🥮 2025 中秋「可可月映」結案數據績效</div>
            <div class="metric-container">
                <div class="metric-card">
                    <div class="metric-num">{MID_AUTUMN_CASE['actual_performance_summary']['total_revenue']}</div>
                    <div class="metric-text">總專案營收</div>
                </div>
                <div class="metric-card">
                    <div class="metric-num">{MID_AUTUMN_CASE['actual_performance_summary']['total_boxes_sold']}</div>
                    <div class="metric-text">總銷售盒數</div>
                </div>
                <div class="metric-card">
                    <div class="metric-num">{MID_AUTUMN_CASE['actual_performance_summary']['gross_margin']}</div>
                    <div class="metric-text">專案毛利率</div>
                </div>
            </div>
            <p style="font-size: 13.5px; color: #E0D7CD; margin-top: 10px;">
                <strong>💡 關鍵成功要素：</strong> {MID_AUTUMN_CASE['actual_performance_summary']['key_success_factor']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 🔍 中秋案例 STP 與 4P 實戰架構拆解")
    st_col1, st_col2 = st.columns(2)
    with st_col1:
        with st.expander("🎯 STP 市場定位策略拆解", expanded=True):
            st.markdown(f"""
            - **S (市場區隔)**：{MID_AUTUMN_CASE['stp_framework']['segmentation']}
            - **T (目標市場)**：{MID_AUTUMN_CASE['stp_framework']['targeting']}
            - **P (品牌定位)**：{MID_AUTUMN_CASE['stp_framework']['positioning']}
            """)
    with st_col2:
        with st.expander("🎁 4P 行銷組合落地策略", expanded=True):
            st.markdown(f"""
            - **Product (產品)**：{MID_AUTUMN_CASE['four_p_strategy']['product']}
            - **Price (定價)**：{MID_AUTUMN_CASE['four_p_strategy']['price']}
            - **Place (通路)**：{MID_AUTUMN_CASE['four_p_strategy']['place']}
            - **Promotion (推廣)**：{MID_AUTUMN_CASE['four_p_strategy']['promotion']}
            """)

# ------------------------------------------------------------------------------
# TAB 2: 3 大受眾決策分析 (CH02 簡報方法論與受眾切換)
# ------------------------------------------------------------------------------
with tabs[1]:
    st.markdown("### 👥 簡報場景與 3 大受眾心理決策矩陣")
    st.caption("根據土庫驛真實提案比重：40% 內部主管、40% 福委與採購、20% 異業老闆高階")

    selected_audience_key = st.radio(
        "選擇目標簡報對象：",
        options=list(AUDIENCE_PERSONAS.keys()),
        format_func=lambda x: f"{AUDIENCE_PERSONAS[x]['title']} (比重 {AUDIENCE_PERSONAS[x]['ratio']})"
    )

    aud = AUDIENCE_PERSONAS[selected_audience_key]

    st.markdown(f"""
    <div class="tukuyi-card">
        <div class="card-heading">🎯 {aud['title']} 核心關注與說服切角</div>
        <p style="font-size: 15px; color: #F3E5AB;"><strong>核心利益焦點：</strong> {aud['core_interest']}</p>
        <div style="margin: 12px 0;">
            <strong style="color: #FFB3B3;">⚠️ 他們最大的抗拒與心中痛點：</strong>
            <ul style="color: #DDD; font-size: 14px; margin-top: 6px;">
                {''.join(f'<li>{p}</li>' for p in aud['pain_points'])}
            </ul>
        </div>
        <p style="font-size: 14px; color: #D4AF37;"><strong>💡 提案說服策略 (金字塔原則)：</strong> {aud['persuasion_strategy']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### ⚡ 一案三轉提示詞生成")
    st.markdown("點選下方按鈕，自動產生將相同產品轉換為該受眾專屬說服邏輯的 AI 提示詞：")

    sample_prompt = PROMPT_TEMPLATES["ch02_q1_mid_autumn_switch"]["prompt"]

    st.markdown(f'<div class="prompt-box">{sample_prompt}</div>', unsafe_allow_html=True)
    if st.button("📋 複製此受眾提示詞", key="btn_copy_aud"):
        st.success("提示詞已備妥，可直接貼入 Gemini Advanced 或 ChatGPT Plus 進行推論！")

# ------------------------------------------------------------------------------
# TAB 3: 視覺與生圖實驗室 (CH03 ChatGPT Images 2.5 專題)
# ------------------------------------------------------------------------------
with tabs[2]:
    st.markdown("### 🎨 視覺生圖實驗室 (ChatGPT Images 2.5 實戰)")
    st.info("💡 **行銷專員必備技能**：30分鐘生圖教學 + 30分鐘實作演練。掌握 CI/VI 約束、可可粉微距質感、留白排版與防文字變形。")

    vis_mode = st.selectbox(
        "選擇視覺生圖場景：",
        [
            "場景 1：可可粉微距與生巧光澤商品攝影圖 (解決粉末與光澤痛點)",
            "場景 2：乾淨留白排版圖卡 (Negative Space - 解決繁體字變形痛點)",
            "場景 3：一頁式企劃資訊圖卡 (1-Page Infographic Poster)"
        ]
    )

    if "微距" in vis_mode:
        prompt_text = PROMPT_TEMPLATES["ch03_q1_cocoa_macro"]["prompt"]
        explanation = "特點：鎖定 100mm 微距鏡頭 (Macro)、銳利邊緣、可可脂光澤 (Butter Sheen) 與天鵝絨霧面可可粉，杜絕融化或模糊。"
    elif "留白" in vis_mode:
        prompt_text = PROMPT_TEMPLATES["ch03_q2_negative_space"]["prompt"]
        explanation = "特點：【專員救星】AI 生圖常出現繁體字亂碼變形。本提示詞強制 70% 畫面完全留白 (NO TEXT)，生出高奢底圖後，再用 PPTX 或 Canva 疊加清晰繁體中文字！"
    else:
        prompt_text = PROMPT_TEMPLATES["ch03_q3_infographic_exec"]["prompt"]
        explanation = "特點：對齊瑞士平面設計網格，劃分頂部標題、三大禮盒階梯、四大價值柱與底部採購流程。"

    st.markdown(f"""
    <div class="tukuyi-card">
        <div class="card-heading">📸 生圖提示詞參數解析</div>
        <p style="font-size: 14px; color: #DDD;">{explanation}</p>
        <div class="prompt-box">{prompt_text}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 📐 品牌 CI/VI 底層約束規則 (可作為 GPTs 或 Gemini System Prompt)")
    ci_rule_text = f"""【系統底層約束】：
你必須嚴格遵守「土庫驛可可莊園 (Tukuyi Cocoa)」品牌識別指南：
- 主色：深可可棕 #3B2314
- 輔色：典雅香檳金 #D4AF37
- 背景底色：絲滑奶霜白 #FDFBF7
- 標題字型：思源宋體 (Noto Serif TC)
- 內文字型：思源黑體 (Noto Sans TC)
- 核心精神：Tree-to-Bar 13道工序原豆慢磨，無添加化學乳化劑。"""
    st.markdown(f'<div class="prompt-box">{ci_rule_text}</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 4: 聖誕禮盒企劃生成器 (CH05 工作坊演練與成果產出)
# ------------------------------------------------------------------------------
with tabs[3]:
    st.markdown("### 🚀 CH05 工作坊：2026 聖誕「星漾可可」B2B 企劃生成器")
    st.caption("學員團隊分工演練：策略發想 -> AI 企劃生成 -> 多格式一鍵匯出")

    # 輸入表單
    c1, c2 = st.columns(2)
    with c1:
        workshop_title = st.text_input("企劃案名稱", value="土庫驛 2026 聖誕「星漾可可」企業尊榮禮盒提案")
        workshop_audience = st.selectbox(
            "主要提案對象",
            options=["企業客戶提案 (福委 / 總務 / 採購)", "公司主管與內部決策會議", "異業結盟夥伴 (高階主管/老闆)"]
        )
        target_industry = st.selectbox("目標客戶產業", ["高科技半導體業", "金融保險業", "外商律師會計師事務所", "生技醫療業", "傳統製造業"])

    with c2:
        budget_tier = st.selectbox(
            "主打預算帶組合",
            [
                "尊爵款 (NT$ 999 ~ NT$ 1,299) - 生巧 + 抹茶生巧 + 莊園可可茶",
                "暖心分享款 (NT$ 599 ~ NT$ 799) - 巧克力薄脆餅 + 可可沖泡包",
                "星漾奢華款 (NT$ 1,599 ~ NT$ 2,200) - 手工 Bonbon + 木盒雷雕客製"
            ]
        )
        custom_esg = st.checkbox("強化雲林地方創生與 ESG 永續減碳採購訴求", value=True)
        dual_temperature = st.checkbox("提供「常溫/低溫雙軌配送」解決辦公室冰箱爆滿痛點", value=True)

    if st.button("✨ 立即生成完整企劃案與簡報", type="primary"):
        with st.spinner("AI 企劃大師正在結合土庫驛品牌底蘊與受眾心理進行深度推論..."):
            ai_generated_text = ""
            # 如果具備已驗證的 API Key 且非模擬模式，調用真實 Gemini Client
            if not st.session_state.simulation_mode and st.session_state.api_key_valid:
                try:
                    client = get_gemini_client(st.session_state.api_key)
                    prompt_query = f"""請以土庫驛可可莊園資深策略總監視角，為【{workshop_title}】撰寫一份極具說服力的 B2B 企劃提案摘要。
受眾：{workshop_audience}，目標產業：{target_industry}，預算帶：{budget_tier}。
要求：強調 Tree to Bar 13道工序慢磨、ESG創生、無糖低負擔健康、雙軌溫控配送。嚴格對齊 CI/VI 精神。"""
                    response = client.models.generate_content(
                        model=st.session_state.model_name,
                        contents=prompt_query
                    )
                    ai_generated_text = response.text
                except Exception as e:
                    st.warning(f"Gemini API 調用異常 ({str(e)})，已平滑切換至高擬真模擬模式！")

            summary_final = ai_generated_text if ai_generated_text else (
                f"針對{target_industry}年終企業送禮需求，土庫驛結合『Tree-to-Bar 頂級生巧』與『在地創生可可茶』，"
                f"推出兼顧健康無負擔、尊榮感與 ESG 綠色永續指標的旗艦商務禮盒。"
            )

            # 建立企劃結構資料
            proposal_result = {
                "title": workshop_title,
                "audience_name": workshop_audience,
                "festival": "2026 聖誕年終感恩禮盒",
                "target_industry": target_industry,
                "summary": summary_final,
                "stp_s": f"鎖定{target_industry}中高階主管、重視生活質感與員工健康福祉之採購單位。",
                "stp_t": f"鎖定 {budget_tier.split(' - ')[0]} 之集中採購案，單案採購規模 500 ~ 2,000 盒。",
                "stp_p": "『低調奢華、米其林級無糖低負擔、富含台灣土地溫度』的頂級商務贈禮。",
                "p_product": f"核心配置：{budget_tier.split(' - ')[1]}，搭配聖誕深可可棕與香檳金緞帶包裝。",
                "p_price": f"{budget_tier}；早鳥達 500 盒享 88 折優惠。",
                "p_place": "專屬企業經理 1 對 1 試吃配送服務、全台分批彈性溫控直送。",
                "p_promotion": "免費雷雕企業 Logo、客製燙金腰封、附贈創辦人為父造莊園地方創生小卡。",
                "audience_pitch": (
                    "福委長官有面子、同仁零熱量負擔、總務配送零客訴；"
                    "提供常溫/低溫雙軌彈性，免除同仁家中或公司冰箱容量不足之痛點。"
                ),
                "image_prompt": PROMPT_TEMPLATES["ch03_q1_cocoa_macro"]["prompt"],
                "kpi_boxes": "1,800 盒",
                "kpi_revenue": "NT$ 2,150,000",
                "kpi_margin": "57.2%",
                "kpi_satisfaction": "4.9 ★"
            }

            st.session_state["current_proposal"] = proposal_result
            st.success("🎉 企劃案生成完畢！請檢視下方預覽並下載成果。")

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
            <div class="card-heading">🎯 企劃核心綱要</div>
            <p><strong>專案名稱：</strong> {p_data['title']}</p>
            <p><strong>目標客群：</strong> {p_data['audience_name']} ({p_data['target_industry']})</p>
            <p><strong>核心產品：</strong> {p_data['p_product']}</p>
            <p><strong>定位主張：</strong> {p_data['stp_p']}</p>
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
            file_name=f"土庫驛_聖誕企劃書_{datetime.now().strftime('%m%d')}.md",
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
        pptx_filepath = os.path.join(os.path.dirname(__file__), "output_proposal.pptx")
        
        # 生成 PPTX
        build_tukuyi_pptx(p_data, pptx_filepath)
        if os.path.exists(pptx_filepath):
            with open(pptx_filepath, "rb") as f_pptx:
                col_down4.download_button(
                    label="📊 下載 16:9 PPTX 簡報",
                    data=f_pptx.read(),
                    file_name=pptx_filename,
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True
                )
        else:
            col_down4.info("（PPTX 生成腳本就緒）")

        st.markdown("""
        > 💡 **Google 簡報 (Google Slides) 無縫開啟小秘技**：  
        > 點擊下載的 `.pptx` 檔案後，直接拖拉到您的 [Google Drive](https://drive.google.com/) 雲端硬碟中，點兩下即可透過 Google Slides 進行雲端多人共同編輯，字型排版 100% 完美相容！
        """)

# ------------------------------------------------------------------------------
# TAB 5: B2B 虛擬數據包互動分析 (Virtual Dataset Explorer)
# ------------------------------------------------------------------------------
with tabs[4]:
    st.markdown("### 📊 土庫驛 B2B 虛擬銷售數據包")
    st.caption("供學員實測 AI 數據清洗、交叉分析與回購率洞察，無機密洩漏風險")

    df_sales = pd.DataFrame(VIRTUAL_SALES_DATA)
    st.dataframe(df_sales, use_container_width=True)

    st.markdown("#### 📈 數據洞察儀表板")
    c1, c2, c3 = st.columns(3)
    avg_price = df_sales["budget_per_box"].mean()
    total_qty = df_sales["qty"].sum()
    reorder_rate = (df_sales["reorder_next_year"] == "Yes").mean() * 100

    c1.metric("平均採購盒單價", f"NT$ {avg_price:.0f}")
    c2.metric("歷年虛擬總銷量", f"{total_qty:,} 盒")
    c3.metric("次年回購再購率", f"{reorder_rate:.1f}%")

    st.markdown("#### 💡 數據分析思考題（學員實作演練）")
    st.markdown("""
    1. **溫控與滿意度關聯**：為什麼「全常溫」的滿意度 (4.2~4.4) 普遍低於「冷藏+常溫組合」(4.6~4.9)？
    2. **客製化效應**：有加購「客製 Logo/燙金封套」的客戶，其次年回購率高達 100%，這對我們的定價策略有何啟發？
    """)

    csv_data = export_virtual_sales_csv()
    st.download_button(
        "📥 下載完整虛擬銷售數據 CSV",
        data=csv_data,
        file_name="tukuyi_virtual_sales_dataset.csv",
        mime="text/csv"
    )

# ------------------------------------------------------------------------------
# TAB 6: 6 大實戰題型提示詞庫 (Prompt Templates Library)
# ------------------------------------------------------------------------------
with tabs[5]:
    st.markdown("### 💡 6小時工作坊提示詞總庫 (CH01~CH03 完整 2-3 題實戰題型)")
    st.caption("每章節精選 2-3 題型（包含中秋核心題與各情境複習題）• 內建資安脫敏前綴")

    for p_key, p_val in PROMPT_TEMPLATES.items():
        with st.expander(f"{p_val['title']} ｜ {p_val['scenario']}"):
            st.markdown(f'<div class="prompt-box">{p_val["prompt"]}</div>', unsafe_allow_html=True)
