"""
土庫驛可可莊園 (Tukuyi Cocoa) - AI 行銷企劃工作台核心資料集
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
    "version": "2.0.0-enterprise",
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
# 6. 多題型提示詞模板庫 (CH01~CH03 完整 2-3 題實戰題型)
# ==============================================================================
PROMPT_TEMPLATES = {
    # -------------------------------------------------------------
    # CH01: 行銷企劃方法論實戰 (2-3 題)
    # -------------------------------------------------------------
    "ch01_q1_mid_autumn": {
        "title": "【CH01 題目一 (中秋必練)】中秋「可可月映」STP 市場定位探勘器",
        "scenario": "CH01 實務：以中秋真實案例深化 STP 與預算帶破局",
        "prompt": """【系統指令約束 (資安脫敏)】：本任務為土庫驛內部教學推演，不涉及未公開個人或企業敏感資料。
你是一位精通台灣食品伴手禮與高端 B2B 禮品市場的資深行銷策略顧問。
請依據「土庫驛可可莊園 (Tukuyi Cocoa)」的品牌核心資產，為【中秋節企業採購專案】進行完整的 STP 市場定位分析，重點解決客戶「預算卡死在特定區間 ($800-$1,200)」與「受夠油膩月餅」的痛點。

【土庫驛品牌底層資產】：
- 創辦人返鄉為失智父親打造莊園，「做純淨健康巧克力給爸爸吃」之感人初心
- Tree-to-Bar 13道工序慢磨、100%天然可可脂、零反式脂肪
- 明星品項：85%生巧克力、小山園抹茶生巧、炭焙烏龍生巧、莊園可可豆茶

【請輸出以下架構】：
1. Market Segmentation (市場區隔)：交叉「產業類型 (科技/金融/傳產)」與「預算敏感度」，劃分 4 個區隔。
2. Target Market Selection (目標市場)：選定最有吸引力的 2 個區隔，並給出具體毛利率與商業理由。
3. Positioning Statement (定位主張)：寫出一句結合「米其林級無糖黑巧 x 雲林創生溫度」的直擊心靈 Slogan。
4. 預算破局策略：當福委會預算卡死在 $600-$800 時，我們如何設計「分級加價搭售 (Upsell)」與「冷藏/常溫混合方案」說服其升級？"""
    },

    "ch01_q2_cny_spring": {
        "title": "【CH01 題目二 (複習演練)】春節「富貴可可‧金磚納福」高客單商務禮盒企劃",
        "scenario": "CH01 複習：針對年節送禮大檔，運用 5W2H 與 4P 建立高客單專案",
        "prompt": """【系統指令約束 (資安脫敏)】：請依據土庫驛可可莊園品牌資產，規劃【2027 農曆春節年節商務尊榮禮盒】。

【專案挑戰】：
春節是台灣企業送禮最大檔期，傳統市場被烏魚子、進口洋酒、名店燕窩所佔據。
土庫驛希望以「Tree-to-Bar 原豆可可磚 + 奢華 Bonbon 星空夾心 + 頂級茶品」切入客單價 $1,680 ~ $2,500 之頂級 VIP 賀禮市場。

【請輸出以下企劃模組】：
1. 5W2H 戰略檢核表（Why、What、Who、When、Where、How、How much）。
2. 4P 行銷組合矩陣：
   - Product：如何包裝「金磚可可」與星空鏡面淋面的視覺尊榮感？
   - Price：如何設計早鳥大宗折扣與高毛利架構 (守住 60% 毛利率)？
   - Place：如何結合企業高端 VIP 私享直送與全台溫控物流？
   - Promotion：如何將創辦人孝心故事化為春節「家與孝道」的溫暖祝福卡？"""
    },

    "ch01_q3_dragon_boat": {
        "title": "【CH01 題目三 (複習演練)】端午「黑巧冰粽 × 莊園冷萃茶」跨界消暑企劃",
        "scenario": "CH01 複習：淡季反向突圍，以跨界思維設計創新企劃",
        "prompt": """【系統指令約束 (資安脫敏)】：請為土庫驛設計【端午節企業消暑微型企劃案】。

【專案情境】：
端午節為傳統巧克力淡季，但現代員工極度恐懼傳統糯米粽的消化不良與高油脂熱量。
土庫驛計劃推出「可可冰心粽 (以 85% 生巧及抹茶為內餡) + 莊園冷萃可可茶」之跨界限量禮盒。

