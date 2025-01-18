import musicscore_spider
import threading
import time

def single_thread():
    print("single_thread begins")
    while musicscore_spider.url_set.has_new_url():
        curr_url = musicscore_spider.url_set.get_url()
        musicscore_spider.c_p(curr_url, musicscore_spider.target)
    print("single_thread ends")


def multi_thread():
    print("multi_thread begins")
    threads = []
    for url in musicscore_spider.urls:
        threads.append(
            threading.Thread(target=musicscore_spider.c_p, args=(url, musicscore_spider.target))
        )

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("multi_thread ends")


if __name__ == "__main__":
    begin = time.time()
    single_thread()
    end = time.time()
    print("single_thread costs:", end - begin, "second")

    begin = time.time()
    multi_thread()
    end = time.time()
    print("multi_thread costs:", end - begin, "second")
