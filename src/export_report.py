import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")


def export_report():

    print("=== レポート作成開始 ===")

    engine = create_engine(
    	f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )

    # SQLファイル読み込み
    with open(
        "../sql/aggregation.sql",
        encoding="utf-8"
    ) as f:
        sql = f.read()

    # SQL実行
    report_df = pd.read_sql(
        sql,
        engine
    )

    print("=== 集計結果 ===")
    print(report_df)

    # CSV出力
    report_df.to_csv(
        "../output/sales_report.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\n=== レポート出力完了 ===")
    print("../output/sales_report.csv")


if __name__ == "__main__":
    export_report()