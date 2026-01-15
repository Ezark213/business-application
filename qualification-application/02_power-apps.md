# Power Apps 申請フォーム 設計・作成手順

## 1. アプリ作成

### 1.1 Power Appsにアクセス
1. https://make.powerapps.com にアクセス
2. 左メニュー「+ 作成」
3. 「空のアプリ」→「空のキャンバスアプリ」
4. アプリ名: `資格取得申請`
5. 形式: タブレット（PCメイン）またはスマートフォン
6. 「作成」

### 1.2 データソース接続
1. 左メニュー「データ」アイコン
2. 「+ データの追加」
3. 「SharePoint」を選択
4. サイトURLを入力
5. リストを選択:
   - `資格マスタ`
   - `資格取得申請`

---

## 2. 画面設計

### 2.1 画面構成
```
Screen1: 申請フォーム画面
Screen2: 申請完了画面
Screen3: 申請履歴画面（オプション）
```

### 2.2 コントロール名対応表

| 項目 | コントロール名 | 種類 |
|------|--------------|------|
| 申請種別 | RadioApplicationType | ラジオボタン |
| 分類 | DropdownCategory | ドロップダウン |
| 資格名 | DropdownQualification | ドロップダウン |
| 詳細（級） | DropdownDetail | ドロップダウン |
| 日付ラベル | lbl取得日 | ラベル |
| 日付入力 | DatePickerAcquisition | 日付ピッカー |
| 理由入力 | TextInputReason | テキスト入力 |
| 報奨金ラベル | Label3 | ラベル |
| 申請ボタン | ButtonSubmit | ボタン |

---

## 3. Screen1（申請フォーム）作成

### 3.1 ヘッダー部分
1. 「挿入」→「テキストラベル」
2. Text: `"資格取得申請"`
3. フォントサイズ: 24
4. 配置: 上部中央

### 3.2 申請種別（ラジオボタン）
1. 「挿入」→「入力」→「ラジオ」
2. 名前: `RadioApplicationType`
3. Items: `["資格取得宣言届", "資格取得届"]`
4. Default: `"資格取得宣言届"`
5. Layout: `Layout.Horizontal`

### 3.3 分類ドロップダウン
1. 「挿入」→「入力」→「ドロップダウン」
2. 名前: `DropdownCategory`
3. Items:
```
Distinct(資格マスタ, 分類)
```

### 3.4 資格名ドロップダウン（Distinct使用）
1. 「挿入」→「入力」→「ドロップダウン」
2. 名前: `DropdownQualification`
3. Items:
```
Distinct(
    Filter(資格マスタ, 分類 = DropdownCategory.Selected.Value),
    Title
)
```

> **注意**: Distinctを使用すると、Selectedの参照が `.Selected.Title` から `.Selected.Value` に変わります。

### 3.5 詳細（級）ドロップダウン【新規追加】
1. 「挿入」→「入力」→「ドロップダウン」
2. 名前: `DropdownDetail`
3. Items:
```
Distinct(
    Filter(資格マスタ, Title = DropdownQualification.Selected.Value),
    詳細
)
```

> **目的**: 同じ資格名でも「1級」「2級」など詳細によって報奨金が異なるため、詳細を選択できるようにします。

### 3.6 日付ラベル（動的切り替え）
1. 「挿入」→「テキストラベル」
2. 名前: `lbl取得日`
3. Text:
```
If(
    RadioApplicationType.Selected.Value = "資格取得宣言届",
    "取得予定日",
    "取得日"
)
```

> **動作**: 申請種別に応じてラベルが自動で切り替わります。

### 3.7 日付入力
1. 「挿入」→「入力」→「日付の選択」
2. 名前: `DatePickerAcquisition`

### 3.8 理由/内容テキスト入力
1. 「挿入」→「入力」→「テキスト入力」
2. 名前: `TextInputReason`
3. Mode: `TextMode.MultiLine`
4. HintText:
```
If(RadioApplicationType.Selected.Value = "資格取得宣言届",
   "資格を取得したい理由を入力してください",
   "資格の内容を入力してください"
)
```

### 3.9 報奨金表示ラベル（4パターン対応）
1. 「挿入」→「テキストラベル」
2. 名前: `Label3`
3. Text:
```
If(
    LookUp(
        資格マスタ,
        Title = DropdownQualification.Selected.Value && 詳細 = DropdownDetail.Selected.Value,
        報奨金
    ) = 0,
    If(
        RadioApplicationType.Selected.Value = "資格取得宣言届",
        "報奨金: ¥5,000（事前申請ボーナス）+ 受験料相当額",
        "報奨金: 受験料相当額"
    ),
    If(
        RadioApplicationType.Selected.Value = "資格取得宣言届",
        "報奨金: ¥" & Text(
            LookUp(
                資格マスタ,
                Title = DropdownQualification.Selected.Value && 詳細 = DropdownDetail.Selected.Value,
                報奨金
            ),
            "#,##0"
        ) & " + ¥5,000（事前申請ボーナス）",
        "報奨金: ¥" & Text(
            LookUp(
                資格マスタ,
                Title = DropdownQualification.Selected.Value && 詳細 = DropdownDetail.Selected.Value,
                報奨金
            ),
            "#,##0"
        )
    )
)
```

#### 表示パターン一覧

| 報奨金 | 申請種別 | 表示 |
|--------|---------|------|
| 0円（FP3級など） | 資格取得宣言届 | ¥5,000（事前申請ボーナス）+ 受験料相当額 |
| 0円（FP3級など） | 資格取得届 | 受験料相当額 |
| 通常 | 資格取得宣言届 | ¥XX,XXX + ¥5,000（事前申請ボーナス） |
| 通常 | 資格取得届 | ¥XX,XXX |

