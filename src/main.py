# coding:utf-8
import RPi.GPIO as GPIO
import time
from oshaberiNanakaChan import main

# codamaのwake up wordが検出されるとhighになるGPIOの番号
CODAMA_TRIGGERD_GPIO = 27


# ウェイクアップワードを検出したときに実行されるコールバック関数
# 別スレッドで実行される
def detected(value):
    print("detected wake-up-word")


# 終了処理
# これを実行しないと、このスクリプトを再度実行したとき失敗する
def cleanup():
    print("cleanup codama gpio")
    GPIO.setmode(GPIO.BCM)
    GPIO.remove_event_detect(CODAMA_TRIGGERD_GPIO)
    GPIO.cleanup()


# 初期設定
def codama_setup():
    # GPIOピンのチャンネルの指定方法を設定
    GPIO.setmode(GPIO.BCM)
    # チャンネルのモード設定
    # 指定したチャンネルを入力モードにする
    GPIO.setup(CODAMA_TRIGGERD_GPIO, GPIO.IN)
    # エッジ検出イベントの発生状態を取得
    # 指定したチャンネルで立ち上がりエッジ検出イベントが発生すると、コールバック関数を呼び出す
    GPIO.add_event_detect(CODAMA_TRIGGERD_GPIO, GPIO.RISING, callback=detected)


if __name__ == "__main__":
    try:
        codama_setup()
        print("Wait for wakeup word input...")
        while True:
            # ウェイクワードを検出したらメイン処理を実行する
            if GPIO.input(CODAMA_TRIGGERD_GPIO) == GPIO.HIGH:
                print("Detect wakeup word.")
                main()
                break
            # ウェイクワードを検出していなければ待つ
            time.sleep(0.1)
    except KeyboardInterrupt:
        cleanup()
    finally:
        cleanup()

