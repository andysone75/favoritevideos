import youtube_dl, os, ast

PATH = 'YoutubePodcasts/static/podcasts/'
PATH2 = '/static/podcasts/'
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': PATH + '/%(id)s.%(ext)s'
}
dl = youtube_dl.YoutubeDL({'outtmpl': PATH + '/%(id)s.%(ext)s'})

def download(link):
    try:
        r = dl.extract_info(link)
    except youtube_dl_utils.DownloadError:
        return False
    with open(f"{PATH}{r['id']}", 'w', encoding='UTF-8', errors='replace') as f:
        f.write(str(r))
    return True

def download_info(link):
    with dl:
        result = dl.extract_info(
            link, download=False)
    if 'entries' in result:
        video = result['entries'][0]
    else:
        video = result
    info = {
        'title': video["title"],
        'uploader': video["uploader"],
        'uploader_url' : video["uploader_url"],
        'thumbnail': video["thumbnails"][4]['url']}
    return info

def get():
    audios = {}
    for i in os.walk(PATH):
        for filename in i[2]:
            if '.' in filename and not filename.endswith('.part'):
                try:
                    audios[f'{PATH2}{filename}'] = ast.literal_eval(open(f'{PATH}{filename.split(".")[0]}', 'r', encoding='UTF-8').read())
                except FileNotFoundError:
                    pass
    return audios
