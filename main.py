from flask import Flask, request, send_file
from pytube import YouTube
from io import BytesIO
import instaloader
import requests
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)

@app.route('/youtube/download_audio', methods=['GET', 'POST'])
def download_audio():
    url = request.args['url']
    yt = YouTube(url)
    audio = yt.streams.filter(only_audio=True).first()
    filename = f"{yt.title}.mp3"
    audio.download(filename=filename)
    return send_file(filename, as_attachment=True)


@app.route('/youtube/download_video', methods=['GET', 'POST'])
def download_video():
    url = request.args['url']
    res = request.args['res']
    yt = YouTube(url)
    print(yt.streams.all)
    video = yt.streams.filter(res=f"{res}p").first()
    filename = f"{yt.title}.mp4"    
    video_data = BytesIO()
    video.stream_to_buffer(video_data)
    video_data.seek(0)
    return send_file(video_data, download_name=filename, as_attachment=True)


@app.route('/youtube/details', methods=['GET', 'POST'])
def details():
    
    url = request.args['url']
    yt = YouTube(url)
    min,sec = divmod(yt.length,60)
    video_details = {
        'title': yt.title,
        'thumbnail_url': yt.thumbnail_url,
        'length': f"{min}:{sec}",
        'views': yt.views,
        'rating': yt.rating,
        'author': yt.author,
        'publish_date': yt.publish_date
    }
    return video_details

@app.route("/instagram/download")
def download_Insta():
    url = request.args['url']
    L = instaloader.Instaloader()
    l = url.split("/")
    if "p" in l or "tv" in l or "reel" in l:
        shortcode = l[4]
    else:
        return {"error":"Invalid url"}
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    if post.is_video:
        video_url = post.video_url
        video_file = BytesIO(requests.get(video_url).content)
        return send_file(video_file, download_name=f"{post.profile}.mp4", as_attachment=True)
    else:
        img_url = post._asdict()["display_url"]
        file = BytesIO(requests.get(img_url).content)
        return send_file(file, download_name=f"{post.profile}.jpg", as_attachment=True)


@app.route("/instagram/details")
def details_Insta():
    url = request.args['url']
    L = instaloader.Instaloader()
    l = url.split("/")
    if "p" in l or "tv" in l or "reel" in l:
        shortcode = l[4]
    else:
        return {"error":"Invalid url"}
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    return post._asdict()

if __name__ == '__main__':
    app.run(debug=True,host ='0.0.0.0',port=5000)