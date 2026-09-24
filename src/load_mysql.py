import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")



def load_mysql():

    print("=== MySQL登録開始 ===")

    engine = create_engine(
    	f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )

    df = pd.read_csv(
        "../output/new_data.csv",
        encoding="utf-8-sig"
    )

    print(f"登録対象: {len(df)}件")

    # 登録対象が0件なら終了
    if df.empty:
        print("新規登録データがありません。")
        print("=== MySQL登録終了 ===")
        return

    try:

        df.to_sql(
            "sales",
            con=engine,
            if_exists="append",
            index=False
        )

        print(f"登録成功: {len(df)}件")

    except Exception as e:

        print("登録エラー:")
        print(e)

    print("=== MySQL登録終了 ===")


if __name__ == "__main__":
    load_mysql()