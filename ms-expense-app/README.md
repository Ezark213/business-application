# MS 経費申請アプリ (MS Expense App)

## 概要

既存のPython製経費計上アプリ（[expense-app](https://github.com/Ezark213/expense-app)）をMicrosoft 365エコシステムに移行したアプリケーションです。

**本システムは「複数の経費をまとめて1回で申請」する設計（ヘッダー・明細方式）です。**

### 主な特徴

- **Power Apps** によるモダンなUI
- **SharePoint Lists** によるデータ管理（申請ヘッダー + 経費明細）
- **Power Automate** による承認ワークフロー・申請者自動設定
- **Microsoft Teams** への通知連携
- **インボイス制度対応** 8パターンの税区分に対応

## 最新の更新情報（2026/01/19）

### 修正・改善点

| 項目 | 内容 |
|------|------|
| ギャラリー表示 | 承認ステータス → 勘定科目に変更 |
| ヘッダーラベル | ギャラリー外に配置（エラー対策） |
| 金額表示 | カンマ区切り表示（`Text(..., "¥#,##0")`） |
| 行間調整 | TemplateSize: 45, TemplatePadding: 2 |
| Person列対応 | Power Automateで申請者を自動設定（Patch式から除外） |
| 税計算 | 空欄時のエラー対策（IsBlank判定追加） |
| Teams通知 | 申請時に承認者へ自動通知 |

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

## 画面構成

| 画面 | 名前 | 用途 |
|------|------|------|
| 1 | HomeScreen | ホーム画面 |
| 2 | RequestListScreen | 申請一覧（ギャラリー表示） |
| 3 | RequestFormScreen | 申請作成・経費明細一覧 |
| 4 | DetailFormScreen | 経費明細の入力 |

### 画面遷移フロー

```
HomeScreen
    ↓ 「申請一覧」ボタン
RequestListScreen
    ↓ 「+ 新規申請」ボタン / 行クリック
RequestFormScreen
    ↓ 「+ 経費を追加」ボタン
DetailFormScreen
    ↓ 「追加」ボタン
RequestFormScreen（戻る）
    ↓ 「申請する」ボタン
RequestListScreen（戻る）
```

## Power Automate フロー

### フロー1：申請者自動設定

ExpenseRequestsに新規アイテム作成時、登録者を「申請者」列に自動設定します。

```
トリガー: 項目が作成されたとき (ExpenseRequests)
    ↓
アクション: 項目の更新
    - 申請者 ← 登録者 Email
```

**なぜ必要か**: Power AppsからPerson列（申請者）を直接設定すると複雑な構文が必要でエラーになりやすいため、Power Automateで自動設定します。

### フロー2：Teams承認通知

承認ステータスが「申請中」に変更されたとき、承認者にTeams通知を送信します。

```
トリガー: 項目が作成または変更されたとき (ExpenseRequests)
    ↓
条件: 承認ステータス = "申請中"
    ↓ はい
アクション: チャットでメッセージを投稿
    - 受信者: 承認者
    - メッセージ: 申請内容の詳細
```

## フォルダ構成

```
ms-expense-app/
├── README.md                                      # このファイル
├── docs/
│   ├── PowerApps_経費申請アプリ_完全ガイド.html   # ★ 最新の構築ガイド
│   ├── architecture.md                            # アーキテクチャ説明
│   └── ...
├── sharepoint/
│   ├── lists-schema.json                          # SharePoint Listsスキーマ
│   └── data/
│       ├── ExpenseRequests.csv                    # 申請ヘッダー（インポート用）
│       ├── ExpenseDetails.csv                     # 経費明細（インポート用）
│       └── TaxRates.csv                           # 税区分マスター（インポート用）
├── power-automate/
│   ├── approval-flow.json                         # 承認フロー定義
│   └── teams-notification.json                    # Teams通知フロー
├── power-apps/
│   └── app-definition.json                        # アプリ定義
└── old/                                           # 旧ファイル・参考資料
```

## クイックスタート

### 1. 必要なライセンス

- Microsoft 365 Business Basic以上
- Power Apps ライセンス（Microsoft 365に含まれるStandard版で可）
- Power Automate ライセンス（承認フロー用）

### 2. 構築手順

詳細な構築手順は以下のファイルを参照してください：

- **[PowerApps_経費申請アプリ_完全ガイド.html](docs/PowerApps_経費申請アプリ_完全ガイド.html)** - 最新の完全ガイド（全修正反映済み）

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

## よくあるエラーと対処法

| エラー | 原因 | 解決方法 |
|--------|------|----------|
| 'ThisItem' は認識されません | ラベルがギャラリー外にある | ギャラリーの1行目を選択してからラベルを追加 |
| ボタンを押しても反応しない | Person列の設定エラー | Patch式から申請者を削除、Power Automateで設定 |
| Text値が必要です | Choice列に.Valueがない | `ThisItem.'列名'.Value` に修正 |
| 数式でスコープが... | ギャラリーにデータがない | 警告のみ。データがあれば動作する |

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
| 申請者自動設定 | - | ★ Power Automateで自動設定 |

## 関連リポジトリ

- [expense-app](https://github.com/Ezark213/expense-app) - 元のPython製デスクトップアプリ

## ライセンス

MIT License
