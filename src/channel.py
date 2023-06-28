import os
from googleapiclient.discovery import build
import json

api_key = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.object = self.get_service()
        self.channel = self.object.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = self.channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriberCount = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.viewCount = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title}({self.url})'

    def __add__(self, other):
        return self.subscriberCount + other.subscriberCount

    def __sub__(self, other):
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __sub__(self, other):
        return int(other.subscriberCount) - int(self.subscriberCount)

    def __gt__(self, other):
        return int(self.subscriberCount) > int(other.subscriberCount)

    def __ge__(self, other):
        return int(self.subscriberCount) >= int(other.subscriberCount)

    def __lt__(self, other):
        return int(self.subscriberCount) < int(other.subscriberCount)

    def __le__(self, other):
        return int(self.subscriberCount) <= int(other.subscriberCount)

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=api_key)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    def to_json(self, filename):
        channel_info = {"title": self.title,
                        "channel_id": self.channel_id,
                        "description": self.description,
                        "url": self.url,
                        "subscriberCount": self.subscriberCount,
                        "video_count": self.video_count,
                        "viewCount": self.viewCount}
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(channel_info, file, indent=4, ensure_ascii=False)

