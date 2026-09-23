import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")


def validate():

    print("=== データ検証開始 ===")

    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )


    # CSV読み込み
    df = pd.read_csv(
        "../data/sales.csv",
        encoding="utf-8"
    )

    print(f"CSV読み込み: {len(df)}件")

    # 必須列チェック
    required_columns = [
        "日付",
        "商品名",
        "都道府県",
        "数量",
        "売上金額"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"必要な列がありません: {column}")

    # 数値変換
    df["数量"] = pd.to_numeric(
        df["数量"],
        errors="coerce"
    )

    df["売上金額"] = pd.to_numeric(
        df["売上金額"],
        errors="coerce"
    )

    # 基本エラーチェック
    error_condition = (
        df["日付"].isna()
        | df["商品名"].isna()
        | df["都道府県"].isna()
        | df["数量"].isna()
        | df["売上金額"].isna()
    )

    error_df = df[error_condition].copy()
    valid_df = df[~error_condition].copy()

    print(f"基本エラー: {len(error_df)}件")

    error_df.to_csv(
        "../output/error.csv",
        index=False,
        encoding="utf-8-sig"
    )

    valid_df.to_csv(
        "../output/valid.csv",
        index=False,
        encoding="utf-8-sig"
    )

    # 商品マスタ確認
    products_df = pd.read_sql(
        "SELECT 商品名 FROM products",
        engine
    )

    master_check = valid_df.merge(
        products_df,
        on="商品名",
        how="left",
        indicator=True
    )

    master_error_df = master_check[
        master_check["_merge"] == "left_only"
    ].drop(columns=["_merge"])

    valid_df = master_check[
        master_check["_merge"] == "both"
    ].drop(columns=["_merge"])

    print(f"商品マスタエラー: {len(master_error_df)}件")

    master_error_df.to_csv(
        "../output/master_error.csv",
        index=False,
        encoding="utf-8-sig"
    )


    # MySQL既存データ取得
    existing_df = pd.read_sql(
        """
        SELECT
            日付,
            商品名,
            都道府県,
            数量,
            売上金額
        FROM sales
        """,
        engine
    )

    # 日付の型を統一
    valid_df["日付"] = pd.to_datetime(
    	valid_df["日付"]
    ).dt.date

    existing_df["日付"] = pd.to_datetime(
    	existing_df["日付"]
    ).dt.date

    # 重複チェック
    key_columns = [
        "日付",
        "商品名",
        "都道府県",
        "数量",
        "売上金額"
    ]

    merged = valid_df.merge(
        existing_df,
        on=key_columns,
        how="left",
        indicator=True
    )

    duplicate_df = merged[
        merged["_merge"] == "both"
    ].drop(columns=["_merge"])

    new_df = merged[
        merged["_merge"] == "left_only"
    ].drop(columns=["_merge"])

    print(f"MySQL重複: {len(duplicate_df)}件")
    print(f"新規登録: {len(new_df)}件")

    duplicate_df.to_csv(
        "../output/duplicate.csv",
        index=False,
        encoding="utf-8-sig"
    )

    new_df.to_csv(
        "../output/new_data.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("=== データ検証完了 ===")

    return len(new_df)
    

if __name__ == "__main__":
    validate()