#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""マネーフォワード vs freee 比較資料 Excel生成スクリプト（修正版）"""

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
    ["税務申告（自社完結）", "★★☆☆☆", "★★★★★", "freeeは freee申告で自社完結"],
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

# ========== シート3: 税務申告（重要な修正） ==========
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
    ["法人税申告", "× 自社機能なし\n外部連携（達人シリーズ等）が必要", "◎ freee申告（法人税）\n自社ソフトで完結可能\n年額29,800円〜", "freee優位"],
    ["消費税申告", "× 自社機能なし\n外部連携（達人シリーズ等）が必要", "◎ freee申告（消費税）\nfreee会計に付帯\nインボイス対応・電子申告可", "freee優位"],
    ["所得税確定申告\n（個人事業主）", "○ クラウド確定申告で完結\ne-Tax対応", "◎ freee会計 確定申告機能\nスマホのみで申告可能", "freee優位"],
    ["所得税申告\n（税理士向け代理）", "× 自社機能なし\n外部連携が必要", "◎ freee申告（所得税）\nアドバイザー向け提供", "freee優位"],
    ["達人シリーズ連携", "◎ 2024年API連携実装\nワンクリックでデータ取込", "○ CSV/データ連携対応\n※freee申告があるため依存度低い", "MF優位"],
    ["電子申告対応", "△ 外部ソフト経由のみ", "◎ freee申告内で完結\n法人税+消費税一括送信可", "freee優位"],
    ["申告書作成の一体性", "△ 会計→外部ソフトで申告", "◎ 会計→申告まで自社完結\nデータ自動連携", "freee優位"],
]

for row_idx, row_data in enumerate(data, 4):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws3.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='center', wrap_text=True)

# 注記追加
ws3['A12'] = "【重要】freeeは「freee申告」で法人税・消費税・所得税の申告書作成から電子申告まで自社完結可能。"
ws3['A13'] = "マネーフォワードは自社で税務申告ソフトを持たないため、達人シリーズ等の外部ソフトが必須。"
ws3['A14'] = "会計事務所が達人シリーズを既に導入済みの場合はMFでも問題ないが、新規導入ならfreeeが有利。"

ws3.column_dimensions['A'].width = 22
ws3.column_dimensions['B'].width = 38
ws3.column_dimensions['C'].width = 38
ws3.column_dimensions['D'].width = 15

# ========== シート4: freee申告 詳細（新規追加） ==========
ws3b = wb.create_sheet("freee申告 詳細")

ws3b.merge_cells('A1:C1')
ws3b['A1'] = "freee申告 プラン・機能一覧"
ws3b['A1'].font = Font(bold=True, size=14)

headers = ["プラン名", "年額（税別）", "主な機能"]
for col, header in enumerate(headers, 1):
    cell = ws3b.cell(row=3, column=col, value=header)
    cell.font = font_header
    cell.fill = header_fill_freee
    cell.border = thin_border

data = [
    ["freee申告 法人税スターター", "29,800円", "法人税確定申告\n電子申告対応"],
    ["freee申告 法人税スタンダード", "48,800円", "法人税確定申告\n+高度な機能"],
    ["freee申告 法人税アドバンス", "要問合せ", "資本金1億円超対応\n固定資産100件以上対応"],
    ["freee申告 消費税", "freee会計に付帯", "消費税申告書作成\n電子申告・インボイス対応"],
    ["freee申告 所得税", "アドバイザー向け", "税理士の代理申告用\n一括電子申告可"],
    ["freee申告 償却資産", "59,800円", "償却資産申告書作成\neLTAX電子申告対応"],
    ["freee申告 内訳書・概況書", "別途契約", "勘定科目内訳明細書\n法人事業概況説明書"],
    ["freee申告 年調・法定調書", "freee人事労務に付帯", "年末調整\n法定調書合計表"],
]

for row_idx, row_data in enumerate(data, 4):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws3b.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='center', wrap_text=True)

# 注記
ws3b['A14'] = "【freee申告の強み】"
ws3b['A15'] = "・freee会計からデータ自動連携（当期純利益・交際費・固定資産等）"
ws3b['A16'] = "・帳票間の数字連携がツリー形式で表示され、整合性確認が容易"
ws3b['A17'] = "・法人税+消費税の一括電子申告が可能（アドバイザー向け）"
ws3b['A18'] = "・eLTAX/e-Taxインストール不要で電子申告可能"

ws3b['A20'] = "【注意事項】"
ws3b['A21'] = "・資本金1億円超の法人はアドバンスプランが必要"
ws3b['A22'] = "・電気・ガス供給業、保険業は対応外（保険代理店は可）"
ws3b['A23'] = "・修正申告・予定申告はスターター/スタンダードでは不可"

ws3b.column_dimensions['A'].width = 30
ws3b.column_dimensions['B'].width = 22
ws3b.column_dimensions['C'].width = 35

