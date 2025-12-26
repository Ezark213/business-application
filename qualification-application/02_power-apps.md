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

### 2.2 Screen1（申請フォーム）作成

#### ヘッダー部分
1. 「挿入」→「テキストラベル」
2. Text: `"資格取得申請"`
3. フォントサイズ: 24
4. 配置: 上部中央

#### 申請種別（ラジオボタン）
1. 「挿入」→「入力」→「ラジオ」
2. 名前: `RadioApplicationType`
3. Items: `["資格取得宣言届", "資格取得届"]`
4. Default: `"資格取得宣言届"`
5. Layout: `Layout.Horizontal`

#### 分類ドロップダウン
1. 「挿入」→「入力」→「ドロップダウン」
2. 名前: `DropdownCategory`
3. Items:
```
Distinct(資格マスタ, 分類)
```

#### 資格名ドロップダウン
1. 「挿入」→「入力」→「ドロップダウン」
2. 名前: `DropdownQualification`
3. Items:
```
Filter(資格マスタ, 分類 = DropdownCategory.Selected.Value)
```
4. DisplayFields: `["Title"]`

#### 詳細（級）ドロップダウン
1. 「挿入」→「入力」→「ドロップダウン」
2. 名前: `DropdownDetail`
3. Items:
```
Filter(資格マスタ,
    分類 = DropdownCategory.Selected.Value &&
    Title = DropdownQualification.Selected.Title
)
```
4. DisplayFields: `["詳細"]`

#### 日付入力
1. 「挿入」→「入力」→「日付の選択」
2. 名前: `DatePickerTarget`
3. ラベル追加:
```
If(RadioApplicationType.Selected.Value = "資格取得宣言届",
   "取得予定日",
   "取得日"
)
```

#### 理由/内容テキスト入力
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

#### 備考テキスト入力
1. 「挿入」→「入力」→「テキスト入力」
2. 名前: `TextInputRemarks`
3. Mode: `TextMode.MultiLine`
4. HintText: `"備考があれば入力してください"`

#### 報奨金表示ラベル
1. 「挿入」→「テキストラベル」
2. 名前: `LabelReward`
3. Text:
```
"報奨金: ¥" & Text(
    LookUp(資格マスタ,
        ID = DropdownDetail.Selected.ID
    ).報奨金,
    "#,##0"
) &
If(RadioApplicationType.Selected.Value = "資格取得宣言届",
   " + ¥5,000（事前申請ボーナス）",
   ""
)
```

#### 申請ボタン
1. 「挿入」→「ボタン」
2. 名前: `ButtonSubmit`
3. Text: `"申請する"`
4. OnSelect:
```
// 申請データをSharePointに登録
Patch(資格取得申請,
    Defaults(資格取得申請),
    {
        Title: "APP-" & Text(Now(), "yyyymmddhhmmss"),
        申請種別: If(RadioApplicationType.Selected.Value = "資格取得宣言届",
                    {Value: "宣言届"},
                    {Value: "取得届"}),
        申請者: {
            '@odata.type': "#Microsoft.Azure.Connectors.SharePoint.SPListExpandedUser",
            Claims: "i:0#.f|membership|" & User().Email,
            DisplayName: User().FullName,
            Email: User().Email
        },
        申請日: Today(),
        取得資格: {
            Id: DropdownDetail.Selected.ID,
            Value: DropdownQualification.Selected.Title
        },
        予定日_取得日: DatePickerTarget.SelectedDate,
        理由_内容: TextInputReason.Text,
        備考: TextInputRemarks.Text,
        ステータス: {Value: "申請中"},
        事前申請フラグ: If(RadioApplicationType.Selected.Value = "資格取得宣言届", true, false),
        報奨金額: LookUp(資格マスタ, ID = DropdownDetail.Selected.ID).報奨金,
        事前ボーナス: If(RadioApplicationType.Selected.Value = "資格取得宣言届", 5000, 0)
    }
);

// 完了画面へ遷移
Navigate(Screen2, ScreenTransition.Fade);

// フォームリセット
Reset(RadioApplicationType);
Reset(DropdownCategory);
Reset(DropdownQualification);
Reset(DropdownDetail);
Reset(DatePickerTarget);
Reset(TextInputReason);
Reset(TextInputRemarks);
```

---

## 3. Screen2（申請完了画面）作成

### 3.1 コンポーネント配置

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

## 4. 入力検証

### 4.1 必須チェック
ButtonSubmitのDisplayModeを設定:
```
If(
    IsBlank(DropdownCategory.Selected) ||
    IsBlank(DropdownQualification.Selected) ||
    IsBlank(DropdownDetail.Selected) ||
    IsBlank(DatePickerTarget.SelectedDate) ||
    IsBlank(TextInputReason.Text),
    DisplayMode.Disabled,
    DisplayMode.Edit
)
```

### 4.2 日付検証（宣言届の場合）
予定日が1ヶ月以上先かチェック:
```
If(
    RadioApplicationType.Selected.Value = "資格取得宣言届" &&
    DatePickerTarget.SelectedDate < DateAdd(Today(), 30, Days),
    Notify("事前申請ボーナスを受けるには、受験予定日を1ヶ月以上先に設定してください", NotificationType.Warning)
)
```

---

## 5. デザイン調整

### 5.1 テーマ設定
1. 「テーマ」→ 会社のブランドカラーに合わせる
2. または以下を手動設定:
   - Primary: #0078D4（青）
   - Background: #F3F2F1（グレー）

### 5.2 レスポンシブ対応
1. アプリ設定 →「画面サイズとスケーリング」
2. 「画面に合わせてスケール」をON

---

## 6. 公開

### 6.1 アプリの保存と公開
1. 右上「保存」アイコン
2. 「公開」→「このバージョンの公開」

### 6.2 アプリの共有
1. 左メニュー「共有」
2. 全従業員または特定グループを追加
3. 「共有」

### 6.3 Teamsへの追加（オプション）
1. Teams → アプリ → Power Apps
2. 「自分用に追加」または「チームに追加」
3. 作成したアプリを選択

---

## 7. 画面レイアウト参考

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
│  級・詳細      [▼ 選択してください        ]        │
│                                                    │
│  ─────────────────────────────────────────────    │
│                                                    │
│  取得予定日    [ 2025 / 03 / 15 ]                  │
│                                                    │
│  理由                                              │
│  ┌──────────────────────────────────────────┐    │
│  │ キャリアアップのため、簿記2級の取得を      │    │
│  │ 目指します。                               │    │
│  └──────────────────────────────────────────┘    │
│                                                    │
│  備考                                              │
│  ┌──────────────────────────────────────────┐    │
│  │                                           │    │
│  └──────────────────────────────────────────┘    │
│                                                    │
│  ─────────────────────────────────────────────    │
│                                                    │
│  報奨金: ¥10,000 + ¥5,000（事前申請ボーナス）      │
│  合計: ¥15,000                                    │
│                                                    │
│              [ 申請する ]                          │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 8. トラブルシューティング

### よくある問題

| 問題 | 解決方法 |
|------|---------|
| ドロップダウンにデータが表示されない | データソース接続を確認、Filterの条件を確認 |
| 申請ボタンが押せない | 必須項目の入力を確認 |
| 保存時にエラー | SharePointリストの列名とPatchの項目名が一致しているか確認 |
| ユーザー情報が取得できない | User()関数の権限を確認 |
