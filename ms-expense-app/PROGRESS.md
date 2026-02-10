# 経費申請アプリ 進捗管理

> **最終更新: 2026年2月10日**
> 次回作業時はこのファイルを参照して、どこから再開するか確認してください。

---

## 現在のステータス: フェーズ2 作業中

```
[██████████░░░░░░░░░░] 約45% 完了
```

**フェーズ1（SharePoint基盤）→ 完了**
**フェーズ2（Power Apps修正）→ 作業中（2-1, 2-2 完了）**
**フェーズ3（Power Automate）→ 未着手**
**フェーズ4（仕上げ）→ 未着手**

---

## 完了済み作業の詳細

### SharePoint Lists（フェーズ1: 完了）

| リスト | 状態 | 備考 |
|--------|------|------|
| **ExpenseRequests** | ✅ 完了 | 16列すべて作成済み（タイトル, 申請者, 経費日付, 部署, 勘定科目, 内容, 税込金額, 税額, 税抜金額, 税区分, インボイス番号, 領収書, 承認ステータス, 承認者, 承認日時, 承認コメント）。**追加が必要だった「合計金額」「明細件数」の2列も追加済み** |
| **ExpenseDetails** | ✅ 完了 | 列: タイトル, 申請ID, 経費日付, 勘定科目, 内容, 税込金額, 税区分, 税額, 税抜金額, インボイス番号。テストデータあり（要クリーンアップ） |
| **TaxRates** | ✅ 完了 | 8行の税区分データ登録済み（10%適格, 10%経過措置80%, 10%経過措置50%, 8%適格, 8%経過措置80%, 8%経過措置50%, 非課税, 不課税） |
| **Approvers** | ⏸️ 後回し | フェーズ4で必要に応じて作成。当面は固定承認者で運用可能 |

### Power Apps（フェーズ2: 作業中）

**5画面が存在:** HomeScreen, RequestListScreen, RequestFormScreen, DetailFormScreen, ApprovalScreen

| タスク | 状態 | 完了日 | 備考 |
|--------|------|--------|------|
| 2-1. データソース接続確認 | ✅ 完了 | 2/10 | ExpenseRequests, ExpenseDetails, TaxRates 接続済み |
| 2-2. DetailFormScreen 税計算エラー修正 | ✅ 完了 | 2/10 | Label9_1 の税額・税抜金額ラベルのエラー解消。txtAmountのDefault を空に修正し、IsBlank + IsNumeric ガード追加 |
| 2-3. インボイス番号入力欄追加 | ❌ 未着手 | - | DetailFormScreen に txtInvoiceNumber を追加する |
| 2-4. 「追加」ボタンの Patch式完成 | ❌ 未着手 | - | 税区分・税額・税抜金額・インボイス番号を Patch に含める |
| 2-5. HomeScreen ボタン OnSelect設定 | ❌ 未着手 | - | 新規申請(Patch+Navigate), 申請一覧(Navigate), 承認管理(Navigate) |
| 2-6. RequestListScreen 新規申請ボタン・行選択確認 | ❌ 未着手 | - | OnSelect式の確認・修正 |
| 2-7. 「申請する」ボタン完成 | ❌ 未着手 | - | 承認ステータス→申請中、合計金額・明細件数の書き戻し |
| 2-8. 部署入力の改善 | ❌ 任意 | - | テキスト入力→ドロップダウンに変更（優先度低） |
| 2-9. コントロール名整理 | ❌ 推奨 | - | Button1等のデフォルト名をリネーム（優先度低） |

### Power Automate（フェーズ3: 未着手）

| タスク | 状態 |
|--------|------|
| 3-1. 申請者自動設定フロー | ❌ 未着手 |
| 3-2. Teams承認通知フロー | ❌ 未着手 |
| 3-3. 承認フロー（承認アクション付き） | ❌ 未着手 |

### 仕上げ（フェーズ4: 未着手）

| タスク | 状態 |
|--------|------|
| 4-1. ApprovalScreen 実装 | ❌ 未着手 |
| 4-2. Approvers リスト作成 | ❌ 未着手 |
| 4-3. 領収書添付機能 | ❌ 任意 |
| 4-4. テストデータ削除・全体テスト | ❌ 未着手 |
| 4-5. アプリ公開・共有 | ❌ 未着手 |

---

## 明日の作業再開ポイント

### 次にやること: タスク 2-3 から

1. **タスク 2-3**: DetailFormScreen にインボイス番号入力欄を追加
   - TextInput 挿入 → 名前を `txtInvoiceNumber` に変更
   - HintText: `"例: T1234567890123"`
   - ラベル「インボイス番号」を税区分ドロップダウンの下に配置

2. **タスク 2-4**: 「追加」ボタン（Button1_6）の Patch 式を完成版に差し替え
   ```
   With(
       {
           rate: Value(Substitute(Dropdown2.Selected.税率, "%", "")) / 100,
           amt: Value(txtAmount.Text)
       },
       Patch(
           ExpenseDetails,
           Defaults(ExpenseDetails),
           {
               Title: txtContent.Text,
               '経費日付': dpExpenseDate.SelectedDate,
               '勘定科目': {Value: ddAccountItem.Selected.Value},
               '内容': txtContent.Text,
               '税込金額': amt,
               '申請ID': varCurrentRequestID,
               '税区分': {Value: Dropdown2.Selected.税区分},
               '税額': RoundDown(amt - amt / (1 + rate), 0),
               '税抜金額': RoundDown(amt / (1 + rate), 0),
               'インボイス番号': txtInvoiceNumber.Text
           }
       )
   );
   Navigate(RequestFormScreen)
   ```

