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

    DB_PATH = 'nanakapedia/wikipedia_abstract.db'
    """Wikipedia要約データベースのファイルパス"""
    TABLE_NAME = 'abstract'
    """Wikipedia要約データテーブル名"""

    def __init__(self):
        """
        インスタンス変数の設定
        """

        self.dump_file_path = '../../data/jawiki-latest-abstract.xml'
        """Wikipedia要約ダンプデータのファイルパス"""
        self.file_line_count = 0
        """Wikipedia要約ダンプデータファイルの行数"""
        self.read_line_count = 0
        """Wikipedia要約ダンプデータファイルを読み込んだ行数"""

    def set_abstract_dump_file(self, file_path):
        """
        データベースへ登録するWikipedia要約ダンプデータを指定する

        Return:
            None
        """
        self.dump_file_path = file_path

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

        conn = sqlite3.connect(WikipediaAbstract.DB_PATH)
        """データベースに接続"""
        c = conn.cursor()

        c.execute("create table IF NOT EXISTS {}(title text, abstract text)".format(WikipediaAbstract.TABLE_NAME))
        """テーブルが存在しない場合は作成"""

        # 要約データをパースして、タイトルと要約をデータベースへ登録する
        for body in self.file_read_generator():
            soup = BeautifulSoup(body, 'html.parser')
            c.execute("INSERT INTO {} VALUES (?,?)".format(WikipediaAbstract.TABLE_NAME), (soup.title.get_text().replace("Wikipedia: ", ""), soup.abstract.get_text()))

        conn.commit()
        """コミットする"""
        conn.close()
        """データベースから切断する"""

    def get_random_abstract_from_db(self) -> dict:
        """
        データベースからランダムにWikipedia要約データを取得する。

        Returns:
            data (dict): データベースから取得したWikipedia要約データ
        """

        # データベースに接続
        conn = sqlite3.connect(WikipediaAbstract.DB_PATH)
        # データベースから取得したデータに列名でアクセス可能にする
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # データベースからランダムに要約データを1件取得
        c.execute("SELECT * FROM {} ORDER BY RANDOM() limit 1".format(WikipediaAbstract.TABLE_NAME))

        # 取得した要約データを格納
        data = {}
        fetched_data = c.fetchone()
        data['title'] = fetched_data['title']
        data['abstract'] = fetched_data['abstract']

        conn.commit()
        conn.close()

        return data


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

