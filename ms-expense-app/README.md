# MS 経費申請アプリ (MS Expense App)

## 概要

既存のPython製経費計上アプリ（[expense-app](https://github.com/Ezark213/expense-app)）をMicrosoft 365エコシステムに移行したアプリケーションです。

### 主な特徴

- **Power Apps** によるモダンなUI
- **SharePoint Lists** によるデータ管理
- **Power Automate** による承認ワークフロー
- **Microsoft Teams** への通知連携
- **SharePoint** ドキュメントライブラリでの領収書管理
- **インボイス制度対応** 8パターンの税区分に対応

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
├── README.md                           # このファイル
├── docs/
│   ├── M365経費申請アプリ構築手順.html  # ★ 構築手順書（HTML）
│   ├── architecture.md                 # 詳細アーキテクチャ
│   ├── setup-guide.md                  # セットアップ手順
│   ├── step-by-step-guide.html         # ステップバイステップガイド
│   ├── step-by-step-guide.md           # ステップバイステップガイド(MD)
│   ├── user-manual.md                  # ユーザーマニュアル
│   ├── mf-freee-comparison.html        # 会計ソフト比較
│   └── mf-freee-comparison.xlsx        # 会計ソフト比較(Excel)
├── sharepoint/
│   ├── lists-schema.json               # SharePoint Listsスキーマ
│   └── data/
│       ├── ExpenseRequests.csv         # ★ 経費申請リスト（インポート用）
│       └── TaxRates.csv                # ★ 税区分マスター（インポート用）
├── power-automate/
│   ├── approval-flow.json              # 承認フロー定義
│   └── teams-notification.json         # Teams通知フロー
├── power-apps/
│   └── app-definition.json             # アプリ定義
└── old/                                # 旧ファイル・参考資料
```

## クイックスタート

### 1. 必要なライセンス

- Microsoft 365 Business Basic以上
- Power Apps ライセンス（Microsoft 365に含まれるStandard版で可）
- Power Automate ライセンス（承認フロー用）

### 2. 構築手順

詳細な構築手順は以下のファイルを参照してください：

- **[M365経費申請アプリ構築手順.html](docs/M365経費申請アプリ構築手順.html)** - 誰にでもわかるステップバイステップガイド

### 3. SharePointリストのインポート

以下のCSVファイルをSharePointにインポートしてリストを作成します：

| ファイル | 説明 |
|---------|------|
| [ExpenseRequests.csv](sharepoint/data/ExpenseRequests.csv) | 経費申請データ用リスト |
| [TaxRates.csv](sharepoint/data/TaxRates.csv) | 税区分マスター（8パターン） |

### 税区分一覧（TaxRates.csv）

| 税区分 | 税率 | 控除割合 |
|--------|------|----------|
| 10%・適格（インボイス） | 10.00% | 100.00% |
| 10%・区分記載（経過措置80%） | 10.00% | 80.00% |
| 10%・区分記載（経過措置50%） | 10.00% | 50.00% |
| 8%（軽減税率）・適格（インボイス） | 8.00% | 100.00% |
| 8%（軽減税率）・区分記載（経過措置80%） | 8.00% | 80.00% |
| 8%（軽減税率）・区分記載（経過措置50%） | 8.00% | 50.00% |
| 非課税 | 0.00% | - |
| 不課税 | 0.00% | - |

## 機能一覧

| 機能 | 元アプリ (Python) | MS版 |
|------|-------------------|------|
| 経費登録 | Tkinter Form | Power Apps Canvas |
| データ保存 | CSV | SharePoint Lists |
| 税計算 | Python Decimal | Power Fx |
| 承認フロー | なし | Power Automate Approvals |
| 通知 | なし | Teams + Outlook |
| 領収書添付 | ローカルファイル | SharePoint/OneDrive |
| 会計ソフト出力 | CSV Export | Power Automate + Excel |

## 関連リポジトリ

- [expense-app](https://github.com/Ezark213/expense-app) - 元のPython製デスクトップアプリ

## ライセンス

MIT License
