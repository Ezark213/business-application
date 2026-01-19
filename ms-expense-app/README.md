# MS 経費申請アプリ (MS Expense App)

## 概要

既存のPython製経費計上アプリ（[expense-app](https://github.com/Ezark213/expense-app)）をMicrosoft 365エコシステムに移行したアプリケーションです。

**本システムは「複数の経費をまとめて1回で申請」する設計（ヘッダー・明細方式）です。**

### 主な特徴

- **Power Apps** によるモダンなUI
- **SharePoint Lists** によるデータ管理（申請ヘッダー + 経費明細）
- **Power Automate** による承認ワークフロー
- **Microsoft Teams** への通知連携
- **インボイス制度対応** 8パターンの税区分に対応

## データ構造

```
┌─────────────────────────────┐     ┌─────────────────────────────┐
│  ExpenseRequests            │     │  ExpenseDetails             │
│  （申請ヘッダー）            │     │  （経費明細）               │
├─────────────────────────────┤     ├─────────────────────────────┤
│  1申請 = 1レコード          │◀────│  1経費 = 1レコード          │
│                             │     │                             │
│  ・申請者                   │     │  ・申請ID（参照）           │
│  ・申請日                   │     │  ・経費日付                 │
│  ・部署                     │     │  ・勘定科目                 │
│  ・明細件数（自動計算）     │     │  ・内容                     │
│  ・合計金額（自動計算）     │     │  ・税込金額                 │
│  ・承認ステータス           │     │  ・税区分                   │
│  ・承認者/承認日時          │     │  ・税額/税抜金額            │
└─────────────────────────────┘     │  ・インボイス番号           │
                                    │  ・領収書                   │
                                    └─────────────────────────────┘
```

## 運用フロー

1. 申請者が「新規申請」を作成（ExpenseRequestsに1レコード作成）
2. 経費を1件ずつ追加（ExpenseDetailsに複数レコード作成）
3. すべての経費を入力したら「申請する」ボタンで一括申請
4. 承認者は申請単位で承認/却下

## フォルダ構成

```
ms-expense-app/
├── README.md                           # このファイル
├── docs/
│   ├── M365経費申請アプリ構築手順.html  # ★ 構築手順書（HTML）
│   └── ...
├── sharepoint/
│   ├── lists-schema.json               # SharePoint Listsスキーマ
│   └── data/
│       ├── ExpenseRequests.csv         # ★ 申請ヘッダー（インポート用）
│       ├── ExpenseDetails.csv          # ★ 経費明細（インポート用）
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

以下の3つのCSVファイルをSharePointにインポートしてリストを作成します：

| ファイル | 説明 |
|---------|------|
| [ExpenseRequests.csv](sharepoint/data/ExpenseRequests.csv) | 申請ヘッダー用リスト |
| [ExpenseDetails.csv](sharepoint/data/ExpenseDetails.csv) | 経費明細用リスト |
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
| データ保存 | CSV | SharePoint Lists（ヘッダー+明細） |
| 税計算 | Python Decimal | Power Fx |
| 一括申請 | なし | ★ 複数経費をまとめて申請 |
| 承認フロー | なし | Power Automate Approvals |
| 通知 | なし | Teams + Outlook |
| 領収書添付 | ローカルファイル | SharePoint/OneDrive |

## 関連リポジトリ

- [expense-app](https://github.com/Ezark213/expense-app) - 元のPython製デスクトップアプリ

## ライセンス

MIT License
