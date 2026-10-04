"""
土庫驛可可莊園 (Tukuyi Cocoa) - AI 行銷企劃工作台核心資料集 (v2.1 Enterprise)
==============================================================================
所有權人 / 著作權人：BOSS、院長、Eric 潘穩安博士 (Dr. Eric Wen-An Pan)
授權範圍：僅供土庫驛可可莊園企業內部教育訓練使用，嚴禁未經授權之複製、反向工程、商業轉售與二次分發。
==============================================================================
"""

# ==============================================================================
# 0. 系統版權與所有權宣告 (System Ownership & Copyright)
# ==============================================================================
SYSTEM_OWNERSHIP = {
    "owner": "BOSS / 院長 / Eric 潘穩安博士 (Dr. Eric Wen-An Pan)",
    "app_title": "AI 行銷企劃大師 Web App (Tukuyi Marketing AI Suite)",
    "version": "2.1.0-enterprise",
    "deployment_mode": "BYOK (Bring Your Own Key) - Zero Cloud Maintenance Cost",
    "security_policy": (
        "1. 本系統所有權與智財權歸屬 Eric 潘穩安博士所有。\n"
        "2. 嚴格保護商業機密，禁止任何未經授權之第三人盜用、篡改或轉售。\n"
        "3. API Key 僅留存於當前使用者瀏覽器 Session，伺服器不落地儲存，確保 100% 隱私資安。\n"
        "4. 所有生成企劃案均包含 SHA-256 數位指紋防篡改追蹤。"
    )
}

# ==============================================================================
# 1. 土庫驛品牌識別規範 (Brand CI / VI Guidelines)
# ==============================================================================
TUKUYI_BRAND_IDENTITY = {
    "brand_name": "土庫驛可可莊園 (Tukuyi Cocoa)",
    "origin": "台灣雲林縣土庫鎮 (原台糖五分車歷史節點)",
    "founder_story": (
        "2016年，創辦人陳盈豪為了照料罹患失智症的父親返鄉，以園藝治療為初心，"
        "斥資數億將荒廢廢棄豬舍打造為全台首座 Tree-to-Bar 創生可可莊園。"
        "初心非常純粹——『做最純淨健康的巧克力給爸爸吃』。"
    ),
    "core_values": [
        "Tree to Bar 13道原豆慢磨工藝",
        "無人工添加、堅持天然可可脂",
        "雲林在地小農契作與地方創生",
        "ESG 綠色永續與減碳零里程包裝"
    ],
    "ci_vi_colors": {
        "primary_cocoa": "#3B2314",      # 莊園頂級深可可棕 (沉穩奢華)
        "secondary_gold": "#D4AF37",     # 典雅香檳金 (尊榮高貴)
        "earth_terracotta": "#8C4A32",   # 暖紅陶大地色 (在地泥土溫度)
        "bg_cream": "#FDFBF7",           # 絲滑奶霜白 (乾淨簡約底色)
        "charcoal_black": "#1E1E1E",     # 竹炭墨黑 (高對比標題與文字)
        "card_bg": "#2A180D",            # 深色介面卡片色
        "border_color": "#5A3A25"        # 邊框裝飾色
    },
    "typography": {
        "title_font": "Noto Serif TC (思源宋體 - 展現職人典雅底蘊)",
        "body_font": "Noto Sans TC (思源黑體 - 現代清晰易讀)"
    },
    "tone_and_voice": "溫潤深邃、低調奢華、真實透明、富含土地人情味而不流於俗套。"
}

