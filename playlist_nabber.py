from pytube import Playlist

def get_video_ids_from_playlist(playlist_url):
    try:
        playlist = Playlist(playlist_url)
        # This forces the script to fetch the videos in the playlist
        playlist._video_regex = None
        return [video.video_id for video in playlist.videos]
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        playlist_url = sys.argv[1]
        video_ids = get_video_ids_from_playlist(playlist_url)
        print("Video IDs:", video_ids)
    else:
        print("Usage: python playlist_nabber.py 'playlist_url'")
