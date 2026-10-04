"""
土庫驛可可莊園 - 商業提案 PPTX 生成引擎 (v2.1)
嚴格遵循品牌 CI/VI 指南：16:9 比例、深可可棕 (#3B2314)、香檳金 (#D4AF37)、奶霜白 (#FDFBF7)
整合 STP、4P、P&L 財務分析與 NSDB (Need, Solution, Differentiation, Benefit) 說服模型
所有權人：BOSS / 院長 / Eric 潘穩安博士
"""

import os
from typing import Optional

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    HAS_PPTX = True
except ImportError:
    HAS_PPTX = False

# 土庫驛品牌調色盤 (RGBColor 封裝)
COLOR_COCOA_DARK = RGBColor(59, 35, 20)       # #3B2314 深可可色
COLOR_COCOA_CARD = RGBColor(42, 24, 13)       # #2A180D 卡片深色
COLOR_GOLD = RGBColor(212, 175, 55)           # #D4AF37 典雅香檳金
COLOR_CREAM = RGBColor(253, 251, 247)         # #FDFBF7 絲滑奶霜白
COLOR_CHARCOAL = RGBColor(30, 30, 30)         # #1E1E1E 沉穩碳黑
COLOR_MUTED = RGBColor(180, 165, 150)         # 次級文字色
COLOR_BORDER = RGBColor(90, 58, 37)           # 邊框裝飾色

