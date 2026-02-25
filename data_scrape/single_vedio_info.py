import asyncio
import json
from bilibili_api import user
from bilibili_api import video, Credential
import datetime

from config import credentials
from utils.logger import logger


class BilibiliVideoInfo:
    def __init__(self,video_id: str,credentials_info:dict|None= None):
        if credentials_info is None:
            credentials_info = credentials
        self.video_id = video_id
        self.credential = Credential(**credentials_info)
        self.v = video.Video(bvid=video_id, credential=self.credential)
        self.info = asyncio.run(self.v.get_info())

    def get_video_effects(self):
        """
        获得视频的播放量，点赞数，弹幕数，收藏数，转发数，硬币数，评论数
        :param video_id: 视频id
        :return:视频的播放量，点赞数，弹幕数，收藏数，转发数，硬币数，评论数
        """
        video_effect_elements =["view", "like", "danmaku", "favorite", "share", "coin", "reply"]
        video_state ={k: self.info.get("stat").get(k) for k in video_effect_elements}
        return video_state


    def get_video_basics(self):
        """
        获得视频的基础信息
        :param video_id: 视频id
        :return: 视频的标题，简介，发布时间，总时长
        """
        video_basic_elements = ["title", "desc", "pubdate", "pages"]
        video_basics_raw = {k: self.info.get(k) for k in video_basic_elements}
        video_basics_raw["pages"] = [{"duration": page.get("duration")} for page in video_basics_raw.get("pages")]
        total_duration = sum(page.get("duration") for page in video_basics_raw.get("pages"))
        timestamp_second = video_basics_raw.get("pubdate")
        standard_pubdate = datetime.datetime.fromtimestamp(timestamp_second).strftime("%Y-%m-%d %H:%M:%S")
        video_basics = {
            "video_id": self.video_id,
            "title": video_basics_raw.get("title"),
            "desc": video_basics_raw.get("desc"),
            "pubdate": standard_pubdate,
            "total_duration": total_duration
        }
        return video_basics

    def get_up_info(self):
        """
        获取up主信息
        :param mid: up主mid
        :return :up主的粉丝数，以及
        """
        owner= self.info.get("owner")
        u = user.User(uid=owner.get("mid"), credential=self.credential)
        info = asyncio.run(u.get_relation_info())
        selected_info = {"up_fans": info.get("follower")}
        return selected_info

def combined_video_info(video_id: str):
    """

    :param video_id: 视频id
    :param credentials_info: 凭据类，用于各种请求操作的验证。
    :return: 整合出来的单条数据 数据类型：dict
    """
    video_info = BilibiliVideoInfo(video_id)
    video_effects = video_info.get_video_effects()
    up_info = video_info.get_up_info()
    video_basics = video_info.get_video_basics()
    data = {**video_basics,**up_info, **video_effects}

    return data


if __name__ == '__main__':

    print(combined_video_info("BV147411U7WK"))