# ========== シート5: 償却資産申告 ==========
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
    ["償却資産申告書作成", "× 自社機能なし\n減価償却の達人等へデータ出力", "◎ freee申告 償却資産\nソフト内で申告書作成可能", "freee優位"],
    ["電子申告（eLTAX）", "× 外部ソフト経由のみ", "◎ freee内で完結\neLTAXインストール不要", "freee優位"],
    ["追加費用", "達人シリーズ等の費用が別途必要", "年額59,800円（税別）\n※アドバイザー契約者は追加不要", "条件による"],
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

# ========== シート6: 給与・労務 ==========
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
    ["年末調整", "クラウド年末調整\nWeb完結・e-Tax対応", "freee申告 年調・法定調書\n人事労務に付帯", "同等"],
    ["社会保険手続き", "クラウド社会保険\n算定基礎届・月変届出力", "人事労務freee内\n算定基礎届・月変届出力", "同等"],
    ["法定調書", "○ 給与支払報告書・源泉徴収票\ne-Tax/eLTAX連携", "◎ freee申告 年調・法定調書\n法定調書合計表まで対応", "freee優位"],
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

# ========== シート7: 経費精算 ==========
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

# ========== シート8: 請求・支払 ==========
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

# ========== シート9: 料金プラン ==========
ws8 = wb.create_sheet("料金プラン")

ws8.merge_cells('A1:E1')
ws8['A1'] = "料金プラン比較（法人向け・税抜）"
ws8['A1'].font = Font(bold=True, size=14)

# 会計ソフト料金
ws8['A3'] = "【会計ソフト】"
ws8['A3'].font = font_header

headers = ["プラン", "MF月額", "MF年額", "freee月額", "freee年額"]
for col, header in enumerate(headers, 1):
    cell = ws8.cell(row=4, column=col, value=header)
    cell.font = font_header
    cell.fill = header_fill_gray
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center')

data = [
    ["スモール/スターター", "3,980円", "35,760円", "4,780円", "47,760円"],
    ["ビジネス/スタンダード", "5,980円", "59,760円", "9,280円", "95,760円"],
    ["エンタープライズ等", "要問合せ", "要問合せ", "要問合せ", "要問合せ"],
]

for row_idx, row_data in enumerate(data, 5):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws8.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center', vertical='center')

# 申告ソフト料金
ws8['A10'] = "【税務申告ソフト】"
ws8['A10'].font = font_header

headers2 = ["項目", "マネーフォワード", "freee"]
for col, header in enumerate(headers2, 1):
    cell = ws8.cell(row=11, column=col, value=header)
    cell.font = font_header
    cell.fill = header_fill_gray
    cell.border = thin_border

data2 = [
    ["法人税申告", "自社機能なし\n（達人シリーズ等が別途必要）", "freee申告 年額29,800円〜"],
    ["消費税申告", "自社機能なし\n（達人シリーズ等が別途必要）", "freee会計に付帯（追加費用なし）"],
    ["償却資産申告", "自社機能なし\n（達人シリーズ等が別途必要）", "freee申告 年額59,800円"],
]

for row_idx, row_data in enumerate(data2, 12):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws8.cell(row=row_idx, column=col_idx, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(vertical='center', wrap_text=True)

# 注記
ws8['A17'] = "※料金は2025年1月時点。最新料金は各社公式サイトをご確認ください。"
ws8['A18'] = "※freeeは2024年7月に価格改定あり。クラウドソフトは価格改定リスクがあります。"
ws8['A19'] = "※MFで税務申告を行う場合、達人シリーズ等の費用が別途発生します。"

ws8.column_dimensions['A'].width = 25
ws8.column_dimensions['B'].width = 30
ws8.column_dimensions['C'].width = 30
ws8.column_dimensions['D'].width = 15
ws8.column_dimensions['E'].width = 15

# ========== シート10: 市場シェア ==========
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

# ========== シート11: 推奨シナリオ ==========
ws10 = wb.create_sheet("推奨シナリオ")

ws10.merge_cells('A1:B1')
ws10['A1'] = "推奨シナリオ"
ws10['A1'].font = Font(bold=True, size=14)

ws10['A3'] = "マネーフォワードが向いているケース"
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
    "税務申告は達人シリーズで行う前提",
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
    "会計から税務申告まで自社完結したい",
    "達人シリーズを持っていない（新規導入）",
    "API連携で独自システムと接続",
]

for idx, case in enumerate(freee_cases, 4):
    ws10[f'B{idx}'] = f"・{case}"

# 結論
ws10['A15'] = "【会計事務所としての結論】"
ws10['A15'].font = Font(bold=True, size=12)
ws10.merge_cells('A16:B16')
ws10['A16'] = "freeeは「freee申告」で税務申告まで自社完結できるのが大きな強み。"
ws10.merge_cells('A17:B17')
ws10['A17'] = "達人シリーズを既に導入済みの事務所はMFでも問題ないが、新規導入ならfreeeが有利。"
ws10.merge_cells('A18:B18')
ws10['A18'] = "顧問先の規模・業種・ITリテラシーに応じて使い分けるのが現実的。"

ws10.column_dimensions['A'].width = 45
ws10.column_dimensions['B'].width = 45

# 保存
output_path = r"C:\Users\yiwao\business-application\ms-expense-app\docs\mf-freee-comparison.xlsx"
wb.save(output_path)
print(f"Excelファイルを作成しました: {output_path}")
