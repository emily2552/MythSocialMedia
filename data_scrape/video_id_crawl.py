import re

from concurrent.futures import ThreadPoolExecutor
from typing import Optional

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

from config import header_info
from data_scrape.single_vedio_info import combined_video_info
from utils.logger import logger

KEYWORDS = ["哪吒", "封神", "神话电影", "姜子牙", "白蛇"]


class BilibiliSearchScraper:
    def __init__(self, keyword: str):
        self.keyword = keyword
        self.url = f"https://search.bilibili.com/video?vt=52639747&keyword={keyword}"
        self.header = header_info

    def get_single_page_bvid_list(self, page: int) ->dict:
        html = requests.get(self.url + f"&page={page}", headers=self.header)
        bvid_list = re.findall(r'bvid:"(BV[0-9A-Za-z]+)"', html.text)
        return bvid_list

    def crawl_bvids(self):
        """
        从搜索页面爬搜到所有页的视频id的list
        :param url:要爬取的网页
        :return: 所有视频id的list（去重版）
        """
        options = Options()
        options.add_argument("--headless=new") # 不打开浏览器界面

        driver = webdriver.Chrome(options=options)
        driver.get(self.url)
        # html = driver.page_source  # 包含渲染后的 DOM
        # 获取总页数
        page_buttons = driver.find_elements(by="xpath",
                                            value='//div[contains(@class,"vui_pagenation")]//button[contains(@class,"vui_pagenation--btn-num")]')
        max_page = page_buttons[-1].accessible_name
        logger.info(f"{self.keyword}b站搜索页共有{max_page}页")

        bvid_list = []

        # 并发爬取
        with ThreadPoolExecutor(max_workers=30) as executor:
            logger.info(f"开始批量爬取{self.keyword}搜索页的所有视频id")
            result= tqdm(
                executor.map(self.get_single_page_bvid_list, range(1, int(max_page) + 1)),
                total=int(max_page)

            )
        logger.info("批量爬取完毕")
        for result in result:
            bvid_list.extend(result)

        # 对视频id列表的结果去重
        bvid_list = list(set(bvid_list))

        return bvid_list
    def crawl_video_infos(self,bvid_list: Optional[list] ):
        if bvid_list is None:
            bvid_list = self.crawl_bvids()
        total_bvid_list = bvid_list
        with ThreadPoolExecutor(max_workers=70) as executor:
            logger.info(f"开始批量爬取{self.keyword}搜索页的所有视频信息")
            all_vedio_infos = list(
                tqdm(
                    executor.map(combined_video_info, total_bvid_list),
                    total=len(total_bvid_list)
                )
            )
            logger.info("批量爬取视频详情信息完毕")
        return all_vedio_infos








if __name__ == "__main__":
    blibili_sracper = BilibiliSearchScraper("哪吒")
    video_ids = blibili_sracper.crawl_bvids()
    video_infos = blibili_sracper.crawl_video_infos(video_ids)
    print(video_infos[0])







