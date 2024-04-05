import re
import sys
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def make_filename_safe(title):
    # Remove any character that is not alphanumeric, a space, or a hyphen
    filename = re.sub(r'[^\w\s-]', '', title)
    # Replace spaces or consecutive hyphens with a single hyphen
    filename = re.sub(r'[-\s]+', '-', filename).strip()
    # Ensure the filename is not too long
    filename = filename[:200]
    return filename

def download_transcript(video_id):
    try:
        # Fetch the video object
        video = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        video_title = make_filename_safe(video.title)

        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = "\n".join([entry['text'] for entry in transcript])
        with open(f"{video_title}.txt", "w", encoding='utf-8') as text_file:
            text_file.write(transcript_text)
        print(f"Transcript for video '{video_title}' saved as '{video_title}.txt'")
    except TranscriptsDisabled:
        print("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        print("No transcript found for this video.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_id = sys.argv[1]
        download_transcript(video_id)
    else:
        print("Usage: python download_transcript.py [video_id]")
