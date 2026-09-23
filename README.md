# Data Pipeline Portfolio

CSV形式のデータをPythonで検証・加工し、MySQLへ登録した後、
SQLで集計してCSVレポートを出力するデータパイプラインです。

Python、pandas、MySQL、SQLを組み合わせ、
データの「取り込み → 検証 → 登録 → 集計 → 出力」までを
一連の処理として自動化しています。

---

## 1. プロジェクト概要

本プロジェクトでは、CSV形式で受け取った売上データを対象として、
以下のデータパイプラインを構築しました。

```text
CSV
 ↓
Python / pandas
 ↓
データバリデーション
 ↓
商品マスタチェック
 ↓
重複チェック
 ↓
MySQL
 ↓
SQL集計
 ↓
CSVレポート
````

最終的には `main.py` を実行するだけで、
一連の処理を自動的に実行できます。

```bash
python main.py
```

---

## 2. データパイプライン構成

```text
                    ┌─────────────────┐
                    │   sales.csv     │
                    │  CSV入力データ   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   validate.py   │
                    │                 │
                    │ ・必須項目確認   │
                    │ ・数値チェック   │
                    │ ・マスタ確認     │
                    │ ・重複チェック   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ load_mysql.py   │
                    │                 │
                    │ 新規データのみ   │
                    │ MySQLへ登録      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     MySQL       │
                    │    sales DB     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ aggregation.sql │
                    │                 │
                    │ SQLによる集計    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │export_report.py │
                    │                 │
                    │ CSVレポート出力  │
                    └─────────────────┘
```

---

## 3. 使用技術

| 技術            | 用途              |
| ------------- | --------------- |
| Python        | データ処理・パイプライン制御  |
| pandas        | CSV読み込み・データ加工   |
| SQLAlchemy    | PythonとMySQLの接続 |
| PyMySQL       | MySQL接続         |
| MySQL         | データ保存           |
| SQL           | データ集計           |
| python-dotenv | DB接続情報の環境変数管理   |
| Git           | バージョン管理         |
| GitHub        | ソースコード管理・公開     |

---

## 4. データバリデーション

`validate.py` では、MySQLへ登録する前に
CSVデータのチェックを行います。

### 基本チェック

以下の項目を確認します。

* 必須列の存在確認
* 日付の確認
* 商品名の確認
* 都道府県の確認
* 数量の数値チェック
* 売上金額の数値チェック

エラーとなったデータは、

```text
output/error.csv
```

へ出力します。

---

## 5. 商品マスタチェック

売上データの商品名が、
MySQLの商品マスタに存在するか確認します。

例えば、

```text
A商品
B商品
C商品
```

が商品マスタに存在する一方で、

```text
D商品
```

が存在しない場合、

`D商品` のデータをマスタエラーとして検出します。

結果は、

```text
output/master_error.csv
```

へ出力します。

---

## 6. 重複データの防止

MySQLにすでに存在するデータと、
CSVから読み込んだデータを比較します。

以下の項目を組み合わせて重複を判定しています。

```text
日付
商品名
都道府県
数量
売上金額
```

重複データは、

```text
output/duplicate.csv
```

へ出力します。

新規データだけを、

```text
output/new_data.csv
```

へ出力し、MySQLへの登録対象とします。

---

## 7. MySQLへの登録

`load_mysql.py` では、
`new_data.csv` に含まれる新規データだけを
MySQLの `sales` テーブルへ登録します。

同じCSVを再度処理しても、
すでに登録済みのデータは重複として判定されるため、
二重登録を防止できます。

---

## 8. SQLによる集計

`sql/aggregation.sql` では、
MySQLに登録されたデータを都道府県単位で集計しています。

現在は以下の項目を集計しています。

* 件数
* 数量合計
* 売上合計
* 平均売上

例えば、

```sql
SELECT
    `都道府県`,
    COUNT(*) AS `件数`,
    SUM(`数量`) AS `数量合計`,
    SUM(`売上金額`) AS `売上合計`,
    AVG(`売上金額`) AS `平均売上`
FROM sales
GROUP BY `都道府県`
ORDER BY `売上合計` DESC;
```

というSQLを使用しています。

---

## 9. レポート出力

`export_report.py` でSQLを実行し、
集計結果をCSVとして出力します。

```text
output/sales_report.csv
```

---

## 10. ディレクトリ構成

```text
data_pipeline_portfolio/
│
├─ data/
│  └─ sales.csv
│
├─ src/
│  ├─ main.py
│  ├─ validate.py
│  ├─ load_mysql.py
│  └─ export_report.py
│
├─ sql/
│  └─ aggregation.sql
│
├─ output/
│  └─ 実行時に生成されるファイル
│
├─ .gitignore
└─ README.md
```

---

## 11. 実行方法

### 必要なPythonパッケージ

```bash
pip install pandas sqlalchemy pymysql python-dotenv
```

### MySQLの準備

MySQLに `sales_db` データベースを作成し、
必要なテーブルを準備します。

### `.env` の設定

プロジェクトのルートディレクトリに `.env` を作成します。

```text
DB_USER=root
DB_PASSWORD=自分のMySQLパスワード
DB_HOST=localhost
DB_NAME=sales_db
```

`.env` は `.gitignore` に登録しているため、
GitHubには公開されません。

### CSVの配置

処理したいCSVデータを、

```text
data/sales.csv
```

に配置します。

### パイプライン実行

`src` ディレクトリへ移動し、

```bash
python main.py
```

を実行します。

---

## 12. 実行結果

実行すると、以下のような処理結果が生成されます。

```text
output/
├─ error.csv
├─ master_error.csv
├─ duplicate.csv
├─ new_data.csv
├─ valid.csv
└─ sales_report.csv
```

`output/` は実行時に生成される結果ファイルのため、
GitHubでは管理対象から除外しています。

---

## 13. セキュリティ

MySQLの接続情報はPythonコードに直接記述せず、
`.env` から読み込む方式にしています。

```python
DB_PASSWORD = os.getenv("DB_PASSWORD")
```

`.env` は `.gitignore` に登録しているため、
GitHubへ公開されません。

---

## 14. Gitによるバージョン管理

本プロジェクトではGitを使用して、
コードの変更履歴を管理しています。

基本的な更新手順は以下の通りです。

```bash
git status
git add .
git commit -m "変更内容"
git push
```

---

## 15. 今後の発展

現在はローカル環境で動作するデータパイプラインですが、
今後は以下の技術を追加してクラウド環境へ発展させる予定です。

```text
現在
CSV
 ↓
Python
 ↓
MySQL
 ↓
SQL
 ↓
CSV

        ↓

今後
AWS S3
 ↓
Python / ETL
 ↓
AWS上のデータ基盤
 ↓
データウェアハウス
 ↓
SQL
 ↓
BI / 分析
```

また、

* Linux
* Docker
* AWS
* GitHub
* 定期実行
* API連携

などを追加し、より実務に近いデータエンジニアリング環境へ
発展させる予定です。



