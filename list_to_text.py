# list_to_text.py
from playlist_nabber import get_video_ids_from_playlist
from text_getter import download_transcript

def download_playlist_transcripts(playlist_url):
    video_ids = get_video_ids_from_playlist(playlist_url)
    for video_id in video_ids:
        download_transcript(video_id)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        playlist_url = sys.argv[1]
        download_playlist_transcripts(playlist_url)
    else:
        print("Usage: python list_to_text.py 'playlist_url'")
