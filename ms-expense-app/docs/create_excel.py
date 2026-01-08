#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""マネーフォワード vs freee 比較資料 Excel生成スクリプト"""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill, NamedStyle
from openpyxl.utils import get_column_letter

# ワークブック作成
wb = Workbook()

# スタイル定義
header_fill_mf = PatternFill(start_color="E8F0FE", end_color="E8F0FE", fill_type="solid")
header_fill_freee = PatternFill(start_color="E6F7ED", end_color="E6F7ED", fill_type="solid")
header_fill_gray = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")
header_fill_purple = PatternFill(start_color="667EEA", end_color="667EEA", fill_type="solid")

thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

font_header = Font(bold=True, size=11)
font_title = Font(bold=True, size=14)
font_mf = Font(bold=True, color="3B7DE9")
font_freee = Font(bold=True, color="00AA4F")

# ========== シート1: 総合比較 ==========
ws1 = wb.active
ws1.title = "総合比較"

# タイトル
ws1.merge_cells('A1:D1')
ws1['A1'] = "マネーフォワード vs freee 総合比較表"
ws1['A1'].font = Font(bold=True, size=16)
ws1['A1'].alignment = Alignment(horizontal='center')

# ヘッダー
headers = ["比較項目", "マネーフォワード", "freee", "備考"]
for col, header in enumerate(headers, 1):
    cell = ws1.cell(row=3, column=col, value=header)
    cell.font = font_header
    cell.fill = header_fill_gray
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center', vertical='center')

# データ
data = [
    ["記帳効率（大量取引）", "★★★☆☆", "★★★★★", "freeeは自動登録機能あり"],
    ["会計事務所との親和性", "★★★★★", "★★★☆☆", "MFは従来の複式簿記UI"],
    ["税務申告連携", "★★★★★", "★★★★☆", "MFは達人とAPI連携強化"],
    ["償却資産申告", "★★★☆☆", "★★★★★", "freeeは電子申告まで完結"],
    ["給与・労務一体性", "★★★★☆", "★★★★★", "freeeはオールインワン"],
    ["初心者の使いやすさ", "★★★☆☆", "★★★★★", "freeeは簿記知識不要"],
    ["拡張性・API", "★★★☆☆", "★★★★★", "freeeはAPI完全公開"],
    ["コストパフォーマンス", "★★★★☆", "★★★☆☆", "freeeは価格改定リスクあり"],
]

for row_idx, row_data in enumerate(data, 4):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws1.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='center', wrap_text=True)
        if col_idx == 2:
            cell.font = font_mf
        elif col_idx == 3:
            cell.font = font_freee

# 列幅調整
ws1.column_dimensions['A'].width = 25
ws1.column_dimensions['B'].width = 18
ws1.column_dimensions['C'].width = 18
ws1.column_dimensions['D'].width = 35

# ========== シート2: 会計入力・記帳 ==========
ws2 = wb.create_sheet("会計入力・記帳")

ws2.merge_cells('A1:D1')
ws2['A1'] = "会計入力・記帳効率の比較"
ws2['A1'].font = Font(bold=True, size=14)

headers = ["項目", "マネーフォワード", "freee", "評価"]
for col, header in enumerate(headers, 1):
    cell = ws2.cell(row=3, column=col, value=header)
    cell.font = font_header
    cell.fill = header_fill_gray
    cell.border = thin_border

data = [
    ["UI設計思想", "従来の複式簿記に準拠\n経理経験者・税理士向け", "簿記知識不要の独自UI\n初心者・スタートアップ向け", "用途による"],
    ["仕訳入力方式", "貸借科目を明示する従来型\n仕訳帳イメージで入力", "取引登録型（家計簿感覚）\n貸借を意識させない設計", "用途による"],
    ["自動仕訳", "推測までで「登録ボタン」が必要\n一括登録は可能", "ルール設定で完全自動登録可能\n大量取引に強み", "freee優位"],
    ["銀行連携数", "2,300以上\n未確定明細も取込可能", "主要金融機関対応", "MF優位"],
    ["AI学習機能", "科目推測の精度向上", "科目推測の精度向上", "同等"],
    ["クレジットカード連携", "未確定明細も取込可能\nリアルタイム性が高い", "確定明細のみ", "MF優位"],
]

for row_idx, row_data in enumerate(data, 4):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws2.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='center', wrap_text=True)

