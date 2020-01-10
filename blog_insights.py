import json
import urllib.request
from lxml.html import fromstring
from readability.readability import Document
from reppy.cache import RobotsCache
from time import sleep
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import PersonalityInsightsV3

# 開始URL
start_url = "http://qiita.com/hmatsu47"
# ドメイン
domain = "http://qiita.com/"
# 探索対象URLパス
scrape_path = "http://qiita.com/hmatsu47/items/"
# 探索対象外URL文字列
exclude_str_list = ["feed", "rss", "archive", "about", "revision", "like", "follow", "contribution", "comment", "reference", ".md"]
# 探索済みURL
scrape_url_list = []
# 抽出した本文
summary_ap_text = []
# 探索する最大ページ数
crawl_limit = 100
# 本文を抽出する最大ページ数
item_limit = 50
# robots.txt判定用
robots_cache = RobotsCache(capacity=crawl_limit)
# Watson認証情報
apikey = '【APIキー】'
url = '【APIのURL】'
# 対象外URLが含まれていないか判定
def is_crawlable_url(url):
  for es in exclude_str_list:
    if url.find(es) != -1:
      break
  else:
    robots_flag = robots_cache.allowed(domain, "*")
    return (robots_flag)
  return False

# 探索
def crawl(url):
  # 探索最大ページ数に達していれば何もしない
  if crawl_limit <= len(scrape_url_list):
    return
  # 探索対象かどうか判定
  if (len(summary_ap_text) < item_limit) and (url not in scrape_url_list) and (is_crawlable_url(url)):
    print(url)
    scrape_url_list.append(url)
    # ページHTMLを取得
    html = urllib.request.urlopen(url).read()
    # 1秒スリープする※大事なのであえてコメント！※
    sleep(1)
    # 本文抽出対象なら抽出処理を行う
    et = fromstring(html.lower())
    robots = et.xpath("//meta[@name='robots']/@content")
    if (url.startswith(scrape_path)) and not ("nofollow" in robots):
      summary = Document(html).summary()
      et2 = fromstring(summary)
      text = "".join([text for text in et2.xpath("//text()") if text.strip()])
      print("☆append☆")
      summary_ap_text.append(text)
    # リンクを抽出する
    et.make_links_absolute(domain)
    ev_url_list = et.xpath("//@href")
    # 抽出したリンクの先を探索する
    for evurl in ev_url_list:
      if evurl.startswith(start_url):
        crawl(evurl)

# 処理メイン

# 開始URLから探索する
crawl(start_url)
# 抽出文書の表示
print("□抽出文書□")
print(" ".join(summary_ap_text))
# Personality Insightsの認証
print("◇プロファイリング開始◇")
authenticator = IAMAuthenticator(apikey)
personality_insights = PersonalityInsightsV3(
  version="2017-10-13",
  authenticator=authenticator)
personality_insights.set_service_url(url)
# プロファイリング
profile = personality_insights.profile(
  " ".join(summary_ap_text).encode("utf-8"),
  content_type="text/plain", content_language="ja",
  accept="application/json", accept_language="ja",
  raw_scores=True, consumption_preferences=True).get_result()
# 結果を表示する
print(json.dumps(profile, indent=2, ensure_ascii=False))
