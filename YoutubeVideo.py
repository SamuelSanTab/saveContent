from bs4 import BeautifulSoup
import requests
import json

videoURL = "http://www.youtube.com/watch?v="


class VideoDetails:
    def __init__(self, video_id):
        self._ID = video_id

        response = requests.get(videoURL + video_id)
        soup = BeautifulSoup(response.text, "html.parser")

        scripts = soup.body.find_all("script")

        raw_data = next(filter(lambda x: ("var ytInitialPlayerResponse = " in x.get_text()), scripts))
        data = json.loads(raw_data.get_text().replace("var ytInitialPlayerResponse = ", "")[:-1])

        videoDetails = data['videoDetails']
        self.title = videoDetails['title']
        self.keywords = videoDetails['keywords']
        self.channelId = videoDetails['channelId']
        self.shortDescription = videoDetails['shortDescription']
        self.author = videoDetails['author']
        self.isPrivate = videoDetails['isPrivate']

        microformat = data['microformat']
        playerMicroformatRenderer = microformat['playerMicroformatRenderer']
        self.isFamilySafe = playerMicroformatRenderer['isFamilySafe']
        self.category = playerMicroformatRenderer['category']
        self.publishDate = playerMicroformatRenderer['publishDate']
        self.uploadDate = playerMicroformatRenderer['uploadDate']

        self.thumbnail = (playerMicroformatRenderer['thumbnail'])['thumbnails']

    def save_details(self, name="videoDetails", file_format="JSON", encoding="utf-8"):
        if file_format == "JSON":
            self._save_as_json(encoding, name)

    def _save_as_json(self, encoding, file):
        file += '.json'
        attr = {'videoID': self._ID,
                'title': self.title,
                'keywords': self.keywords,
                'channelId': self.channelId,
                'description': self.shortDescription,
                'author': self.author,
                'isPrivate': self.isPrivate,
                'isFamilySafe': self.isFamilySafe,
                'category': self.category,
                'publishDate': self.publishDate,
                'uploadDate': self.uploadDate}

        with open(file, 'w', encoding=encoding) as f:
            json.dump(attr, f, indent=4, ensure_ascii=False)
            f.close()

    def save_thumbnail(self, file='thumbnail'):
        thumbnail = next(iter(self.thumbnail))
        url = thumbnail['url']
        imagen = requests.get(url)
        extension = url.split('.')[-1]
        with open(file + '.' + extension, 'wb') as f:
            f.write(imagen.content)
            f.close()