ws2.column_dimensions['A'].width = 20
ws2.column_dimensions['B'].width = 35
ws2.column_dimensions['C'].width = 35
ws2.column_dimensions['D'].width = 15

# ========== シート3: 税務申告 ==========
ws3 = wb.create_sheet("税務申告")

ws3.merge_cells('A1:D1')
ws3['A1'] = "税務申告対応の比較"
ws3['A1'].font = Font(bold=True, size=14)

headers = ["項目", "マネーフォワード", "freee", "評価"]
for col, header in enumerate(headers, 1):
    cell = ws3.cell(row=3, column=col, value=header)
    cell.font = font_header
    cell.fill = header_fill_gray
    cell.border = thin_border

data = [
    ["法人税申告", "外部連携（達人シリーズ等）\nAPI連携で自動データ取込", "外部連携（達人シリーズ等）\nCSV/API連携対応", "MF優位"],
    ["消費税申告", "外部連携（消費税の達人等）\n消費税集計データ出力", "外部連携（消費税の達人等）\n消費税集計データ出力", "同等"],
    ["所得税確定申告", "クラウド確定申告で完結\ne-Tax対応", "確定申告freeeで完結\nスマホのみで申告可能", "freee優位"],
    ["達人シリーズ連携", "2024年API連携実装\nワンクリックでデータ取込", "2013年〜連携対応\nCSV/データ連携", "MF優位"],
    ["電子申告対応", "外部ソフト経由", "外部ソフト経由", "同等"],
]

for row_idx, row_data in enumerate(data, 4):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws3.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='center', wrap_text=True)

ws3.column_dimensions['A'].width = 20
ws3.column_dimensions['B'].width = 35
ws3.column_dimensions['C'].width = 35
ws3.column_dimensions['D'].width = 15

# ========== シート4: 償却資産申告 ==========
ws4 = wb.create_sheet("償却資産申告")

ws4.merge_cells('A1:D1')
ws4['A1'] = "償却資産申告の比較"
ws4['A1'].font = Font(bold=True, size=14)

headers = ["項目", "マネーフォワード", "freee", "評価"]
for col, header in enumerate(headers, 1):
    cell = ws4.cell(row=3, column=col, value=header)
    cell.font = font_header
    cell.fill = header_fill_gray
    cell.border = thin_border

data = [
    ["固定資産台帳", "○ 標準機能で対応", "○ 標準機能で対応", "同等"],
    ["減価償却自動計上", "○ 毎期自動仕訳", "○ 毎期自動仕訳", "同等"],
    ["償却資産申告書作成", "△ 外部ソフト連携\n減価償却の達人等へデータ出力", "◎ freee申告 償却資産\nソフト内で申告書作成可能", "freee優位"],
    ["電子申告（eLTAX）", "△ 外部ソフト経由", "◎ freee内で完結\neLTAXインストール不要", "freee優位"],
    ["追加費用", "達人シリーズ等の費用", "年額59,800円（税別）\n※アドバイザー契約者は追加不要", "条件による"],
]

for row_idx, row_data in enumerate(data, 4):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws4.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='center', wrap_text=True)

ws4.column_dimensions['A'].width = 22
ws4.column_dimensions['B'].width = 35
ws4.column_dimensions['C'].width = 35
ws4.column_dimensions['D'].width = 15

# ========== シート5: 給与・労務 ==========
ws5 = wb.create_sheet("給与・年末調整・労務")

ws5.merge_cells('A1:D1')
ws5['A1'] = "給与・年末調整・労務・社保・法定調書の比較"
ws5['A1'].font = Font(bold=True, size=14)

headers = ["項目", "マネーフォワード", "freee", "評価"]
for col, header in enumerate(headers, 1):
    cell = ws5.cell(row=3, column=col, value=header)
    cell.font = font_header
    cell.fill = header_fill_gray
    cell.border = thin_border

data = [
    ["給与計算", "クラウド給与\n勤怠連携対応", "人事労務freee\n会計と一体型", "freee優位"],
    ["年末調整", "クラウド年末調整\nWeb完結・e-Tax対応", "人事労務freee内\nWeb完結・e-Tax対応", "同等"],
    ["社会保険手続き", "クラウド社会保険\n算定基礎届・月変届出力", "人事労務freee内\n算定基礎届・月変届出力", "同等"],
    ["法定調書", "○ 給与支払報告書・源泉徴収票\ne-Tax/eLTAX連携", "○ 給与支払報告書・源泉徴収票\ne-Tax/eLTAX連携", "同等"],
    ["外部連携", "◎ SmartHR、Touch On Time等", "○ 主要サービス対応", "MF優位"],
    ["料金", "基本料金内 or 追加契約", "月額2,600円〜（5名まで）", "条件による"],
]