# ==============================================================================
# 2. 三大簡報場景與受眾特徵模型 (Audience Persona Matrix)
# ==============================================================================
AUDIENCE_PERSONAS = {
    "boss_internal": {
        "id": "boss_internal",
        "ratio": "40%",
        "title": "公司主管與內部決策會議",
        "core_interest": "投資報酬率 (ROI)、產能瓶頸、獲利毛利率、排程交期與品牌長期資產",
        "pain_points": [
            "節慶產能有限，Tree-to-Bar 精磨製程耗時，訂單暴增時是否面臨缺貨或延遲風險？",
            "B2B 客製化開版與冷藏溫控包材會否大幅侵蝕淨毛利率（毛利目標需守住 55% 以上）？",
            "業務團隊提案是否具備可持續性，抑或只是單次削價促銷？"
        ],
        "persuasion_strategy": "結論先行 (Pyramid Principle)，用數據說話，先報預期營收與利潤率，再提產能排程與風險防禦備案。",
        "keywords": ["毛利率 (GM%)", "保本點 (BEP)", "產能稼動率", "交期風險管理", "品牌資產積累"]
    },
    "procurement_b2b": {
        "id": "procurement_b2b",
        "ratio": "40%",
        "title": "企業客戶提案 (福委會 / 總務 / 採購窗口)",
        "core_interest": "員工滿意度、送禮大氣有面子、預算彈性分級、物流溫控容錯與採購發票合規",
        "pain_points": [
            "年年送月餅/蛋黃酥，員工抱怨熱量過高又膩口，但送非傳統點心又怕被長官嫌不夠大氣。",
            "冷藏生巧克力配送容易因收件人不在家導致融化客訴，總務分發行政負擔巨大。",
            "預算區間卡死 (如福委會預算限制在每人 $500 - $800 或 $1,000 - $1,200)，需多種規格組合。"
        ],
        "persuasion_strategy": "解決痛點方案法。強調『高奢不膩口、健康無負擔、ESG採購加分』，並提供『常溫/低溫雙軌禮盒方案』與『專人企業統配分流服務』。",
        "keywords": ["健康低負擔", "常溫冷藏彈性", "多階預算組合 ($500~$1,500)", "客製腰封與賀卡", "ESG 綠色採購加分"]
    },
    "partner_vip": {
        "id": "partner_vip",
        "ratio": "20%",
        "title": "異業結盟夥伴 (企業老闆 / 高階主管 / 品牌聯名)",
        "core_interest": "品牌雙贏效應、頂級 VIP 尊榮客戶體驗、地方創生永續故事與文化厚度",
        "pain_points": [
            "市面上聯名禮盒過於氾濫，流於貼標貼紙，缺乏真正的產品原創共鳴與獨特性。",
            "擔心合作方品牌力不足，反而拉低自身高端形象 (如金融 VIP / 豪車車主俱樂部)。"
        ],
        "persuasion_strategy": "價值共鳴與情感故事 (Golden Circle)。從創辦人為父造莊園的初心出發，結合頂級可可與在地風土，設計『限定訂製款』與專屬尊榮品鑑私宴。",
        "keywords": ["尊榮限量聯名", "Tree-to-Bar 匠人精神", "VIP 私享體驗", "台灣在地風土故事", "品牌溢價共振"]
    }
}

# ==============================================================================
# 3. 課堂教學案例：中秋節「可可尊榮月映禮盒」(已知結案實戰拆解)
# ==============================================================================
MID_AUTUMN_CASE = {
    "case_title": "土庫驛 2025 中秋「可可月映‧大地之金」B2B 企業尊榮禮盒",
    "background": "為打破傳統中秋糕餅紅海競爭，土庫驛將 85% 頂級生巧、特製炭焙烏龍夾心生巧與在地可可豆茶整合為中秋跨界奢華禮盒。",
    "stp_framework": {
        "segmentation": "鎖定科技業、金融保險業、外商會計師事務所等注重主管健康與品味的中高階企業客戶。",
        "targeting": "客單價 $880 ~ $1,680 之企業採購案，年採購規模 200~1,500 盒。",
        "positioning": "『非傳統、零反式脂肪、兼具尊貴儀式感與 ESG 永續倡議』的高端中秋商務賀禮。"
    },
    "four_p_strategy": {
        "product": "85% 生巧克力 16入 + 炭焙烏龍可可夾心 8入 + 莊園可可豆茶包 6包 (兼具品巧與解膩之雙重享受)。",
        "price": "分為『雅緻款 $880』、『尊爵款 $1,280』、『極致奢華訂製款 $1,680』(含客製燙金腰封與專屬木盒)。",
        "place": "B2B 專屬企業經理一對一服務、預約品鑑直送、企業專屬線上大宗試算下單頁面。",
        "promotion": "早鳥滿額享全台單點/多分點免運低溫溫控直送、企業免費雷雕客製企業 Logo 燙金封套、附贈地方創生 ESG 倡議小卡。"
    },
    "actual_performance_summary": {
        "total_revenue": "NT$ 4,860,000",
        "total_boxes_sold": "4,120 盒",
        "avg_order_value": "NT$ 1,180",
        "gross_margin": "58.4%",
        "pnl_analysis": {
            "total_sales": 4860000,
            "cogs": 2021760,        # 原物料與製造成本
            "gross_profit": 2838240, # 毛利
            "logistics_packaging": 583200, # 客製燙金腰封與低溫冷藏直送
            "marketing_sales_exp": 388800, # 業務與推廣費用
            "operating_net_profit": 1866240, # 營業淨利
            "net_margin_pct": "38.4%"
        },
        "key_success_factor": "成功抓準福委會『受夠了送月餅被員工嫌胖』的心理痛點，以『米其林級無糖低負擔黑巧』切入，回購率達 42%。"
    }
}

