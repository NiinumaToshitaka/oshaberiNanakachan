"""
Wikipedia要約データダンプファイルから、
記事のタイトルと要約文を抽出して、
SQLiteデータベースに格納する。
"""

import sqlite3
from bs4 import BeautifulSoup
import sys


class WikipediaAbstract:
    """
    Wikipedia要約データを扱うクラス
    """

    def __init__(self):
        """
        インスタンス変数の設定
        """

        self.db_path = 'wikipedia_abstract.db'
        """Wikipedia要約データベースのファイルパス"""
        self.table_name = 'abstract'
        """Wikipedia要約データテーブル名"""
        self.dump_file_path = '../../data/jawiki-latest-abstract.xml'
        """Wikipedia要約ダンプデータのファイルパス"""
        self.file_line_count = 0
        """Wikipedia要約ダンプデータファイルの行数"""
        self.read_line_count = 0
        """Wikipedia要約ダンプデータファイルを読み込んだ行数"""

    def file_read_generator(self):
        """
        XMLをパースして<doc> 〜 </doc>を読み込み返却するgenerator
        参考：[巨大なWikipedia全ページ要約xmlをジェネレータを使って良い感じに扱う - Qiita]<https://qiita.com/haminiku/items/faa6e4f20b4d94896834>

        Yields:
            result: 指定範囲をパースしたテキスト
        """

        separate = '</doc>'
        """パースする単位となる範囲のタグ"""
        txt = ''
        """パースしたテキスト"""

        with open(self.dump_file_path, 'r') as f:
            # Fileを1行ずつ読む
            for line in f:
                txt += line
                self.read_line_count += 1
                if separate in line:
                    result = txt
                    txt = ''
                    # パースしたテキストを返す
                    yield result

                # 進捗状況を表示。1000行処理するごとに進捗度を更新する
                if self.read_line_count % 1000 == 0:
                    sys.stdout.write("\r")
                    sys.stdout.write("{0:.2%}".format((self.read_line_count / self.file_line_count)))
                    sys.stdout.flush()

    def insert_dump_data_to_db(self):
        """
        Wikipedia要約データをデータベースへ登録する

        Returns:
            None
        """

        self.file_line_count = len(open(self.dump_file_path).readlines())

        conn = sqlite3.connect(self.db_path)
        """データベースに接続"""
        c = conn.cursor()

        c.execute("create table IF NOT EXISTS {}(title text, abstract text)".format(self.table_name))
        """テーブルが存在しない場合は作成"""

        # 要約データをパースして、タイトルと要約をデータベースへ登録する
        for body in self.file_read_generator():
            soup = BeautifulSoup(body, 'html.parser')
            c.execute("INSERT INTO {} VALUES (?,?)".format(self.table_name), (soup.title.get_text().replace("Wikipedia: ", ""), soup.abstract.get_text()))

        conn.commit()
        """コミットする"""
        conn.close()
        """データベースから切断する"""


def main():
    """
    メイン処理
    Returns:
        None
    """

    controller = WikipediaAbstract()
    # 要約データをデータベースへ登録
    controller.insert_dump_data_to_db()


if __name__ == '__main__':
    main()