3. **タスク 2-5**: HomeScreen の3ボタンに OnSelect を設定

→ 詳細な手順は `docs/経費申請アプリ_作業手順書.html` を参照

---

## 現在の Power Apps コントロール構造（2/10時点のツリービュー）

```
App
├── Host
│
├── HomeScreen
│   ├── Button1_2     （新規申請・青ボタン）
│   ├── Button1_1     （申請一覧・緑ボタン）
│   ├── Button1       （承認管理・灰ボタン）
│   ├── Label2        （ヘッダータイトル「経費申請システム」）
│   └── Label1
│
├── RequestListScreen
│   ├── lblHeaderDept_1   （列ヘッダー「勘定科目」）
│   ├── lblHeaderAmount_1 （列ヘッダー「税込金額」）
│   ├── lblHeaderDept     （列ヘッダー「部署」）
│   ├── lblHeaderDate     （列ヘッダー「日付」）
│   ├── galRequests       （申請一覧ギャラリー）★動作確認済み
│   ├── Button1_3         （+新規申請ボタン）
│   ├── rectHeader2       （ヘッダーバー）
│   ├── Label3            （「申請一覧」タイトル）
│   ├── Label1_1          （「←戻る」ラベル）
│   └── Rectangle7
│
├── RequestFormScreen
│   ├── Button1_5         （←戻るボタン）
│   ├── Button1_4         （申請するボタン）★OnSelect要修正
│   ├── lblTotalInfo      （合計表示ラベル）★動作確認済み
│   ├── lblHeaderDate_3   （列ヘッダー）
│   ├── lblHeaderDate_2   （列ヘッダー）
│   ├── lblHeaderDate_1   （列ヘッダー）
│   ├── Rectangle7_1
│   ├── TextInput1        （部署テキスト入力）
│   ├── galDetails        （経費明細ギャラリー）★Filter動作確認済み
│   ├── Label5_1, Label5  （ラベル類）
│   ├── dpRequestDate     （申請日DatePicker）
│   ├── rectHeader2_1     （ヘッダーバー）
│   ├── Label3_1          （「申請作成」タイトル）
│   ├── Label1_2          （「←戻る」ラベル）
│   └── Rectangle1
│
├── DetailFormScreen
│   ├── Label9_1          （税額ラベル）★エラー修正済み(2/10)
│   ├── Button1_6         （追加ボタン）★Patch式要修正
│   ├── Rectangle2
│   ├── Dropdown2         （税区分ドロップダウン）
│   ├── Label5_6, Label5_5（ラベル類）
│   ├── txtAmount         （税込金額入力）★Default修正済み(2/10)
│   ├── txtContent        （内容入力）
│   ├── Label5_4
│   ├── ddAccountItem     （勘定科目ドロップダウン）
│   ├── dpExpenseDate     （経費日付DatePicker）
│   ├── Label5_3, Label5_2（ラベル類）
│   ├── Label8            （税抜金額ラベル）★エラー修正済み(2/10)
│   └── Label1_3          （キャンセルボタン周辺ラベル）
│
└── ApprovalScreen        （空・未実装）
```

---

## 現状分析サマリー（2/10実施）

### SharePoint 経費管理サイトの状況
- **サイト名**: 経費管理
- **リスト**: ExpenseRequests, ExpenseDetails, TaxRates の3つが存在
- **Approvers リスト**: 未作成（フェーズ4）
- **テストデータ**: ExpenseDetailsに6件のテストデータあり（一部は申請IDが空で紐付け不全）

### Power Apps の状況
- **アプリ名**: 経費申請アプリ
- **画面数**: 5画面（設計は4画面 + ApprovalScreen追加）
- **動作確認済み機能**:
  - RequestListScreen のギャラリー表示（日付, 部署, 税込金額, 勘定科目）
  - RequestFormScreen の明細ギャラリー（Filter by 申請ID）
  - RequestFormScreen の合計ラベル（件数・金額）
  - DetailFormScreen の基本入力フォーム（経費日付, 勘定科目, 内容, 税込金額, 税区分）
- **修正済み問題**:
  - 税額ラベル(Label9_1)のエラー → IsBlank + IsNumeric ガード追加で解消
  - 税抜金額ラベル(Label8)のエラー → 同上で解消
  - txtAmount のDefault「テキスト入力」→ 空文字に修正
- **残存問題**:
  - HomeScreenのボタンにOnSelect未設定の可能性
  - DetailFormScreenの「追加」ボタンPatch式が不完全（税関連列が含まれていない）
  - ApprovalScreenが空
  - コントロール名がデフォルトのまま多数

### Power Automate の状況
- **フロー数**: 0（全て未作成）
- **必要なフロー**: 申請者自動設定、Teams承認通知、承認フロー

---

## 参考ファイル

| ファイル | 説明 |
|---------|------|
| [docs/経費申請アプリ_作業手順書.html](docs/経費申請アプリ_作業手順書.html) | 全タスクの詳細手順書（Power Apps数式・Power Automate設定手順付き） |
| [docs/PowerApps_経費申請アプリ_完全ガイド.html](docs/PowerApps_経費申請アプリ_完全ガイド.html) | アプリ構築の完全ガイド（1/19版） |
| [docs/architecture.md](docs/architecture.md) | アーキテクチャ設計書 |
| [power-apps/app-definition.json](power-apps/app-definition.json) | Power Apps設計定義 |
| [power-automate/approval-flow.json](power-automate/approval-flow.json) | 承認フロー設計 |
| [power-automate/teams-notification.json](power-automate/teams-notification.json) | Teams通知フロー設計 |
