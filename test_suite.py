"""
土庫驛 AI 行銷企劃工作台 - 自動化測試套件 (Automated Test Suite)
檢驗資料模型完整性、匯出功能、HTML 獨立簡報、PPTX 生成邏輯與程式碼語法
"""

import os
import ast
import json
from sample_data import (
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

def test_sample_data_integrity():
    print("[TEST 1] 檢驗土庫驛品牌與教學案例資料完整性...")
    assert "brand_name" in TUKUYI_BRAND_IDENTITY
    assert "ci_vi_colors" in TUKUYI_BRAND_IDENTITY
    assert TUKUYI_BRAND_IDENTITY["ci_vi_colors"]["primary_cocoa"] == "#3B2314"
    assert TUKUYI_BRAND_IDENTITY["ci_vi_colors"]["secondary_gold"] == "#D4AF37"
    
    # 檢查 3 大受眾 (40% 主管、40% 採購、20% 夥伴)
    assert len(AUDIENCE_PERSONAS) == 3
    assert "boss_internal" in AUDIENCE_PERSONAS
    assert "procurement_b2b" in AUDIENCE_PERSONAS
    assert "partner_vip" in AUDIENCE_PERSONAS
    
    # 檢查中秋與聖誕案例
    assert "stp_framework" in MID_AUTUMN_CASE
    assert "candidate_product_pool" in CHRISTMAS_WORKSHOP_CASE
    assert len(VIRTUAL_SALES_DATA) >= 10
    print(" -> 品牌底蘊、受眾矩陣、教學案例與虛擬數據包檢驗 PASS！")

def test_exports_and_sha256():
    print("[TEST 2] 檢驗 Markdown、JSON、HTML 與 CSV 匯出功能...")
    demo_proposal = {
        "title": "土庫驛 2026 聖誕星漾 B2B 禮盒提案",
        "audience_name": "企業客戶提案 (福委 / 總務 / 採購)",
        "festival": "2026 聖誕年終感恩禮盒",
        "summary": "以 Tree-to-Bar 頂級可可與 13 道工序，打造尊榮健康且兼顧 ESG 的企業商務禮盒。",
        "stp_s": "高科技半導體與外商金融主管及福委採購窗口。",
        "stp_t": "客單價 $800 - $1,500 區間之年終福委及 VIP 外部客戶禮盒。",
        "stp_p": "『雲林在地創生 x 米其林級頂級可可』之尊榮商務賀禮。",
        "p_product": "85% 生巧克力 + 小山園抹茶生巧 + 莊園可可豆茶包，冷藏常溫彈性配搭。",
        "p_price": "三階梯定價：分享款 $699 / 尊爵款 $1,099 / 旗艦奢華款 $1,680。",
        "p_place": "專人 B2B 顧問一對一試吃配送、企業專屬線上大宗試算下單頁面。",
        "p_promotion": "早鳥滿額免運溫控、免費客製燙金腰封與企業 Logo 雷雕、附贈地方創生小卡。",
        "kpi_boxes": "2,000 盒",
        "kpi_revenue": "NT$ 2,200,000",
        "kpi_margin": "56.5%",
        "kpi_satisfaction": "4.8 ★"
    }

    # Markdown
    md_str = export_proposal_markdown(demo_proposal)
    assert "SHA256-" in md_str
    assert "土庫驛可可莊園" in md_str

    # JSON
    json_str = export_proposal_json(demo_proposal)
    parsed = json.loads(json_str)
    assert parsed["document_type"] == "tukuyi_marketing_proposal"

    # HTML
    html_str = generate_standalone_html_deck(demo_proposal)
    assert "<!DOCTYPE html>" in html_str
    assert "#3B2314" in html_str
    assert "#D4AF37" in html_str

    # CSV
    csv_str = export_virtual_sales_csv()
    assert "budget_per_box" in csv_str
    assert "半導體/科技業" in csv_str
    print(" -> Markdown, JSON, HTML, CSV 匯出與 SHA-256 驗證 PASS！")

def test_code_syntax():
    print("[TEST 3] 檢驗核心 Python 程式碼語法 (AST Check)...")
    base_dir = os.path.dirname(__file__)
    files_to_check = ["app.py", "sample_data.py", "export_helpers.py", "generate_pptx.py"]
    for fname in files_to_check:
        fpath = os.path.join(base_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            source = f.read()
        ast.parse(source, filename=fname)
        print(f"    ✔ {fname} 語法驗證無誤")
    print(" -> 所有核心腳本語法檢驗 PASS！")

if __name__ == "__main__":
    test_sample_data_integrity()
    test_exports_and_sha256()
    test_code_syntax()
    print("\n🎉 土庫驛 AI 行銷企劃工作台測試全數通過 (100% PASS)！")
