import yt_dlp
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

links = [
    "https://www.youtube.com/watch?v=AAAAAAAAAAA",
    "https://www.youtube.com/watch?v=BBBBBBBBBBB",
    "https://www.youtube.com/watch?v=CCCCCCCCCCC"
]

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
    'no_warnings': True,
}

def download_video(url):
    for attempt in range(1, 5):
        try:
            print(f"Downloading (Attempt {attempt}): {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"✅ Downloaded: {url}")
            return None
        except Exception as e:
            print(f"❌ Failed attempt {attempt} for {url}: {e}")
            time.sleep(2)
    print(f"❌ Failed after 4 attempts: {url}")
    return url

failed_links = []
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(download_video, url): url for url in links}
    for future in as_completed(futures):
        result = future.result()
        if result:
            failed_links.append(result)

print("\nFailed links:")
for i in failed_links:
    print(i)
    
print("\nAll downloads completed.")