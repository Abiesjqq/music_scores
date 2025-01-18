import requests
from bs4 import BeautifulSoup
import url_manager
import time

# 定义请求头
urls = [
    "https://www.jianpu.net/jianpu/",
    "https://www.qupu123.com/qiyue/pipa",
    "https://www.2qupu.com/pipa/"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
}


def crawl(url_name):
    try:
        resp = requests.get(url_name, headers=headers)
        time.sleep(1)
    except requests.RequestException as e:
        print(f"Error: {e}")
        return

    if "jianpu" in url:
        resp.encoding = "gb2312"
    elif "qupu123" in url or "2qupu" in url:
        resp.encoding = "utf-8"
    else:
        resp.encoding = resp.apparent_encoding

    return resp.text


def parse_1(html, target_name):
    # 解析HTML，获取歌名
    soup = BeautifulSoup(html, "html.parser")
    all_titles = soup.find_all("dt", attrs={"class": "l1"})
    for title in all_titles:
        song_name = title.find("a").get_text()
        if not song_name:
            continue

        # 判断歌名与输入是否相等a
        if target_name in song_name:
            href = title.find("a").get("href")
            if not href:
                print("Error:href not found")
                continue
            print(f"found:{song_name}\n", f"https://www.jianpu.net{href}")


def parse_2(html, target_name):
    # 解析HTML，获取歌名
    soup = BeautifulSoup(html, "html.parser")
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
            print(f"found:{song_name}\n", f"https://www.qupu123.com{href}")


def parse_3(html, target_name):
    # 解析HTML，获取歌名
    soup = BeautifulSoup(html, "html.parser")
    all_titles = soup.find_all("td", attrs={"class": "td2"})

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
            print(f"found:{song_name}\n", href)


def c_p(url_name, target_name):
    if "jianpu" in url_name:
        total_page = 5
        for page in range(1, total_page + 1):
            url_temp = url_name + f"2_{page}.html"
            parse_1(crawl(url_temp), target_name)
    elif "qupu123" in url_name:
        total_page = 5
        for page in range(1, total_page + 1):
            url_temp = url_name + f"/{page}.html"
            parse_2(crawl(url_temp), target_name)
    elif "2qupu" in url_name:
        total_page = 5
        parse_3(crawl(url_name), target_name)
        for page in range(2, total_page + 1):
            url_temp = url_name + f"{page}.html"
            parse_3(crawl(url_temp), target_name)


# 输入目标歌名
target = input("input the song\'s name:")
# 建立URL管理器
url_set = url_manager.UrlManager()
for url in urls:
    url_set.add_new_url(url)

if __name__ == "__main__":
    url_temp = "https://www.2qupu.com/pipa/"
    resp = requests.get(url_temp, headers=headers)
    resp.encoding = "utf-8"
    if resp.status_code == 200:
        pass
    else:
        print(resp.status_code)

    c_p(url_temp, target)

