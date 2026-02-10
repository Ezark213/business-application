# 資格取得申請システム

Microsoft 365（SharePoint Lists + Power Apps + Power Automate + Teams）を活用した、従業員向けの資格取得申請・承認・報奨金管理システム。

## このアプリでできること

- 従業員が**資格取得の宣言届（事前申請）**と**取得届（事後申請）**を Power Apps から提出できる
- 承認者に**Teams通知**が届き、ワンクリックで承認・却下できる
- 承認結果が申請者にTeamsで自動通知される（報奨金内訳つき）
- 事前に宣言届を出していた場合、**+5,000円のボーナス**が加算される
- 全ての申請・承認履歴が**SharePointリスト**に自動記録される
- **28資格・7分野**に対応した資格マスタを搭載

## システム構成

```
┌─────────────────────────────────────────────────┐
│                  利用者（従業員）                    │
│              Power Apps 申請フォーム                 │
└────────────────────┬────────────────────────────┘
                     │ Patch（申請データ書き込み）
                     ▼
┌─────────────────────────────────────────────────┐
│              SharePoint Lists                    │
│  ┌──────────────┐    ┌─────────────────────┐    │
│  │  資格マスタ    │    │  資格取得申請リスト    │    │
│  │ (28資格)      │◄───│ (申請・承認データ)     │    │
│  └──────────────┘    └──────────┬──────────┘    │
└─────────────────────────────────┬────────────────┘
                                  │ トリガー（アイテム作成時）
                                  ▼
┌─────────────────────────────────────────────────┐
│              Power Automate                      │
│  遅延(10秒) → 報奨金計算 → 承認依頼              │
│       ┌──────┴──────┐                            │
│       │承認         │却下                        │
│       ▼             ▼                            │
│  ステータス更新   ステータス更新                   │
│  ┌────┴────┐    Teams却下通知                    │
│  │宣言届   │取得届                               │
│  ▼         ▼                                     │
│ Teams     ボーナス判定                            │
│ 通知      ┌───┴───┐                             │
│           │あり   │なし                          │
│           ▼       ▼                              │
│         Teams   Teams                            │
│         通知    通知                              │
└─────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│          Microsoft Teams                         │
│  承認依頼通知 / 承認結果通知（Flow bot チャット）   │
└─────────────────────────────────────────────────┘
```

## 申請フロー

```
従業員が資格取得を決意
    │
    ├─→ ❶ 宣言届を提出（任意・事前申請で+5,000円ボーナス対象）
    │       → 承認者がTeamsで承認
    │
    ├─→ ❷ 資格を取得後、取得届を提出
    │       → 宣言届がある場合はドロップダウンで紐づけ
    │       → 承認者がTeamsで承認
    │
    └─→ ❸ 報奨金が確定、Teams通知で本人に通知
```

## 報奨金ルール

| 申請種別 | 報奨金 | 事前ボーナス | 説明 |
|---------|--------|------------|------|
| 資格取得宣言届 | 0円 | 0円 | 事前の宣言のみ。報奨金は取得届提出時に確定 |
| 資格取得届（宣言届あり） | マスタから取得 | **+5,000円** | 事前に宣言届を提出していた場合ボーナス加算 |
| 資格取得届（宣言届なし） | マスタから取得 | 0円 | 報奨金のみ |

### 報奨金表示パターン（Power Apps上）

| 報奨金 | 宣言届の有無 | 表示 |
|--------|------------|------|
| - | 宣言届の場合 | ※この届出では報奨金は発生しません... |
| 0円（FP3級など） | 宣言届あり | 受験料相当額 + ¥5,000（事前申請ボーナス） |
| 0円（FP3級など） | 宣言届なし | 受験料相当額 |
| 通常 | 宣言届あり | ¥XX,XXX + ¥5,000（事前申請ボーナス） |
| 通常 | 宣言届なし | ¥XX,XXX |

## 技術スタック・使用サービス

| コンポーネント | 用途 |
|---------------|------|
| **SharePoint Lists** | データストア（資格マスタ、申請データ） |
| **Power Apps** | 申請フォームUI（キャンバスアプリ、3画面構成） |
| **Power Automate** | 承認ワークフロー（トリガー → 承認 → 分岐処理 → 通知） |
| **Microsoft Teams** | 承認依頼・結果通知（Flow bot チャット） |

## ファイル構成

```
qualification-application/
│
├── README.md                              ← このファイル
│
├── 設計・構築ドキュメント（Markdown）
│   ├── 01_sharepoint-lists.md             SharePointリスト設計・作成手順
│   ├── 02_power-apps.md                   Power Apps設計・作成手順
│   ├── 03_power-automate.md               Power Automate設計・作成手順
│   └── 04_teams-notification.md           Teams通知設定手順
│
├── 差分調査・修正記録
│   ├── 05_gap-analysis-and-fix-plan.md    差分調査・修正プラン（詳細版）
│   └── 06_pending-actions.md              全修正アクションの実施記録
│
├── 修正手順書
│   └── 資格申請システム_修正手順書_完全版.html  確定版・コピペ対応の修正手順書
│
├── データ
│   └── data/qualification_master.csv      資格マスタ（28資格・7分野）
│
└── old/                                   過去の作業用HTMLファイル（参考資料）
    ├── PowerApps_修正後UIイメージ.html
    ├── PowerAutomate_完全設定ガイド.html
    ├── PowerAutomate_修正ガイド_詳細版.html
    ├── PowerAutomate_修正手順書.html
    ├── power-apps-improvement-guide.html
    ├── power-automate-improvement-guide.html
    ├── 差分調査_修正プラン_完全版.html
    └── 資格申請システム修正ガイド.html
```