for row_idx, row_data in enumerate(data, 4):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws5.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='center', wrap_text=True)

ws5.column_dimensions['A'].width = 20
ws5.column_dimensions['B'].width = 35
ws5.column_dimensions['C'].width = 35
ws5.column_dimensions['D'].width = 15

# ========== シート6: 経費精算 ==========
ws6 = wb.create_sheet("経費精算")

ws6.merge_cells('A1:D1')
ws6['A1'] = "経費精算の比較"
ws6['A1'].font = Font(bold=True, size=14)

headers = ["項目", "マネーフォワード", "freee", "評価"]
for col, header in enumerate(headers, 1):
    cell = ws6.cell(row=3, column=col, value=header)
    cell.font = font_header
    cell.fill = header_fill_gray
    cell.border = thin_border

data = [
    ["サービス形態", "クラウド経費（別契約）", "freee会計内蔵 / freee経費精算", "freee優位"],
    ["領収書読取", "◎ AI-OCR高精度\n使うほど学習", "◎ AI-OCR対応\n税区分・金額自動入力", "同等"],
    ["申請・承認", "○ スマホ完結", "◎ スマホ・LINE対応", "freee優位"],
    ["会計連携", "○ 仕訳自動計上", "◎ シームレス連携", "freee優位"],
    ["振込データ作成", "○ 対応", "○ 対応", "同等"],
    ["電子帳簿保存法", "○ JIIMA認証取得", "○ JIIMA認証取得", "同等"],
]

for row_idx, row_data in enumerate(data, 4):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws6.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='center', wrap_text=True)

ws6.column_dimensions['A'].width = 20
ws6.column_dimensions['B'].width = 35
ws6.column_dimensions['C'].width = 35
ws6.column_dimensions['D'].width = 15

# ========== シート7: 請求・支払 ==========
ws7 = wb.create_sheet("請求・支払")

ws7.merge_cells('A1:D1')
ws7['A1'] = "請求・支払の比較"
ws7['A1'].font = Font(bold=True, size=14)

headers = ["項目", "マネーフォワード", "freee", "評価"]
for col, header in enumerate(headers, 1):
    cell = ws7.cell(row=3, column=col, value=header)
    cell.font = font_header
    cell.fill = header_fill_gray
    cell.border = thin_border

data = [
    ["請求書発行", "クラウド請求書（別契約）", "freee請求書（内蔵機能）", "freee優位"],
    ["見積書作成", "○ 対応", "○ 対応", "同等"],
    ["デザインテンプレート", "標準テンプレート", "◎ 40種類以上", "freee優位"],
    ["定期請求・一括請求", "○ 対応", "○ 上位プランで対応", "同等"],
    ["入金消込・督促", "◎ 自動化機能あり", "○ 対応", "MF優位"],
    ["会計連携", "◎ 仕訳自動連携\n二重入力防止", "◎ シームレス連携", "同等"],
    ["インボイス制度対応", "○ 適格請求書対応", "○ 適格請求書対応", "同等"],
]

for row_idx, row_data in enumerate(data, 4):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws7.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='center', wrap_text=True)

ws7.column_dimensions['A'].width = 22
ws7.column_dimensions['B'].width = 35
ws7.column_dimensions['C'].width = 35
ws7.column_dimensions['D'].width = 15

# ========== シート8: 料金プラン ==========
ws8 = wb.create_sheet("料金プラン")

ws8.merge_cells('A1:E1')
ws8['A1'] = "料金プラン比較（法人向け・税抜）"
ws8['A1'].font = Font(bold=True, size=14)

headers = ["プラン", "MF月額", "MF年額", "freee月額", "freee年額"]
for col, header in enumerate(headers, 1):
    cell = ws8.cell(row=3, column=col, value=header)
    cell.font = font_header
    cell.fill = header_fill_gray
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center')

