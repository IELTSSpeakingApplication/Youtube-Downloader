import os
import glob
import argparse
import yt_dlp as youtube_dl
from pydub import AudioSegment

ap = argparse.ArgumentParser()

ap.add_argument("-u", "--url", required=True, help="youtube link url")
ap.add_argument("-s", "--start", required=True, default="00:00", help="start duration")
ap.add_argument("-e", "--end", required=True, default="00:10", help="start duration")
ap.add_argument("-v", "--version", action="version", version="%(prog)s 1.0.0")

args = vars(ap.parse_args())

def download_audio(url):
    ydl_opts = {
                    "format": "bestaudio/best",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }],
                }
    
    print("Starting downloading ... ")

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def newest_mp3_filename():
    list_of_mp3s = glob.glob("./*.mp3")

    print("Success downloading ... ")
    
    return max(list_of_mp3s, key = os.path.getctime)

def get_video_time_in_ms(video_timestamp):
    vt_split = video_timestamp.split(":")

    if (len(vt_split) == 3):
        hours = int(vt_split[0]) * 60 * 60 * 1000
        minutes = int(vt_split[1]) * 60 * 1000
        seconds = int(vt_split[2]) * 1000
    elif (len(vt_split) == 2):
        hours = 0
        minutes = int(vt_split[0]) * 60 * 1000
        seconds = int(vt_split[1]) * 1000
    else:
        hours = 0
        minutes = 0
        seconds = int(vt_split[0]) * 1000
        
    return hours + minutes + seconds

def get_trimmed(mp3_filename, initial, final = ""):
    if (not mp3_filename):
        raise Exception("No MP3 found in local directory.")
    
    sound = AudioSegment.from_mp3(mp3_filename)
    t0 = get_video_time_in_ms(initial)

    print(f"\nBeginning trimming process for file ", mp3_filename, ".")
    print("Starting from ", initial, "...")

    if (len(final) > 0):
        print("...up to ", final, ".\n")
        t1 = get_video_time_in_ms(final)
        return sound[t0:t1]
    
    return sound[t0:]

def delete_original_file(filename):
    os.remove(filename)

def main():
    download_audio(args["url"])
    filename = newest_mp3_filename()
    trimmed_file = get_trimmed(filename, args["start"], args["end"])
    trimmed_filename = "".join([filename.split(".mp3")[0], "-TRIM.mp3"])
    trimmed_filename = os.path.join("data", trimmed_filename.split("/")[1])
    print("Process concluded successfully. Saving trimmed file as ", trimmed_filename)
    trimmed_file.export(trimmed_filename, format="mp3")
    delete_original_file(filename)

if __name__ == "__main__":
    main()

print("Youtube link {}".format(args["url"]))
print("Start time {}".format(args["start"]))
print("End time {}".format(args["end"]))