# ==============================================================================
# 4. CH05 工作坊演練案例：聖誕節「星漾可可」B2B 企業禮盒提案大賽
# ==============================================================================
CHRISTMAS_WORKSHOP_CASE = {
    "case_title": "土庫驛 2026 聖誕「星漾暖心‧可可漫步」B2B 企業年終感恩禮盒提案",
    "brief_challenge": (
        "某頂級半導體/外商科技巨頭福委會與總務處釋出 2,000 份年終聖誕暨尾牙感恩禮品預算 (預算總額約 200~250 萬新台幣)。"
        "採購要求：(1) 必須兼顧科技業高壓工程師喜愛的解壓療癒感；(2) 符合企業年度 ESG 永續減碳採購指標；"
        "(3) 提供常溫/低溫彈性配送選項；(4) 附帶個人化或客製化暖心設計。"
    ),
    "candidate_product_pool": [
        {"name": "經典 85% 生巧克力", "type": "低溫冷藏", "cost": 180, "retail": 420, "selling_point": "極致純粹慢磨，高多酚抗氧化療癒"},
        {"name": "小山園抹茶生巧克力", "type": "低溫冷藏", "cost": 210, "retail": 460, "selling_point": "宇治抹茶苦甜回甘，高顏值聖誕綠意配色"},
        {"name": "粉戀果香生巧克力", "type": "低溫冷藏", "cost": 200, "retail": 450, "selling_point": "天然覆盆子果香，粉紅浪漫聖誕氛圍"},
        {"name": "法式 Bonbon 夾心手工巧克力", "type": "低溫/恆溫", "cost": 240, "retail": 520, "selling_point": "星空大理石鏡面淋面，頂級珠寶盒質感"},
        {"name": "莊園可可豆茶 (濾泡包)", "type": "常溫", "cost": 80, "retail": 250, "selling_point": "低咖啡因、可可多酚助眠抗壓、全天然零廢棄 ESG"},
        {"name": "巧克力夾心薄脆餅", "type": "常溫", "cost": 110, "retail": 280, "selling_point": "辦公室下午茶分享首選、免冷藏、保存期長"},
        {"name": "極濃可可沖泡飲 (隨行包)", "type": "常溫", "cost": 90, "retail": 240, "selling_point": "冬日辦公室暖手暖心熱可可、100% 無添加精緻糖"}
    ],
    "target_budget_tiers": [
        {"tier": "暖心分享款 (福委大量預算)", "price_range": "NT$ 599 ~ NT$ 799", "target_client": "全體員工均發 / 工會尾牙送禮"},
        {"tier": "尊爵品味款 (中階主管/績優同仁)", "price_range": "NT$ 999 ~ NT$ 1,299", "target_client": "專案組長 / 年度績優團隊激勵"},
        {"tier": "星漾旗艦款 (重要外部合作夥伴/VIP客戶)", "price_range": "NT$ 1,599 ~ NT$ 2,200", "target_client": "核心供應商 / 頂級大客戶商務賀禮"}
    ]
}