## セットアップ手順

### 1. SharePoint リスト作成
[`01_sharepoint-lists.md`](01_sharepoint-lists.md) に従い、以下の2リストを作成:
- **資格マスタ**: 資格名・詳細・報奨金・難易度（`data/qualification_master.csv` をインポート）
- **資格取得申請**: 申請データを蓄積するリスト

### 2. Power Apps フォーム作成
[`02_power-apps.md`](02_power-apps.md) に従い、キャンバスアプリを作成:
- **画面1**: 申請フォーム（資格選択 → 報奨金表示 → 送信）
- **画面2**: 送信完了画面
- **画面3**: 申請履歴一覧

### 3. Power Automate 承認フロー作成
[`03_power-automate.md`](03_power-automate.md) に従い、自動フローを作成:
- トリガー → 10秒遅延 → 報奨金メッセージ生成 → 承認依頼 → 承認/却下分岐 → Teams通知

### 4. テスト実行
[`06_pending-actions.md`](06_pending-actions.md) のPhase 3テストケースで動作確認

## Power Apps 主要数式

### 送信ボタン（OnSelect）
```
Patch(
    資格取得申請,
    Defaults(資格取得申請),
    {
        Title: DropdownQualification.Selected.Value & " " & DropdownDetail.Selected.Value,
        申請種別: RadioApplicationType.Selected,
        申請日: Today(),
        予定日_取得日: DatePickerAcquisition.SelectedDate,
        理由_内容: TextInputReason.Text,
        ステータス: {Value: "申請中"},
        報奨金額: If(
            RadioApplicationType.Selected.Value = "資格取得宣言届",
            0,
            LookUp(
                資格マスタ,
                Title = DropdownQualification.Selected.Value && 詳細 = DropdownDetail.Selected.Value,
                報奨金
            )
        ),
        事前ボーナス: If(
            RadioApplicationType.Selected.Value = "資格取得届" && !IsBlank(Dropdown1.Selected),
            5000,
            0
        ),
        関連宣言届ID: If(
            RadioApplicationType.Selected.Value = "資格取得届"
                && !IsBlank(Dropdown1.Selected),
            Dropdown1.Selected.ID,
            Blank()
        )
    }
);
Navigate(Screen2, ScreenTransition.Fade)
```

### 関連宣言届ドロップダウン（Dropdown1 の Items）
```
Filter(
    資格取得申請,
    申請種別.Value = "資格取得宣言届"
        && ステータス.Value = "承認済"
        && Title = DropdownQualification.Selected.Value & " " & DropdownDetail.Selected.Value
)
```

## Power Automate フロー構造

```
トリガー（アイテム作成時）
  → 遅延（10秒）
  → 項目の取得
  → 項目の更新2（初期処理）
  → 作成（報奨金メッセージ生成）
  → 開始して承認を待機
  → 条件（承認 / 却下）
      ├─ True（承認）
      │   → 項目の更新3（ステータス: 承認済, 承認者, 承認日）
      │   → 条件1（申請種別 = 宣言届？）
      │       ├─ True（宣言届）→ Teams通知2
      │       └─ False（取得届）
      │           → 条件2（事前ボーナス > 0？）
      │               ├─ True  → Teams通知3（報奨金＋ボーナス内訳）
      │               └─ False → Teams通知4（報奨金のみ＋次回案内）
      └─ False（却下）
          → 項目の更新1（ステータス: 却下）
          → Teams通知1（却下理由）
          → For each 1 → 項目の更新4（ステータス: 却下）
```

## 注意事項

### Power Apps
- Distinct関数使用後は `.Selected.Value` を使用
- 報奨金は `LookUp()` 関数で資格マスタから動的取得
- Title は「資格名 + 半角スペース + 詳細（級）」の形式で保存される

### Power Automate
- トリガー直後の10秒遅延は必須（SharePoint書き込み完了待ち）
- 承認者Claimsの式: `body('開始して承認を待機')?['responses'][0]?['responder']?['email']`
- 承認日の式: `utcNow()`
- SharePoint列の内部名は日本語の場合 `OData__x...` 形式に変換される

## 実装状況

| コンポーネント | 進捗 |
|---------------|------|
| SharePoint リスト | ✅ 100% |
| Power Apps | ✅ 100% |
| Power Automate | ✅ 100% |
| テスト | ✅ 全5ケース合格 |

## 更新履歴

### 2026-02-10（修正完了）
- **Phase 0 調査完了**: Power Automateの条件分岐を全展開し実装状況を確認
- **Phase 1 Power Apps修正完了**: Dropdown1フィルター修正、Patch関数に関連宣言届ID追加
- **Phase 2 Power Automate修正完了**: 遅延追加、空白行削除、ステータス更新追加、却下修正
- **Phase 3 テスト完了**: 全5ケース合格
- 確定版修正手順書を作成（`資格申請システム_修正手順書_完全版.html`）
- リポジトリ整理: 過去のHTMLファイルを `old/` に移動

### 2026-02-09
- 差分調査・現状分析を実施（GitHub仕様 vs 実装済み環境の比較）
- 修正プランを策定（`05_gap-analysis-and-fix-plan.md`）
- 発見された問題8件を文書化

### 2026-01-15
- 詳細（級）ドロップダウン追加
- 4パターンの報奨金表示対応
- 受験料相当額表示対応
- 動的ラベル切り替え機能追加
