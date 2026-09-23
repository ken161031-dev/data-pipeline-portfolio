from validate import validate
from load_mysql import load_mysql
from export_report import export_report


def main():

    print("==============================")
    print("データパイプライン開始")
    print("==============================")

    # ① データ検証
    validate()

    print()

    # ② MySQL登録
    load_mysql()

    print()

    # ③ レポート作成
    export_report()

    print()
    print("==============================")
    print("データパイプライン完了")
    print("==============================")


if __name__ == "__main__":
    main()