### 3.10 申請ボタン
1. 「挿入」→「ボタン」
2. 名前: `ButtonSubmit`
3. Text: `"申請する"`
4. OnSelect:
```
Patch(
    資格取得申請,
    Defaults(資格取得申請),
    {
        タイトル: DropdownQualification.Selected.Value,
        申請種別: {Value: RadioApplicationType.Selected.Value},
        申請日: Today(),
        予定日_取得日: DatePickerAcquisition.SelectedDate,
        理由_内容: TextInputReason.Text,
        ステータス: {Value: "申請中"},
        報奨金額: LookUp(
            資格マスタ,
            Title = DropdownQualification.Selected.Value && 詳細 = DropdownDetail.Selected.Value,
            報奨金
        ),
        事前ボーナス: If(RadioApplicationType.Selected.Value = "資格取得宣言届", 5000, 0)
    }
); Navigate(Screen2, ScreenTransition.Fade)
```

> **重要**: Distinct使用後は `.Selected.Value` を使用し、報奨金は `LookUp()` で取得します。

---

## 4. Screen2（申請完了画面）作成

### 4.1 コンポーネント配置

#### 完了メッセージ
1. テキストラベル追加
2. Text: `"申請が完了しました"`
3. フォントサイズ: 20

#### サブメッセージ
1. テキストラベル追加
2. Text: `"承認者に通知が送信されました。結果をお待ちください。"`

#### 戻るボタン
1. ボタン追加
2. Text: `"新しい申請を作成"`
3. OnSelect: `Navigate(Screen1, ScreenTransition.Fade)`

---

## 5. 入力検証

### 5.1 必須チェック
ButtonSubmitのDisplayModeを設定:
```
If(
    IsBlank(DropdownCategory.Selected) ||
    IsBlank(DropdownQualification.Selected) ||
    IsBlank(DropdownDetail.Selected) ||
    IsBlank(DatePickerAcquisition.SelectedDate) ||
    IsBlank(TextInputReason.Text),
    DisplayMode.Disabled,
    DisplayMode.Edit
)
```

### 5.2 日付検証（宣言届の場合）
予定日が1ヶ月以上先かチェック:
```
If(
    RadioApplicationType.Selected.Value = "資格取得宣言届" &&
    DatePickerAcquisition.SelectedDate < DateAdd(Today(), 30, Days),
    Notify("事前申請ボーナスを受けるには、受験予定日を1ヶ月以上先に設定してください", NotificationType.Warning)
)
```

---

## 6. デザイン調整

### 6.1 テーマ設定
1. 「テーマ」→ 会社のブランドカラーに合わせる
2. または以下を手動設定:
   - Primary: #0078D4（青）
   - Background: #F3F2F1（グレー）

### 6.2 レスポンシブ対応
1. アプリ設定 →「画面サイズとスケーリング」
2. 「画面に合わせてスケール」をON

---

## 7. 公開

### 7.1 アプリの保存と公開
1. 右上「保存」アイコン
2. 「公開」→「このバージョンの公開」

### 7.2 アプリの共有
1. 左メニュー「共有」
2. 全従業員または特定グループを追加
3. 「共有」

### 7.3 Teamsへの追加（オプション）
1. Teams → アプリ → Power Apps
2. 「自分用に追加」または「チームに追加」
3. 作成したアプリを選択

---

## 8. 画面レイアウト参考

```
┌────────────────────────────────────────────────────┐
│                  資格取得申請                        │
├────────────────────────────────────────────────────┤
│                                                    │
│  申請種別                                           │
│  ○ 資格取得宣言届（事前申請 +5,000円）              │
│  ○ 資格取得届                                      │
│                                                    │
│  ─────────────────────────────────────────────    │
│                                                    │
│  分類          [▼ 選択してください        ]        │
│                                                    │
│  資格名        [▼ 選択してください        ]        │
│                                                    │
│  詳細（級）    [▼ 選択してください        ]  ★NEW │
│                                                    │
│  ─────────────────────────────────────────────    │
│                                                    │
│  取得予定日    [ 2026 / 03 / 15 ]    ←動的ラベル   │
│                                                    │
│  理由                                              │
│  ┌──────────────────────────────────────────┐    │
│  │ キャリアアップのため、簿記2級の取得を      │    │
│  │ 目指します。                               │    │
│  └──────────────────────────────────────────┘    │
│                                                    │
│  ─────────────────────────────────────────────    │
│                                                    │
│  報奨金: ¥10,000 + ¥5,000（事前申請ボーナス）      │
│                                                    │
│              [ 申請する ]                          │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 9. トラブルシューティング

### よくある問題

| 問題 | 解決方法 |
|------|---------|
| ドロップダウンにデータが表示されない | データソース接続を確認、Filterの条件を確認 |
| 申請ボタンが押せない | 必須項目の入力を確認 |
| 保存時にエラー | SharePointリストの列名とPatchの項目名が一致しているか確認 |
| ユーザー情報が取得できない | User()関数の権限を確認 |
| 「名前が無効です」エラー | コントロール名が正しいか確認（上部の対応表参照） |
| 報奨金が表示されない | LookUpの条件で資格名と詳細の両方が選択されているか確認 |

### Distinct使用後の注意点
- `.Selected.Title` → `.Selected.Value` に変更が必要
- `.Selected.報奨金` は使えないため `LookUp()` で取得
