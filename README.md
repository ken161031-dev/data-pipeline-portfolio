# Data Pipeline Portfolio

CSVデータをPythonで検証・加工し、MySQLへ登録した後、
SQLで集計してCSVレポートを出力するデータパイプラインです。

## 概要

このプロジェクトでは、以下の処理を自動化しています。

CSV
↓
Python / pandas
↓
データバリデーション
↓
重複チェック
↓
MySQL登録
↓
SQL集計
↓
CSVレポート出力

## 使用技術

- Python
- pandas
- SQLAlchemy
- PyMySQL
- MySQL
- SQL
- Git
- GitHub

## 主な機能

### 1. CSV読み込み

`data/sales.csv` をPythonで読み込みます。

### 2. データバリデーション

以下のデータをチェックします。

- 必須項目の確認
- 数量・売上金額の数値チェック
- 商品マスタとの照合
- MySQL既存データとの重複チェック

エラーや重複したデータは、それぞれCSVとして出力します。

### 3. MySQL登録

検証を通過した新規データだけをMySQLへ登録します。

同じデータを再度投入した場合は、重複として判定し、
二重登録を防止します。

### 4. SQL集計

MySQLに登録されたデータをSQLで集計します。

現在は都道府県ごとに、

- 件数
- 数量合計
- 売上合計
- 平均売上

を集計しています。

### 5. レポート出力

集計結果を、

`output/sales_report.csv`

として出力します。

## ディレクトリ構成

```text
data_pipeline_portfolio/
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