【請完成以下任務】：
1. 痛點反轉話術：如何用「告別脹氣油膩，迎接米其林級冰涼療癒」作為主要訴求？
2. 針對「生技醫藥」與「外商軟體」兩大重視健康與創新的族群，撰寫精準 STP。
3. 預期效益與產能排程評估：如何在夏季高溫下，確保低溫冷藏物流 100% 零融化客訴？"""
    },

    # -------------------------------------------------------------
    # CH02: 簡報提案方法論實戰 (2-3 題)
    # -------------------------------------------------------------
    "ch02_q1_mid_autumn_switch": {
        "title": "【CH02 題目一 (中秋必練)】中秋禮盒「一案三轉」3大受眾說服大綱",
        "scenario": "CH02 實務：一套產品，精準切換給主管(40%)、福委(40%)、異業(20%)",
        "prompt": """我們正在為土庫驛【中秋可可尊榮禮盒 (建議售價 $1,099，內含85%生巧+炭焙烏龍生巧+可可豆茶)】撰寫提案簡報。
請依據土庫驛 3 大簡報場景與受眾權重，產出 3 套截然不同的說服邏輯與簡報大綱：

【受眾一：公司內部決策主管 (40% 比重)】
- 核心焦點：毛利率需達 55% 以上、Tree-to-Bar 產能稼動率、包材客製庫存風險、交期排程。
- 請產出：3 頁決策簡報大綱，每一頁必須「結論先行 (Action Title)」，直球對決產能與利潤。

【受眾二：企業客戶福委會與採購窗口 (40% 比重)】
- 核心焦點：長官有面子、同仁零熱量負擔、低溫冷藏與常溫茶包分流配送、客製燙金腰封、行政零客訴。
- 請產出：3 頁提案簡報大綱，強調如何幫福委會「省事、贏得讚賞、解決冰箱爆滿問題」。

【受眾三：異業高端夥伴企業高層 (20% 比重)】
- 核心焦點：品牌雙贏光環、頂級 VIP 尊榮體驗、台灣在地創生故事與文化厚度。
- 請產出：2 頁合作大綱，聚焦於「品牌溢價共振與專屬私宴尊榮感」。"""
    },

    "ch02_q2_budget_breakthrough": {
        "title": "【CH02 題目二 (複習演練)】突破預算僵局：向卡死在 $600 預算的福委會提案 $880 升級款",
        "scenario": "CH02 複習：運用金字塔原理 SCQA 說服預算受限的採購窗口",
        "prompt": """請運用麥肯錫 SCQA 架構，為土庫驛業務團隊設計一份 5 頁的【預算升級說服簡報骨架】。

【情境挑戰】：
某科技公司福委會歷年每人預算嚴格卡死在 NT$ 600，原本只想採購全常溫廉價餅乾禮盒。
土庫驛業務希望說服福委會追加至 NT$ 880 (享用 85% 生巧 + 莊園可可豆茶的奢華升級組合)。

【請輸出 5 頁 SCQA 結構】：
- Slide 1: Situation (回顧同仁過去幾年收到千篇一律傳統禮盒的平淡反應與熱量抱怨)
- Slide 2: Complication (若繼續採購 $600 常溫普通禮盒，同仁滿意度依然低迷，福委會淪為例行公事)
- Slide 3: Question (只需每人微調 $280 預算，如何換來 95% 同仁狂讚與主管肯定？)
- Slide 4: Answer / Value Matrix (詳細列出 $880 方案帶來的米其林級無糖療癒感、客製燙金腰封與 ESG 創生認證)
- Slide 5: Action (提供免費樣盒直送福委會親自品鑑試吃，滿額即贈送全公司下午茶熱可可體驗)"""
    },

    "ch02_q3_vip_pitch": {
        "title": "【CH02 題目三 (複習演練)】異業 Pitch：土庫驛 × 德系豪車 VIP 車主奢華尊享私宴大綱",
        "scenario": "CH02 複習：20% 異業高階老闆簡報，黃金圈 (Golden Circle) 提案術",
        "prompt": """請為土庫驛行銷團隊設計一份提案給【德系頂級豪華休旅車台灣總代理 (如 Porsche / BMW)】的 6 頁聯名提案大綱。

【提案核心概念】：
「純粹動力，原豆慢磨」—— 結合德國精密造車工藝與土庫驛 Tree-to-Bar 13 道手工調溫極致匠人精神。

