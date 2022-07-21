from YoutubeVideo import VideoDetails

if __name__ == '__main__':
    video = VideoDetails('oT6uMfHLNwg')
    video.save_details(file_format="JSON")
    video.save_thumbnail()
