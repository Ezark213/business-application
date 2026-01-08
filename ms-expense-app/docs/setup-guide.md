# セットアップガイド

## 前提条件

### 必要なライセンス
- Microsoft 365 Business Basic 以上
- Power Apps ライセンス (M365に含まれる標準機能で可)
- Power Automate ライセンス (承認フロー用)

### 必要な権限
- SharePoint サイト作成権限
- Power Platform 環境へのアクセス
- Teams チーム/チャネル作成権限（通知用）

## セットアップ手順

### Step 1: SharePoint サイトの作成

1. SharePoint 管理センターにアクセス
2. 「サイトの作成」→「チームサイト」を選択
3. サイト名: `経費管理` を入力
4. サイトアドレスを記録（後で使用）

### Step 2: SharePoint Lists の作成

#### 2.1 ExpenseRequests リスト

1. サイトの「サイトコンテンツ」→「新規」→「リスト」
2. 「空白のリスト」を選択
3. リスト名: `ExpenseRequests` を入力
4. 以下の列を追加:

| 列名 | 種類 | 設定 |
|------|------|------|
| ExpenseDate | 日付 | 日付のみ、必須 |
| Applicant | ユーザー | 必須 |
| AccountCategory | 選択肢 | 勘定科目一覧を設定 |
| Description | 1行テキスト | 最大500文字 |
| AmountWithTax | 通貨 | 日本円、必須 |
| TaxCategory | 選択肢 | 税区分一覧を設定 |
| TaxAmount | 通貨 | 日本円 |
| AmountWithoutTax | 通貨 | 日本円 |
| InvoiceNumber | 1行テキスト | 最大14文字 |
| ApprovalStatus | 選択肢 | 下書き/申請中/承認済み/差戻し/却下 |
| Approver | ユーザー | |
| ApprovalDate | 日付と時刻 | |
| ApprovalComment | 複数行テキスト | |
| Department | 選択肢 | 部署一覧を設定 |

#### 2.2 Approvers リスト

1. 新規リスト `Approvers` を作成
2. 以下の列を追加:

| 列名 | 種類 | 設定 |
|------|------|------|
| Department | 選択肢 | 部署一覧 |
| PrimaryApprover | ユーザー | 必須 |
| SecondaryApprover | ユーザー | |
| ThresholdAmount | 通貨 | 既定値: 50000 |
| IsActive | はい/いいえ | 既定: はい |

3. 各部署の承認者データを登録

#### 2.3 TaxRates リスト

1. 新規リスト `TaxRates` を作成
2. 以下の列を追加:

| 列名 | 種類 |
|------|------|
| TaxCategory | 1行テキスト |
| TaxRate | 数値 (小数2桁) |
| DeductionRate | 数値 (小数2桁) |
| Divisor | 数値 |
| Multiplier | 数値 |

3. `sharepoint/lists-schema.json` の `defaultData` を参考にデータを登録

### Step 3: Power Apps の作成

#### 3.1 アプリの新規作成

1. [make.powerapps.com](https://make.powerapps.com) にアクセス
2. 「作成」→「空のアプリ」→「空のキャンバスアプリ」
3. アプリ名: `経費申請アプリ`
4. 形式: タブレット（レスポンシブ推奨）

#### 3.2 データソースの接続

1. 左ペイン「データ」→「データの追加」
2. 「SharePoint」を選択
3. サイトURLを入力して接続
4. 3つのリストすべてを追加:
   - ExpenseRequests
   - Approvers
   - TaxRates

#### 3.3 画面の作成

`power-apps/app-definition.json` を参考に以下の画面を作成:

1. **HomeScreen** - ダッシュボード
2. **ExpenseFormScreen** - 申請フォーム
3. **ExpenseListScreen** - 一覧
4. **ExpenseDetailScreen** - 詳細
5. **ApprovalScreen** - 承認管理
6. **ReportScreen** - レポート

#### 3.4 税計算関数の実装

App.OnStart に以下を追加:

```
Set(
    fnCalculateTax,
    With(
        {taxRate: LookUp(TaxRates, TaxCategory = _taxCategory)},
        {
            TaxAmount: RoundDown(_amountWithTax / taxRate.Divisor * taxRate.Multiplier, 0),
            AmountWithoutTax: _amountWithTax - RoundDown(_amountWithTax / taxRate.Divisor * taxRate.Multiplier, 0)
        }
    )
)
```

### Step 4: Power Automate フローの作成

#### 4.1 承認フロー

1. [make.powerautomate.com](https://make.powerautomate.com) にアクセス
2. 「作成」→「自動クラウドフロー」
3. トリガー: 「アイテムが作成または変更されたとき (SharePoint)」
4. `power-automate/approval-flow.json` を参考にフローを構築

主要なアクション:
- 条件: ApprovalStatus = "申請中"
- SharePoint からアイテム取得 (Approvers)
- 開始して承認を待機
- 条件分岐 (承認/却下)
- SharePoint アイテム更新
- Teams チャットまたはチャネルでメッセージを投稿

#### 4.2 Teams通知フロー

1. 新規自動フロー作成
2. `power-automate/teams-notification.json` を参考に構築

### Step 5: Teams 統合

#### 5.1 通知チャネルの設定

1. Teams で経費管理用チームを作成（または既存チームを使用）
2. 「経費申請」チャネルを作成
3. Power Automate フローでチーム/チャネルIDを設定

#### 5.2 Power Apps タブの追加

1. Teams チャネルで「+」→「Power Apps」
2. 作成したアプリを選択して追加

### Step 6: テストと展開

#### 6.1 テスト手順

1. テストユーザーで申請を作成
2. 承認者アカウントで承認/却下をテスト
3. Teams通知の受信を確認
4. 各種フィルター・検索をテスト

#### 6.2 本番展開

1. Power Apps をユーザーグループと共有
2. SharePoint サイトの権限を設定
3. Power Automate フローの所有者を設定
4. ユーザーマニュアルを配布

## トラブルシューティング

### よくある問題

| 症状 | 原因 | 対処 |
|------|------|------|
| データが表示されない | 接続エラー | データソースを再接続 |
| 承認通知が届かない | フローエラー | フロー実行履歴を確認 |
| 税額計算が合わない | TaxRatesデータ不備 | マスタデータを確認 |

### サポート

問題が解決しない場合は、IT部門または管理者にお問い合わせください。
