# 経費申請アプリ 進捗管理

> **最終更新: 2026年2月17日**
> 次回作業時はこのファイルを参照して、どこから再開するか確認してください。

---

## 現在のステータス: フェーズ2 作業中

```
[████████████░░░░░░░░] 約60% 完了
```

**フェーズ1（SharePoint基盤）→ 完了**
**フェーズ2（Power Apps修正）→ 作業中（2-1, 2-2, 2-4 完了）**
**フェーズ3（Power Automate）→ 未着手**
**フェーズ4（仕上げ）→ 未着手**

---

## 完了済み作業の詳細

### SharePoint Lists（フェーズ1: 完了）

| リスト | 状態 | 備考 |
|--------|------|------|
| **ExpenseRequests** | ✅ 完了 | タイトル, 申請者, 経費日付, 部署, 勘定科目, 内容, 税込金額, 税額, 税抜金額, 税区分（TaxRates参照・Lookup型）, インボイス番号, 領収書, 承認ステータス, 承認者, 承認日時, 承認コメント, 合計金額, 明細件数 |
| **ExpenseDetails** | ✅ 完了 | タイトル, 経費日付, 勘定科目（Choice型）, 内容, 税込金額, 税区分（Lookup型・TaxRates参照）, 税額, 税抜金額, インボイス番号（列は存在・アプリでは未使用）, 申請ID（数値型） |
| **TaxRates** | ✅ 完了 | 8行の税区分データ登録済み。列: タイトル, 税区分, 税率（"10.00%"形式テキスト）, 控除割合 |
| **Approvers** | ⏸️ 後回し | フェーズ4で必要に応じて作成。当面は固定承認者で運用可能 |

### Power Apps（フェーズ2: 作業中）

**5画面が存在:** HomeScreen, RequestListScreen, RequestFormScreen, DetailFormScreen, ApprovalScreen

| タスク | 状態 | 完了日 | 備考 |
|--------|------|--------|------|
| 2-1. データソース接続確認 | ✅ 完了 | 2/10 | ExpenseRequests, ExpenseDetails, TaxRates 接続済み |
| 2-2. DetailFormScreen 税計算エラー修正 | ✅ 完了 | 2/10 | IsBlank + IsNumeric ガード追加で解消 |
| 2-3. インボイス番号入力欄追加 | ⛔ 不要 | - | アプリにインボイス番号は不要と判断。列はリストに存在するが使用しない |
| 2-4. 「追加」ボタン（Button1_7）のPatch式完成 | ✅ 完了 | 2/17 | 下記の確定Patch式を参照 |
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

## 次回の作業再開ポイント

### 次にやること: タスク 2-5 から

**タスク 2-5**: HomeScreen の3ボタンに OnSelect を設定

```
// 新規申請ボタン（Button1_2）
Set(
    varNewRequest,
    Patch(
        ExpenseRequests,
        Defaults(ExpenseRequests),
        {
            タイトル: "申請_" & Text(Now(), "yyyymmddhhmmss"),
            承認ステータス: {Value: "下書き"}
        }
    )
);
Set(varCurrentRequestID, varNewRequest.ID);
Navigate(RequestFormScreen)

// 申請一覧ボタン（Button1_1）
Navigate(RequestListScreen)

// 承認管理ボタン（Button1）
Navigate(ApprovalScreen)
```

---

## 確定済みPatch式（2/17）

### DetailFormScreen「追加」ボタン（Button1_7）OnSelect

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
            '税区分': {
                Id: Dropdown2.Selected.ID,
                Value: Dropdown2.Selected.税区分
            },
            '税額': RoundDown(amt - amt / (1 + rate), 0),
            '税抜金額': RoundDown(amt / (1 + rate), 0)
        }
    )
);
Navigate(RequestFormScreen)
```

**列の型まとめ（2/17確認済み）:**
| 列 | リスト | 型 | Patch時の書き方 |
|----|--------|-----|----------------|
| 申請ID | ExpenseDetails | 数値 | `varCurrentRequestID` 直接 |
| 勘定科目 | ExpenseDetails | Choice | `{Value: ddAccountItem.Selected.Value}` |
| 税区分 | ExpenseDetails / ExpenseRequests | Lookup（TaxRates参照） | `{Id: Dropdown2.Selected.ID, Value: Dropdown2.Selected.税区分}` |
| 税率 | TaxRates | テキスト（"10.00%"形式） | `Value(Substitute(..., "%", "")) / 100` で数値変換 |

---

## 現在の Power Apps コントロール構造（2/17時点）

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
│   ├── TextInput1        （部署テキスト入力）
│   ├── galDetails        （経費明細ギャラリー）★Filter動作確認済み
│   ├── dpRequestDate     （申請日DatePicker）
│   └── 各ヘッダー・ラベル類
│
├── DetailFormScreen
│   ├── Label9_1      （税額ラベル）★修正済み
│   ├── lblNetAmount  （税抜金額ラベル）
│   ├── Button1_7     （追加ボタン）★Patch式完成(2/17)
│   ├── Button1_6     （キャンセルボタン）
│   ├── Rectangle2
│   ├── Dropdown2     （税区分ドロップダウン / Items=TaxRates / 表示列=税区分）
│   ├── txtAmount     （税込金額入力）
│   ├── txtContent    （内容入力）
│   ├── ddAccountItem （勘定科目ドロップダウン / Items=固定リスト）
│   ├── dpExpenseDate （経費日付DatePicker）
│   ├── Label8        （税抜金額ラベル）★修正済み
│   └── 各ラベル類
│
└── ApprovalScreen    （空・未実装）
```

---

## 参考ファイル

| ファイル | 説明 |
|---------|------|
| [docs/作業リスト.html](docs/作業リスト.html) | ★ 作業チェックリスト（2/17更新） |
| [docs/経費申請アプリ_作業手順書.html](docs/経費申請アプリ_作業手順書.html) | 全タスクの詳細手順書 |
| [docs/PowerApps_経費申請アプリ_完全ガイド.html](docs/PowerApps_経費申請アプリ_完全ガイド.html) | アプリ構築の完全ガイド（1/19版） |
