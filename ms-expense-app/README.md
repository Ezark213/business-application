# MS 経費申請アプリ (MS Expense App)

## 概要

既存のPython製経費計上アプリをMicrosoft 365エコシステムに移行したアプリケーションです。

### 主な特徴

- **Power Apps** によるモダンなUI
- **SharePoint Lists** によるデータ管理
- **Power Automate** による承認ワークフロー
- **Microsoft Teams** への通知連携
- **SharePoint** ドキュメントライブラリでの領収書管理

## アーキテクチャ

```
┌─────────────────────────────────────────────────────────────────┐
│                        Microsoft 365                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │  Power Apps  │───▶│   SharePoint │◀───│   OneDrive   │     │
│  │  (Frontend)  │    │   Lists      │    │  (添付資料)  │     │
│  └──────┬───────┘    └──────┬───────┘    └──────────────┘     │
│         │                   │                                  │
│         ▼                   ▼                                  │
│  ┌──────────────────────────────────────┐                     │
│  │         Power Automate               │                     │
│  │  ┌────────────┐  ┌────────────────┐  │                     │
│  │  │ 承認フロー │  │ Teams通知     │  │                     │
│  │  └────────────┘  └────────────────┘  │                     │
│  └──────────────────────────────────────┘                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## フォルダ構成

```
ms-expense-app/
├── README.md                 # このファイル
├── docs/
│   ├── architecture.md       # 詳細アーキテクチャ
│   ├── setup-guide.md        # セットアップ手順
│   └── user-manual.md        # ユーザーマニュアル
├── sharepoint/
│   ├── lists-schema.json     # SharePoint Listsスキーマ
│   └── site-template.xml     # サイトテンプレート
├── power-automate/
│   ├── approval-flow.json    # 承認フロー定義
│   └── teams-notification.json # Teams通知フロー
└── power-apps/
    ├── app-definition.json   # アプリ定義
    └── screens/              # 画面設計
```

## 必要なライセンス

- Microsoft 365 Business Basic以上
- Power Apps ライセンス（Microsoft 365に含まれるStandard版で可）
- Power Automate ライセンス（承認フロー用）

## 機能一覧

| 機能 | 元アプリ | MS版 |
|------|---------|------|
| 経費登録 | Tkinter Form | Power Apps Canvas |
| データ保存 | CSV | SharePoint Lists |
| 税計算 | Python Decimal | Power Fx |
| 承認フロー | なし | Power Automate Approvals |
| 通知 | なし | Teams + Outlook |
| 領収書添付 | ローカルファイル | SharePoint/OneDrive |
| 会計ソフト出力 | CSV Export | Power Automate + Excel |

## セットアップ手順

詳細は [docs/setup-guide.md](docs/setup-guide.md) を参照してください。

## ライセンス

MIT License
