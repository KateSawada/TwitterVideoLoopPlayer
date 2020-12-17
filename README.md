# TwitterVideoLoopPlayer
## 本プログラムについて
本プログラムは，Twitterの動画付きツイートを検索し，その結果を連続再生する機能をサーバー/クライアントで分けて実装したものになります．サーバー側はFlaskで動いています．

## 開発環境
- Python 3.7.7
    - flask 1.1.2
    - flask-cors 3.0.9
    - tweepy 3.8.0

## 使用方法
1. 環境を整える
2. main.pyを実行する `$ python main.py`
3. 表示されたアドレス・ポートにブラウザでアクセスする
4. 検索したい言葉を入力して検索ボタンを押す(デフォルトで「#深夜の2時間DTM」になっています)

## 参考
- Twitter API(tweepy)
    - https://qiita.com/KEI_y/items/2d4d32c78f88fdb16eee
    - https://thinkami.hatenablog.com/entry/2017/11/02/062226
- Flask
    - https://qiita.com/nagataaaas/items/24e68a9c736aec31948e
    - https://qiita.com/bowtin/items/194c1f3b1211d7892ab8
    - https://riptutorial.com/ja/flask/example/5831/flask-api%E3%81%8B%E3%82%89json%E3%83%AC%E3%82%B9%E3%83%9D%E3%83%B3%E3%82%B9%E3%82%92%E8%BF%94%E3%81%99
- html/css/js
    - https://nakox.jp/web/coding/chat_twitter_css

## License
See [LICENSE](/LINCENSE)