data = [
    ["スモール/スターター", "3,980円", "35,760円", "4,780円", "47,760円"],
    ["ビジネス/スタンダード", "5,980円", "59,760円", "9,280円", "95,760円"],
    ["エンタープライズ等", "要問合せ", "要問合せ", "要問合せ", "要問合せ"],
]

for row_idx, row_data in enumerate(data, 4):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws8.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center', vertical='center')

# 注記
ws8['A8'] = "※料金は2025年1月時点。最新料金は各社公式サイトをご確認ください。"
ws8['A9'] = "※freeeは2024年7月に価格改定あり。クラウドソフトは価格改定リスクがあります。"

ws8.column_dimensions['A'].width = 25
ws8.column_dimensions['B'].width = 15
ws8.column_dimensions['C'].width = 15
ws8.column_dimensions['D'].width = 15
ws8.column_dimensions['E'].width = 15

# ========== シート9: 市場シェア ==========
ws9 = wb.create_sheet("市場シェア")

ws9.merge_cells('A1:C1')
ws9['A1'] = "クラウド会計ソフト市場シェア（2025年）"
ws9['A1'].font = Font(bold=True, size=14)

# 法人向け
ws9['A3'] = "【法人向けクラウド会計シェア】"
ws9['A3'].font = font_header

headers = ["ソフト", "シェア", "順位"]
for col, header in enumerate(headers, 1):
    cell = ws9.cell(row=4, column=col, value=header)
    cell.font = font_header
    cell.fill = header_fill_gray
    cell.border = thin_border

data = [
    ["freee", "32.3%", "1位"],
    ["マネーフォワード", "19.2%", "2位"],
    ["弥生シリーズ", "15.4%", "3位"],
    ["その他", "33.1%", "-"],
]

for row_idx, row_data in enumerate(data, 5):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws9.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border

# 個人向け
ws9['A11'] = "【個人事業主向けシェア】"
ws9['A11'].font = font_header

for col, header in enumerate(headers, 1):
    cell = ws9.cell(row=12, column=col, value=header)
    cell.font = font_header
    cell.fill = header_fill_gray
    cell.border = thin_border

data = [
    ["弥生シリーズ", "55.4%", "1位"],
    ["freee", "24.0%", "2位"],
    ["マネーフォワード", "14.3%", "3位"],
    ["その他", "6.3%", "-"],
]

for row_idx, row_data in enumerate(data, 13):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws9.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border

ws9['A19'] = "出典: MM総研 2025年3月末調査"

ws9.column_dimensions['A'].width = 20
ws9.column_dimensions['B'].width = 12
ws9.column_dimensions['C'].width = 10

# ========== シート10: 推奨シナリオ ==========
ws10 = wb.create_sheet("推奨シナリオ")

ws10.merge_cells('A1:B1')
ws10['A1'] = "推奨シナリオ"
ws10['A1'].font = Font(bold=True, size=14)

ws10['A3'] = "マネーフォワードが向いているケース"
ws10['A3'].font = font_mf
ws10['A3'].font = Font(bold=True, size=12, color="3B7DE9")

mf_cases = [
    "経理経験者・税理士が操作する",
    "従来の会計ソフトからの移行",
    "達人シリーズを既に導入済み",
    "銀行・カード連携を重視",
    "中規模以上の法人顧問先",
    "SmartHR等の労務システムと連携したい",
    "安定した料金体系を重視",
    "会計事務所主導で記帳代行",
]

for idx, case in enumerate(mf_cases, 4):
    ws10[f'A{idx}'] = f"・{case}"

ws10['B3'] = "freeeが向いているケース"
ws10['B3'].font = Font(bold=True, size=12, color="00AA4F")

freee_cases = [
    "簿記知識のない経営者が自ら入力",
    "スタートアップ・小規模法人",
    "取引数が多く自動化を重視",
    "スマホ完結を求める",
    "POSレジ・EC連携が必要",
    "オールインワンでシンプルに運用",
    "償却資産申告まで一貫対応したい",
    "API連携で独自システムと接続",
]

for idx, case in enumerate(freee_cases, 4):
    ws10[f'B{idx}'] = f"・{case}"

ws10.column_dimensions['A'].width = 45
ws10.column_dimensions['B'].width = 45

# 保存
output_path = r"C:\Users\yiwao\business-application\ms-expense-app\docs\mf-freee-comparison.xlsx"
wb.save(output_path)
print(f"Excelファイルを作成しました: {output_path}")