def build_tukuyi_pptx(proposal_data: dict, output_path: str) -> bool:
    """
    建構土庫驛專屬 16:9 商業提案簡報 (包含 NSDB 與 P&L 結構)
    """
    if not HAS_PPTX:
        print("[WARN] python-pptx 未安裝，無法生成原生 .pptx 簡報。")
        return False

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    title = proposal_data.get("title", "土庫驛 B2B 節慶企業禮盒提案")
    audience = proposal_data.get("audience_name", "企業客戶提案 (福委 / 總務 / 採購)")
    festival = proposal_data.get("festival", "聖誕節年終感恩禮盒")
    summary = proposal_data.get("summary", "以 Tree-to-Bar 頂級可可與 13 道工序，打造尊榮健康且兼顧 ESG 的企業商務禮盒。")

    # 輔助：背景設定
    def set_background(slide, color):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = color

    # 輔助：添加卡片
    def add_card(slide, left, top, width, height, bg_color=COLOR_COCOA_CARD, border_color=COLOR_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
        return shape

    # 輔助：通用頂部標題列
    def add_header(slide, subtitle, main_title):
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.35))
        tf = tag_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"◆ 土庫驛可可莊園 (TUKUYI COCOA) ｜ {subtitle}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_GOLD

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.65))
        tf2 = title_box.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = main_title
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_CREAM

    # -------------------------------------------------------------
    # SLIDE 1: 封面 (Cover)
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    set_background(slide1, COLOR_COCOA_DARK)

    add_card(slide1, Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5), bg_color=COLOR_COCOA_CARD, border_color=COLOR_GOLD)

    box = slide1.shapes.add_textbox(Inches(1.5), Inches(1.6), Inches(10.333), Inches(3.8))
    tf = box.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "TUKUYI COCOA ESTATE • B2B CORPORATE PROPOSAL • 所有權人：Eric 潘穩安博士"
    p0.font.size = Pt(12)
    p0.font.color.rgb = COLOR_GOLD
    p0.font.bold = True

    p1 = tf.add_paragraph()
    p1.text = title
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_CREAM
    p1.space_before = Pt(12)

    p2 = tf.add_paragraph()
    p2.text = f"專案主題：{festival} ｜ 目標對象：{audience}"
    p2.font.size = Pt(15)
    p2.font.color.rgb = COLOR_MUTED
    p2.space_before = Pt(10)

    p3 = tf.add_paragraph()
    p3.text = f"『做巧克力給爸爸吃的純粹初心』• 雲林創生 Tree-to-Bar 13道工序 100%原豆慢磨"
    p3.font.size = Pt(13)
    p3.font.italic = True
    p3.font.color.rgb = COLOR_GOLD
    p3.space_before = Pt(20)

    # -------------------------------------------------------------
    # SLIDE 2: 痛點與核心解答 (SCQA)
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    set_background(slide2, COLOR_COCOA_DARK)
    add_header(slide2, "痛點突破與提案核心 (SCQA)", "突破傳統送禮同質化：健康尊榮與 ESG 永續新解答")

    add_card(slide2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    c1_box = slide2.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.3))
    tf = c1_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "⚠️ 傳統節慶企業送禮的三大硬傷"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD

    points_pain = [
        "糕餅高熱量負擔：員工怕胖、長官嫌膩，大量轉送流於浪費。",
        "同質化嚴重：年年相似包裝，無法體現企業品牌高度與誠意。",
        "配送行政負擔：冷藏保鮮門檻高，收件不在容易融化產生客訴。"
    ]
    for pt in points_pain:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_CREAM
        p.space_before = Pt(12)

    add_card(slide2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8), border_color=COLOR_GOLD)
    c2_box = slide2.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.0), Inches(4.3))
    tf2 = c2_box.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "✨ 土庫驛提出的旗艦級解方"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD

    points_sol = [
        "米其林級無糖低負擔：85%生巧克力高多酚療癒，同仁零負擔讚不絕口。",
        "Tree-to-Bar 感人故事：創辦人為父造莊園，兼具地方創生 ESG 永續倡議加分。",
        "常溫/低溫彈性配送：混和搭配可可豆茶與薄脆餅，免去辦公室冰箱爆滿噩夢。"
    ]
    for pt in points_sol:
        p = tf2.add_paragraph()
        p.text = f"✔ {pt}"
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_CREAM
        p.space_before = Pt(12)

    # -------------------------------------------------------------
    # SLIDE 3: STP 策略定位
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    set_background(slide3, COLOR_COCOA_DARK)
    add_header(slide3, "STP 市場定位", "精準錨定高價值客群，樹立頂級創生巧克力標竿")

    add_card(slide3, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8))
    b1 = slide3.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(3.2), Inches(4.3))
    t1 = b1.text_frame
    t1.word_wrap = True
    t1.paragraphs[0].text = "S - 市場區隔"
    t1.paragraphs[0].font.size = Pt(16)
    t1.paragraphs[0].font.bold = True
    t1.paragraphs[0].font.color.rgb = COLOR_GOLD
    p = t1.add_paragraph()
    p.text = proposal_data.get("stp_s", "以重視 ESG 永續、同仁健康抗壓與精緻品味的高科技業、外商金融及大型企業為主。")
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_CREAM
    p.space_before = Pt(14)

    add_card(slide3, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8), border_color=COLOR_GOLD)
    b2 = slide3.shapes.add_textbox(Inches(5.0), Inches(2.0), Inches(3.2), Inches(4.3))
    t2 = b2.text_frame
    t2.word_wrap = True
    t2.paragraphs[0].text = "T - 目標市場"
    t2.paragraphs[0].font.size = Pt(16)
    t2.paragraphs[0].font.bold = True
    t2.paragraphs[0].font.color.rgb = COLOR_GOLD
    p = t2.add_paragraph()
    p.text = proposal_data.get("stp_t", "鎖定客單價 $800 - $1,500 區間之年終採購案，單批採購量 300 ~ 2,000 盒。")
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_CREAM
    p.space_before = Pt(14)

    add_card(slide3, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8))
    b3 = slide3.shapes.add_textbox(Inches(9.0), Inches(2.0), Inches(3.2), Inches(4.3))
    t3 = b3.text_frame
    t3.word_wrap = True
    t3.paragraphs[0].text = "P - 品牌定位"
    t3.paragraphs[0].font.size = Pt(16)
    t3.paragraphs[0].font.bold = True
    t3.paragraphs[0].font.color.rgb = COLOR_GOLD
    p = t3.add_paragraph()
    p.text = proposal_data.get("stp_p", "『雲林在地創生 x 職人慢磨』的頂級永續商務賀禮，不可替代的風土故事。")
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_CREAM
    p.space_before = Pt(14)

    # -------------------------------------------------------------
    # SLIDE 4: NSDB 說服架構 (Need, Solution, Differentiation, Benefit)
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    set_background(slide4, COLOR_COCOA_DARK)
    add_header(slide4, "Phase 02 說服策略 (NSDB)", "直擊客戶深層痛點：建構無法拒絕的價值主張")

    nsdb_items = [
        ("N - Need 痛點需求", proposal_data.get("nsdb_n", "需要兼具星級大氣面子、同仁零熱量負擔且行政省事無客訴之禮盒。")),
        ("S - Solution 核心解方", proposal_data.get("nsdb_s", "85% 生巧克力搭配莊園可可豆茶，提供『常溫/低溫雙軌分流配送』方案。")),
        ("D - Differentiation 獨特差異", proposal_data.get("nsdb_d", "Tree-to-Bar 13道工序慢磨、創生孝心故事、免費客製企業燙金腰封與雷雕。")),
        ("B - Benefit 效益實現", proposal_data.get("nsdb_b", "同仁滿意度 95% 以上，減輕總務 60% 配送負擔，提升企業 ESG 永續評鑑。"))
    ]

    coords_nsdb = [
        (Inches(0.8), Inches(1.8)),
        (Inches(6.8), Inches(1.8)),
        (Inches(0.8), Inches(4.3)),
        (Inches(6.8), Inches(4.3))
    ]

    for idx, (title_text, desc_text) in enumerate(nsdb_items):
        x, y = coords_nsdb[idx]
        add_card(slide4, x, y, Inches(5.6), Inches(2.2), border_color=COLOR_GOLD)
        tb = slide4.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), Inches(5.2), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"◆ {title_text}"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_GOLD
        p2 = tf.add_paragraph()
        p2.text = desc_text
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_CREAM
        p2.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 5: 4P 行銷組合與產品亮點
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    set_background(slide5, COLOR_COCOA_DARK)
    add_header(slide5, "4P 行銷組合落地", "米其林職人配搭、彈性階梯預算與尊榮客製服務")

    grid_items = [
        ("Product 產品組合", proposal_data.get("p_product", "85% 生巧 + 抹茶生巧 + 莊園可可豆茶包")),
        ("Price 階梯定價", proposal_data.get("p_price", "三階彈性定價：分享款 $699 / 尊爵款 $1,099 / 旗艦奢華款 $1,680")),
        ("Place 通路服務", proposal_data.get("p_place", "B2B 顧問一對一試吃配送、企業專屬線上大宗試算下單頁面")),
        ("Promotion 促銷禮遇", proposal_data.get("p_promotion", "早鳥滿額免運溫控、免費客製燙金腰封與企業 Logo 雷雕、ESG 倡議小卡"))
    ]

    for idx, (title_text, desc_text) in enumerate(grid_items):
        x, y = coords_nsdb[idx]
        add_card(slide5, x, y, Inches(5.6), Inches(2.2))
        tb = slide5.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), Inches(5.2), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"■ {title_text}"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_GOLD
        p2 = tf.add_paragraph()
        p2.text = desc_text
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_CREAM
        p2.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 6: 財務 P&L 效益與行動呼籲 (CTA)
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    set_background(slide6, COLOR_COCOA_DARK)
    add_header(slide6, "財務 P&L 效益與早鳥行動呼籲", "創造同仁超高滿意度，達成企業 ESG 採購雙贏")

    metrics = [
        ("目標盒數", proposal_data.get("kpi_boxes", "2,000 盒")),
        ("營收規模", proposal_data.get("kpi_revenue", "NT$ 2.2M")),
        ("預估毛利率", proposal_data.get("kpi_margin", "56.5%")),
        ("預估淨利率", proposal_data.get("pnl_net_margin", "38.5%"))
    ]

    for i, (m_lbl, m_val) in enumerate(metrics):
        mx = Inches(0.8 + i * 2.95)
        add_card(slide6, mx, Inches(1.8), Inches(2.75), Inches(2.0), border_color=COLOR_GOLD)
        tb = slide6.shapes.add_textbox(mx + Inches(0.1), Inches(2.1), Inches(2.55), Inches(1.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = m_val
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = COLOR_GOLD
        p.alignment = PP_ALIGN.CENTER
        p2 = tf.add_paragraph()
        p2.text = m_lbl
        p2.font.size = Pt(13)
        p2.font.color.rgb = COLOR_MUTED
        p2.alignment = PP_ALIGN.CENTER
        p2.space_before = Pt(8)

    add_card(slide6, Inches(0.8), Inches(4.2), Inches(11.6), Inches(2.4), bg_color=COLOR_COCOA_CARD, border_color=COLOR_GOLD)
    cta_box = slide6.shapes.add_textbox(Inches(1.2), Inches(4.4), Inches(10.8), Inches(2.0))
    tf = cta_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🎯 企業專屬試吃品鑑與早鳥專案時程 (Next Action)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD
    p1 = tf.add_paragraph()
    p1.text = "1. 免費預約「頂級生巧克力與可可豆茶」品鑑樣盒直送辦公室，福委總務親自試吃無負擔。"
    p1.font.size = Pt(13)
    p1.font.color.rgb = COLOR_CREAM
    p1.space_before = Pt(8)
    p2 = tf.add_paragraph()
    p2.text = "2. 專屬企業經理 1 對 1 接洽：客製化燙金腰封 3D 模擬圖、分批配送時程確認與多點低溫溫控試算。"
    p2.font.size = Pt(13)
    p2.font.color.rgb = COLOR_CREAM
    p2.space_before = Pt(6)

    prs.save(output_path)
    print(f"[SUCCESS] 土庫驛品牌 PPTX 簡報 (含 NSDB) 已生成至：{output_path}")
    return True

if __name__ == "__main__":
    demo_data = {
        "title": "土庫驛 2026 聖誕星漾 B2B 禮盒提案",
        "audience_name": "企業客戶採購與福委會",
        "festival": "聖誕節年終感恩",
        "summary": "以 Tree-to-Bar 頂級可可與 13 道工序，打造尊榮健康且兼顧 ESG 的企業商務禮盒。",
        "stp_s": "高科技半導體與外商金融主管及福委採購窗口。",
        "stp_t": "客單價 $800 - $1,500 區間之年終福委及 VIP 外部客戶禮盒。",
        "stp_p": "『雲林在地創生 x 米其林級頂級可可』之尊榮商務賀禮。",
        "p_product": "85% 生巧克力 + 小山園抹茶生巧 + 莊園可可豆茶包，冷藏常溫彈性配搭。",
        "p_price": "三階梯定價：分享款 $699 / 尊爵款 $1,099 / 旗艦奢華款 $1,680。",
        "p_place": "專人 B2B 顧問一對一試吃配送、企業專屬線上大宗試算下單頁面。",
        "p_promotion": "早鳥滿額免運溫控、免費客製燙金腰封與企業 Logo 雷雕、附贈地方創生小卡。",
        "nsdb_n": "需要兼顧星級大氣面子、同仁零熱量負擔且行政省事無客訴之禮盒。",
        "nsdb_s": "85% 生巧克力搭配莊園可可豆茶，提供『常溫/低溫雙軌分流配送』方案。",
        "nsdb_d": "Tree-to-Bar 13道工序慢磨、創生孝心故事、免費客製企業燙金腰封與雷雕。",
        "nsdb_b": "同仁滿意度 95% 以上，減輕總務 60% 配送負擔，提升企業 ESG 永續評鑑。",
        "kpi_boxes": "2,000 盒",
        "kpi_revenue": "NT$ 2,200,000",
        "kpi_margin": "56.5%",
        "pnl_net_margin": "38.5%",
        "kpi_satisfaction": "4.8 ★"
    }
    test_out = os.path.join(os.path.dirname(__file__), "test_presentation.pptx")
    build_tukuyi_pptx(demo_data, test_out)