# ==============================================================================
# 5. 土庫驛 B2B 虛擬銷售數據包 (Virtual Dataset Package)
# ==============================================================================
VIRTUAL_SALES_DATA = [
    {"year": 2024, "festival": "中秋節", "client_industry": "半導體/科技業", "budget_per_box": 1250, "qty": 850, "storage_type": "冷藏+常溫組合", "custom_logo": True, "satisfaction_score": 4.8, "reorder_next_year": "Yes"},
    {"year": 2024, "festival": "中秋節", "client_industry": "金融保險業", "budget_per_box": 980, "qty": 1200, "storage_type": "低溫冷藏", "custom_logo": True, "satisfaction_score": 4.7, "reorder_next_year": "Yes"},
    {"year": 2024, "festival": "中秋節", "client_industry": "傳統製造業", "budget_per_box": 650, "qty": 600, "storage_type": "全常溫", "custom_logo": False, "satisfaction_score": 4.2, "reorder_next_year": "No"},
    {"year": 2024, "festival": "聖誕年終", "client_industry": "外商軟體/網路", "budget_per_box": 1500, "qty": 450, "storage_type": "低溫冷藏(Bonbon)", "custom_logo": True, "satisfaction_score": 4.9, "reorder_next_year": "Yes"},
    {"year": 2024, "festival": "聖誕年終", "client_industry": "醫藥生技業", "budget_per_box": 1100, "qty": 520, "storage_type": "冷藏+常溫組合", "custom_logo": True, "satisfaction_score": 4.6, "reorder_next_year": "Yes"},
    {"year": 2025, "festival": "中秋節", "client_industry": "半導體/科技業", "budget_per_box": 1380, "qty": 1100, "storage_type": "冷藏+可可茶組合", "custom_logo": True, "satisfaction_score": 4.9, "reorder_next_year": "Yes"},
    {"year": 2025, "festival": "中秋節", "client_industry": "法律與會計師事務所", "budget_per_box": 1680, "qty": 380, "storage_type": "旗艦木盒冷藏", "custom_logo": True, "satisfaction_score": 4.9, "reorder_next_year": "Yes"},
    {"year": 2025, "festival": "中秋節", "client_industry": "金融保險業", "budget_per_box": 1050, "qty": 1450, "storage_type": "冷藏+常溫組合", "custom_logo": True, "satisfaction_score": 4.8, "reorder_next_year": "Yes"},
    {"year": 2025, "festival": "中秋節", "client_industry": "連鎖零售餐飲(福委)", "budget_per_box": 580, "qty": 900, "storage_type": "全常溫(餅乾+可可沖泡)", "custom_logo": False, "satisfaction_score": 4.4, "reorder_next_year": "Yes"},
    {"year": 2025, "festival": "聖誕年終", "client_industry": "精品專櫃/高端車商", "budget_per_box": 2100, "qty": 280, "storage_type": "奢華Bonbon訂製", "custom_logo": True, "satisfaction_score": 5.0, "reorder_next_year": "Yes"},
    {"year": 2025, "festival": "聖誕年終", "client_industry": "半導體/科技業", "budget_per_box": 1200, "qty": 950, "storage_type": "生巧+常溫茶包", "custom_logo": True, "satisfaction_score": 4.7, "reorder_next_year": "Yes"}
]