【請輸出大綱】：
1. Why (共同理念)：對極致細節與純粹工藝的永不妥協。
2. How (合作模式)：為交車尊爵車主客製化「手工星空 Bonbon 專屬車標木盒禮盒」與「莊園封園品鑑私宴」。
3. What (交付內容)：限量聯名禮盒規格、車主專屬品味卡與媒體曝光效益。
4. 預期雙贏效益：如何為車商提升 VIP 車主忠誠度，並為土庫驛樹立頂級奢華標竿。"""
    },

    # -------------------------------------------------------------
    # CH03: 視覺生圖與排版專題實戰 (2-3 題)
    # -------------------------------------------------------------
    "ch03_q1_cocoa_macro": {
        "title": "【CH03 題目一 (中秋生圖)】中秋生巧與微距可可粉霧面質感提示詞",
        "scenario": "CH03 生圖痛點破解：真實原豆慢磨光澤與極致可可粉微距質感",
        "prompt": """Prompt for ChatGPT Images 2.5 / DALL-E 3:
Extreme close-up commercial food photography of Tukuyi Cocoa handcrafted artisan 85% Nama chocolate cubes.
Each chocolate cube has razor-sharp edges and a velvety, ultra-fine dust of rich raw cocoa powder across its top surface, revealing delicate micro-textures and subtle golden cocoa butter sheen under warm directional rim lighting.
Beside the chocolate: roasted whole cocoa beans cut open to reveal authentic deep brown cocoa nibs, and subtle raw cocoa husk flakes.
Background: Luxurious dark slate and warm rustic wood board, a subtle out-of-focus hint of an open rigid chocolate box with gold foil emblem.
Color grading: Rich dark cocoa brown (#3B2314), warm champagne amber highlights, deep contrast, shallow depth of field (f/2.8, 100mm macro lens), 8k resolution, cinematic gourmet aesthetic. Strictly no melted or warped chocolate cubes. --ar 16:9"""
    },

    "ch03_q2_negative_space": {
        "title": "【CH03 題目二 (生圖痛點突破)】純淨留白 (Negative Space) 視覺圖卡提示詞 (防繁體字變形)",
        "scenario": "CH03 生圖痛點破解：解決繁體中文字變形問題，預留乾淨留白供後製排版",
        "prompt": """Prompt for ChatGPT Images 2.5:
A minimalist, high-end commercial advertising background for a luxury chocolate brand Christmas campaign.
Composition: Elegant asymmetric flat-lay.
Left side (30% of canvas): A beautifully styled arrangement of Tukuyi luxury dark chocolate gift box in deep brown (#3B2314) and champagne gold ribbon (#D4AF37), surrounded by subtle festive pine cones, cinnamon sticks, and raw cocoa pods.
Right side (70% of canvas): Completely clean, empty, smooth silk-cream colored surface (#FDFBF7) with soft warm ambient shadows, designed specifically as pristine negative space for typography and infographics.
NO TEXT, NO LETTERS, NO NUMBERS anywhere on the image.
Photorealistic, ultra-clean studio lighting, high key elegance, 8k resolution. --ar 16:9"""
    },

    "ch03_q3_infographic_exec": {
        "title": "【CH03 題目三 (複習演練)】一頁式高階主管商業彙報資訊圖卡 (Infographic Poster)",
        "scenario": "CH03 複習：一頁式企劃圖卡視覺化，適配內部主管與採購快速決策",
        "prompt": """Prompt for ChatGPT Images 2.5:
Clean, modern, premium corporate 1-page executive summary infographic poster for 'Tukuyi Cocoa B2B Holiday Gifting Program'.
Color Palette: Deep artisan cocoa brown (#3B2314), champagne gold (#D4AF37), and clean cream-white (#FDFBF7).
Structured layout:
- Header: Elegant luxury banner with subtle cocoa pod watermark.
- Section 1 (Top Left): 3 packaging tier illustrations with clear price tags ($699, $1099, $1680).
- Section 2 (Top Right): 4 circular badges highlighting key pillars (100% Pure Cocoa Butter, Tree-to-Bar Craft, Dual Temperature Delivery, ESG Local Empowerment).
- Section 3 (Bottom): Step-by-step corporate ordering timeline from free tasting kit to delivery.
Style: Vector infographic graphics harmonized with photorealistic chocolate elements, Swiss graphic design grid layout, high visual hierarchy, pristine executive briefing presentation. --ar 4:3"""
    }
}
