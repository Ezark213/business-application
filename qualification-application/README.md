# 資格取得申請システム（M365）

## 概要
従業員の資格取得申請をMicrosoft 365で電子化するシステム

## システム構成
- **SharePoint Lists**: データ管理（資格マスタ、資格取得申請）
- **Power Apps**: 申請フォーム
- **Power Automate**: 承認ワークフロー + Teams通知

## 主な機能
- 資格名＋詳細（級）による正確な報奨金表示
- 事前申請ボーナス（+5,000円）対応
- 受験料相当額表示（報奨金0円の資格用）
- 申請種別に応じた動的ラベル切り替え

## 申請フロー
1. 従業員が資格取得を決意 → 宣言届を申請（事前申請で+5,000円）
2. 従業員が資格を取得 → 取得届を申請
3. 承認者にTeams通知 → 承認/却下
4. 結果が申請者に通知

## 報奨金表示パターン

| 報奨金 | 申請種別 | 表示 |
|--------|---------|------|
| 0円（FP3級など） | 資格取得宣言届 | ¥5,000（事前申請ボーナス）+ 受験料相当額 |
| 0円（FP3級など） | 資格取得届 | 受験料相当額 |
| 通常 | 資格取得宣言届 | ¥XX,XXX + ¥5,000（事前申請ボーナス） |
| 通常 | 資格取得届 | ¥XX,XXX |

## ファイル構成

### ドキュメント（Markdown）
- `01_sharepoint-lists.md` - SharePointリスト設計
- `02_power-apps.md` - Power Apps設計・作成手順
- `03_power-automate.md` - Power Automate設計・作成手順
- `04_teams-notification.md` - Teams通知設定

### HTMLガイド（初心者向け）
- `power-apps-improvement-guide.html` - Power Apps改良ガイド
- `power-automate-improvement-guide.html` - Power Automate改良ガイド

### データ
- `data/qualification_master.csv` - 資格マスタサンプルデータ

## セットアップ手順

1. SharePointリストを作成（`01_sharepoint-lists.md`参照）
2. Power Appsでフォームを作成（`02_power-apps.md`参照）
3. Power Automateで承認フローを作成（`03_power-automate.md`参照）
4. テスト実行して動作確認

## 注意事項

### Power Apps
- Distinct関数使用後は `.Selected.Value` を使用
- 報奨金は `LookUp()` 関数で取得

### Power Automate
- トリガー直後に10秒の遅延を追加
- 「項目の更新」に報奨金額と事前ボーナスを含める
- 報奨金表示は「作成」アクションで生成
- SharePoint列の内部名は環境によって異なる場合あり

## 更新履歴

### 2026-01-15
- 詳細（級）ドロップダウン追加
- 4パターンの報奨金表示対応
- 受験料相当額表示対応
- 動的ラベル切り替え機能追加
- Power Automate: 遅延アクション追加、作成アクションで報奨金表示生成