# ==============================================================================
# 6. 完整行銷企劃簡報實戰題型提示詞庫 (含 ［    ］ 符號開放填空)
# ==============================================================================
PROMPT_TEMPLATES = {
    # -------------------------------------------------------------
    # Phase 01: 產品市場定位分析 (STP + 4P + P&L 損益分析)
    # -------------------------------------------------------------
    "phase01_template_bracket": {
        "title": "【Phase 01 實戰提示詞模板】產品市場定位分析 (STP + 4P + P&L)",
        "scenario": "Phase 01 交付：生成多頁視覺化 PPTX 簡報與一頁式資訊圖卡 PNG",
        "prompt": """【系統指令約束 (資安脫敏)】：本任務為企業內部策略分析，請依據以下填寫資訊，為品牌進行嚴謹的市場定位分析。
你是一位具備 10 年資歷的頂級企業策略行銷總監。
請針對以下企業基本資料與財務數據，生成一份同時能說服「內部管理層」與「外部目標客戶」的【產品市場定位分析報告 (STP + 4P + P&L)】。

【企業基本底蘊】：
- 品牌/企業名稱：［  土庫驛可可莊園  ］
- 品牌初心與故事：［  創辦人為照護失智父親返鄉，打造全台首座 Tree-to-Bar 創生莊園，做純淨無添加巧克力給父親吃  ］
- 核心工藝特色：［  13道工序慢磨、堅持 100% 天然可可脂、零反式脂肪  ］
- 核心價值觀：［  台灣在地創生、小農契作、ESG 綠色永續採購  ］

【結案數據績效與 P&L 損益指標】：
- 專案總營收：［  NT$ 4,860,000  ］
- 總銷售盒數：［  4,120 盒  ］
- 平均盒單價 (AOV)：［  NT$ 1,180  ］
- 專案毛利率：［  58.4%  ］
- 營業淨利率與 P&L 亮點：［  總製造成本 41.6%、客製燙金與冷藏物流 12.0%、營業淨利率達 38.4%  ］

【請為我生成以下兩項交付物】：
1. 【多頁式視覺化產品市場定位分析簡報 (PPTX 結構)】：
   - Slide 1: 封面（動態行動標題、品牌標語、提案人）
   - Slide 2: 品牌願景與初心故事（感人初心如何轉化為高溢價護城河）
   - Slide 3: 財務績效總結與 P&L 損益分析（營收、毛利率與淨利結構）
   - Slide 4: STP 市場定位深度拆解（S 市場區隔矩陣、T 目標採購規模、P 定位 Slogan）
   - Slide 5: 4P 行銷組合落地策略（產品配置、三階梯定價、通路溫控、客製加值）
   - Slide 6: 商業可行性結論與下階段行動（BEP 損益兩平點與排程安全係數）

2. 【一頁式視覺化資訊圖卡 (PNG 資訊圖表 Prompt)】：
   - 請提供可用於 ChatGPT 或 Gemini 生圖的一頁式 Executive Summary 資訊圖卡提示詞，包含頂部標題、三大定價階梯、四大價值柱與財務指標卡。"""
    },

    # -------------------------------------------------------------
    # Phase 02: 目標受眾決策分析 (Persona + 同理心地圖 + NSDB)
    # -------------------------------------------------------------
    "phase02_template_bracket": {
        "title": "【Phase 02 實戰提示詞模板】目標受眾決策分析 (Persona + 同理心 + NSDB)",
        "scenario": "Phase 02 交付：生成多頁視覺化目標受眾分析 PPTX 與一頁式 PNG 圖卡",
        "prompt": """【系統指令約束 (資安脫敏)】：請依據麥肯錫金字塔原理與 NSDB 框架，執行深度目標受眾分析。
你是一位精通商業心理學與 B2B 採購決策旅程的提案專家。
請依據以下受眾特徵與同理心地圖，建構一份直擊受眾痛點的【目標受眾決策分析簡報】。

【目標受眾基本資料】：
- 主要受眾類型：［  企業客戶提案 (福委會 / 總務 / 採購)  ］
- Persona 角色輪廓：［  科技業與金融業福委會主委，年齡 32~45 歲，重視同仁口碑與預算合規  ］
- 核心關注利益：［  同仁滿意度高、無油膩熱量負擔、預算彈性分級、常溫冷藏分流配送、行政零客訴  ］
- 最大決策抗拒痛點：［  年年送傳統糕餅被同仁抱怨肥胖膩口；全低溫冷藏易融化且辦公室冰箱爆滿；預算死板卡在特定區間  ］

【同理心地圖 (Empathy Map)】：
- 所想所感 (Think & Feel)：［  擔心挑選的禮品被同仁批評或長官嫌不夠大氣；渴望一次省事的完美結案  ］
- 所見所聞 (See & Hear)：［  看見同仁將高熱量月餅堆在茶水間放到發霉；聽到主管要求具備 ESG 綠色永續指標  ］
- 所說所做 (Say & Do)：［  開會時嚴格審核預算單價；私下詢問是否有樣品試吃與統配分流服務  ］
- 痛苦 (Pains) 與 渴望 (Gains)：［  痛點是冰箱爆滿與客訴；渴望是獲得同仁瘋狂好評且長官公開肯定  ］

【NSDB 說服切角分析】：
- Need (受眾深層需求)：［  兼具星級奢華面子與 0 反式脂肪健康低負擔的節慶商務贈禮  ］
- Solution (我方核心解方)：［  土庫驛米其林級無糖黑巧 + 莊園可可豆茶，搭配常溫低溫雙軌彈性溫控  ］
- Differentiation (差異化優勢)：［  Tree-to-Bar 13道工序慢磨、在地創生感人故事、免費客製企業專屬燙金腰封  ］
- Benefit (量化與非量化效益)：［  同仁滿意度提升至 95% 以上，減輕總務 60% 分發負擔，為公司增添 ESG 採購亮點  ］

【請為我生成以下兩項交付物】：
1. 【多頁式視覺化目標受眾決策分析簡報 (PPTX 結構)】：
   - 包含 Empathy Map 同理心畫像、痛點轉換矩陣、NSDB 說服邏輯與結論先行 (Action Title) 投影片大綱。
2. 【一頁式視覺化決策圖卡 (PNG 資訊圖表 Prompt)】：
   - 適合生圖工具的受眾痛點 vs 解方一對一對照圖卡提示詞。"""
    },

    # -------------------------------------------------------------
    # Phase 02+01: 終局版行銷企劃案提示詞 (整合版)
    # -------------------------------------------------------------
    "final_master_proposal_prompt": {
        "title": "【終局版行銷企劃案提示詞】整合 Phase 01 + Phase 02 完整全案",
        "scenario": "終極交付：生成多頁式視覺化［ 產品名 ］行銷企劃 PPTX 與一頁式 PNG 圖卡",
        "prompt": """【系統指令約束 (資安脫敏)】：你是一位頂級行銷企劃大師兼簡報架構師。
請整合以下【Phase 01 品牌底蘊/STP/4P/P&L】與【Phase 02 目標受眾/同理心/NSDB】，
為產品［  土庫驛 2026 聖誕星漾可可企業尊榮禮盒  ］生成終局版完整行銷企劃簡報 (PPTX) 與一頁式資訊圖卡 (PNG) 提示詞。

【全案輸入參數】：
1. 品牌精神：［  土庫驛可可莊園 • 為父造莊園 • Tree-to-Bar 13道慢磨工藝 • 雲林創生  ］
2. 產品規格：［  85%經典生巧 + 小山園抹茶生巧 + 莊園可可豆茶包 (常溫低溫雙軌配搭)  ］
3. 定價與 P&L：［  分享款 $699 / 尊爵款 $1,099 / 旗艦奢華款 $1,680，目標毛利率 57.2%  ］
4. 目標受眾：［  高科技半導體與外商金融企業福委總務，重視健康、面子與 ESG 永續  ］
5. 受眾痛點：［  糕餅熱量高被嫌棄、冷藏配送不易、預算卡死在特定區間  ］
6. NSDB 解方：［  Need健康抗壓、Solution雙軌可可茶禮盒、Diff在地13道工藝、Benefit滿意度95%與ESG加分  ］

【請嚴格依據 16:9 比例與土庫驛 CI/VI 色彩 (#3B2314 深棕 / #D4AF37 香檳金 / #FDFBF7 奶霜白)，輸出：】
- 【完整 10 頁 PPTX 簡報詳細腳本】：每頁均含 Action Title 動態結論句、卡片式視覺排版建議、具體數據指針與演講講者備忘錄 (Speaker Notes)。
- 【一頁式 Executive Summary 資訊圖卡生圖 Prompt (通用於 ChatGPT & Gemini)】。"""
    },

    # -------------------------------------------------------------
    # Phase 03: 雙軌通用高階生圖提示詞 (ChatGPT & Gemini 通用)
    # -------------------------------------------------------------
    "phase03_universal_image_prompt": {
        "title": "【Phase 03 通用生圖模板】產品特定細節與 70% 留白防變形",
        "scenario": "通用於 ChatGPT (DALL-E 3) 與 Gemini (Imagen 3)",
        "prompt": """Prompt for Gemini (Imagen 3) & ChatGPT (DALL-E 3):
Commercial luxury food photography of premium handcrafted artisan chocolate gift box by Tukuyi Cocoa.
【Product Details & Texture】:
- Open rigid luxury box in deep artisan cocoa brown (#3B2314) with delicate champagne gold hot stamping foil (#D4AF37).
- Inside: neatly cut cubes of 85% Nama dark chocolate, with razor-sharp geometric edges and an ultra-fine, velvety dusting of raw cocoa powder across the top surface, revealing a subtle golden sheen of natural cocoa butter under soft lighting.
- Beside the cubes: emerald-green Uji Matcha nama chocolate cubes and glossy hand-painted galaxy marble Bonbons.
【Context & Props】:
- A clear glass teapot with warm amber-colored cocoa bean husk tea, real roasted whole cocoa pods sliced open showing raw beans, and delicate cinnamon sticks.
【Composition & Negative Space】:
- Asymmetric flat-lay commercial studio layout: left 35% features the luxurious product arrangement, right 65% is a completely clean, pristine, smooth silk-cream surface (#FDFBF7) with subtle soft natural shadows, reserved strictly as clean negative space for typography.
- STRICTLY NO TEXT, NO LETTERS, NO TYPOGRAPHY on the image.
【Camera & Lighting】:
- 100mm macro lens, f/2.8 shallow depth of field, 3200K warm golden hour rim lighting, 8k resolution, cinematic commercial gourmet aesthetic. --ar 16:9"""
    }
}
