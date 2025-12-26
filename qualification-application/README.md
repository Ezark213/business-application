# 資格取得申請システム（M365）

## 概要
従業員の資格取得申請をMicrosoft 365で電子化するシステム

## システム構成
- SharePoint Lists: データ管理
- Power Apps: 申請フォーム
- Power Automate: 承認ワークフロー + Teams通知

## 申請フロー
1. 従業員が資格取得を決意 → 宣言届を申請（事前申請で+5,000円）
2. 従業員が資格を取得 → 取得届を申請
3. 承認者にTeams通知 → 承認/却下
4. 結果が申請者に通知

## ファイル構成
- `01_sharepoint-lists.md` - SharePointリスト設計
- `02_power-apps.md` - Power Apps設計・作成手順
- `03_power-automate.md` - Power Automate設計・作成手順
- `04_teams-notification.md` - Teams通知設定
