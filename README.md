# 自分のブログ記事をIBM Watson Personality Insightsに突っ込んで分析してみる・2020/01 版

こちらは、

 - **[自分のブログ記事をIBM Watson Personality Insightsに突っ込んで分析してみる](https://qiita.com/hmatsu47/items/cba33dca86553c0af161)**

を 2020/01 現在のサービス／SDK に対応させたものです。

詳しくは↑の記事を参照してください。

## 準備

※Amazon Linux2 を使う場合の例です。

```bash:
$ sudo yum install python3 gcc gcc-c++

...

$ python3 -m venv dev
$ . dev/bin/activate
(dev) mkdir watsontest
(dev) $ cd watsontest
(dev) $ pip install readability-lxml -t ./

...

(dev) $ pip install reppy --upgrade -t ./

...

(dev) $ pip install --upgrade ibm-watson -t ./

...

(dev) $ vi blog_insights.py

...

```

## 実行（例）

```bash:
(dev) $ python3 blog_insights.py
http://qiita.com/hmatsu47
http://qiita.com/hmatsu47/items/ceb75caf46e3c761095d
☆append☆
http://qiita.com/hmatsu47/items/ceb75caf46e3c761095d/patches

...

□抽出文書□

...

◇プロファイリング開始◇
{
  "word_count": 41061,
  "processed_language": "ja",
  "personality": [
    {
      "trait_id": "big5_openness",
      "name": "知的好奇心",
      "category": "personality",
      "percentile": 0.9972971598081017,
      "raw_score": 0.7062875763568164,
      "significant": true,
      "children": [
        {
          "trait_id": "facet_adventurousness",
          "name": "大胆性",
          "category": "personality",
          "percentile": 0.9689564593609498,
          "raw_score": 0.6829363397292659,
          "significant": true
        },

...

    {
      "consumption_preference_category_id": "consumption_preferences_volunteering",
      "name": "ボランティア精神",
      "consumption_preferences": [
        {
          "consumption_preference_id": "consumption_preferences_volunteer",
          "name": "社会貢献のためにボランティア活動をする傾向があります",
          "score": 1.0
        }
      ]
    }
  ],
  "warnings": []
}
```
