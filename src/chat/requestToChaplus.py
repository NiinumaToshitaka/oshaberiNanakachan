"""Chaplusを利用して、入力メッセージに対応する応答文を取得する。
"""

import requests
import json
from pprint import pprint
import chat.ChaplusAPIKey as Key


class Chaplus:
    """Chaplusを扱うクラス。
    APIの仕様は2020/05/24時点の[公式マニュアル](https://k-masashi.github.io/chaplus-api-doc/ChatAPI.html)に基づく。
    """

    class AgentTone:
        """エージェントの口調"""
        normal = "normal"
        """標準"""
        kansai = "kansai"
        """関西弁風"""
        koshu = "koshu"
        """甲州弁風"""
        dechu = "dechu"
        """デチュ語"""

    requestURL = 'https://www.chaplus.jp/v1/chat'
    """APIのリクエストURL"""

    DEFAULT_PARAMETER = {
        "utterance": "おはよう",
        "username": "お父様",
        "agentState": {
            "agentName": "七香",
            "tone": AgentTone.normal,
            "age": "12歳",
        }
    }
    """パラメータの初期値。
    各パラメータの詳細は<https://k-masashi.github.io/chaplus-api-doc/ChatAPI.html>を参照。
    """

    AUTH = {"apikey": Key.API_KEY}
    """ユーザ認証に使用するパラメータ"""

    def __init__(self):
        """パラメータの初期設定
        """
        self.parameter = Chaplus.DEFAULT_PARAMETER.copy()
        self.response_all = None
        self.response_body = None

    def restore_default(self):
        """パラメータを初期値に戻す

        Returns:
            Chaplus
        """
        self.parameter = Chaplus.DEFAULT_PARAMETER.copy()
        return self

    def set_utterance(self, utterance: str):
        """ユーザの発話を設定

        Args:
            utterance (str): ユーザの発話

        Returns:
            Chaplus:
        """
        self.parameter["utterance"] = utterance
        return self

    def set_username(self, username: str):
        """ユーザの名前（呼び名）を設定

        Args:
            username (str): ユーザの名前（呼び名）

        Returns:
            Chaplus:
        """
        self.parameter["username"] = username
        return self

    def set_agent_state(self, agent_name: 'str' = None, tone: 'AgentTone' = None, age: 'int' = None):
        """エージェント情報を設定

        Args:
            agent_name (str): エージェントの名前
            tone (AgentTone): エージェントの口調
            age (int): エージェントの年齢（0以上）

        Returns:
            Chaplus:
        """

        if agent_name:
            self.parameter["agentState"]["agentName"] = agent_name

        if tone:
            self.parameter["agentState"]["tone"] = tone
        else:
            # [TODO] 口調がリストにない場合の処理
            pass

        if isinstance(age, int) and 0 <= age:
            self.parameter["agentState"]["age"] = "{}歳".format(age)
        else:
            # [TODO] 年齢が不正な場合の処理
            pass

        return self

    def request_to_chaplus(self):
        """リクエストを投げる

        Returns:
            Chaplus:
        """

        self.response_all = requests.post(Chaplus.requestURL, params=Chaplus.AUTH, data=json.dumps(self.parameter))

        if self.response_all.status_code is requests.codes.ok:
            self.response_body = self.response_all.json()
            print("finish request to Chaplus.")
        else:
            print("[ERROR] The request to Chaplus failed. status_code: {}".format(self.response_all.status_code))
        return self

    def print_response(self):
        pprint("response_all: {}".format(self.response_all))
        pprint("response_all.url: {}".format(self.response_all.url))
        pprint("response_body: {}".format(self.response_body))

    def get_best_response(self) -> str:
        """最もスコアの高い応答文を取得する

        Returns:
            (str): 最もスコアの高い応答文。応答文を取得できなかった場合は空の文字列を返す。
        """
        if self.response_body is None:
            return ""
        else:
            # 応答文に改行文字が入っているので削除する
            return self.response_body["bestResponse"]["utterance"].rstrip()


def test():
    # 入力メッセージに対応する応答文を取得
    input_message = "今日も仕事が大変だったよ"
    chaplus = Chaplus()
    print("chaplus.parameter")
    pprint(chaplus.parameter)
    chaplus.set_agent_state("hoge", chaplus.AgentTone.kansai, 20)
    chaplus.set_utterance(input_message)
    print("chaplus.parameter (after setting)")
    pprint(chaplus.parameter)
    best_response = chaplus.get_best_response()
    print("best_response before request: {}".format(best_response))
    best_response = chaplus.request_to_chaplus().get_best_response()
    print("best_response: {}".format(best_response))


if __name__ == '__main__':
    test()
