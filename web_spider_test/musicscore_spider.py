import requests
from bs4 import BeautifulSoup
import url_manager
import time

# 定义请求头
url1 = "https://www.jianpu.net/jianpu/"
url2 = "https://www.qupu123.com/qiyue/pipa"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
}


# url1爬虫函数
def crawl1(url_name, target_name):
    try:
        resp = requests.get(url_name, headers=headers)
        resp.encoding = "gb2312"
        resp.raise_for_status()
        time.sleep(1)
    except requests.RequestException as e:
        print(f"Error: {e}")
        return

    # 解析HTML，获取歌名
    soup = BeautifulSoup(resp.text, "html.parser")
    all_titles = soup.find_all("dt", attrs={"class": "l1"})
    for title in all_titles:
        song_name = title.find("a").get_text()
        if not song_name:
            continue

        # 判断歌名与输入是否相等
        if target_name in song_name:
            href = title.find("a").get("href")
            if not href:
                print("Error:href not found")
                continue
            print("found:\n", f"https://www.jianpu.net{href}")
            break


# url2爬虫函数
def crawl2(url_name, target_name):
    try:
        resp = requests.get(url_name, headers=headers)
        resp.encoding = "utf-8"
        resp.raise_for_status()
        time.sleep(1)
    except requests.RequestException as e:
        print(f"Error: {e}")
        return

    # 解析HTML，获取歌名
    soup = BeautifulSoup(resp.text, "html.parser")
    all_titles = soup.find_all("td", attrs={"class": "f1"})
    for title in all_titles:
        song_name = title.find("a").get_text()
        if not song_name:
            continue

        # 判断歌名与输入是否相等
        if target_name in song_name:
            href = title.find("a").get("href")
            if not href:
                print("Error:href not found")
                continue
            print("found:\n", f"https://www.qupu123.com{href}")
            break


if __name__ == "__main__":
    # 输入目标歌名
    target = input("input the song\'s name:")
    # 建立URL管理器
    url_set = url_manager.UrlManager()
    url_set.add_new_url(url1)
    url_set.add_new_url(url2)

    # 在new_urls中爬取
    while url_set.has_new_url():
        curr_url = url_set.get_url()
        if curr_url == url1:
            total_page = 3
            for page in range(1, total_page + 1):
                url_temp = url1 + f"2_{page}.html"
                crawl1(url_temp, target)
        if curr_url == url2:
            total_page = 3
            for page in range(1, total_page + 1):
                url_temp = url2 + f"/{page}.html"
                crawl2(url_temp, target)
