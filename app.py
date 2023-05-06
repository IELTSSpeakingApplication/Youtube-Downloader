import os
import glob
import shutil
import argparse
import yt_dlp as youtube_dl
from pydub import AudioSegment
from mutagen.mp3 import MP3

ap = argparse.ArgumentParser()

subparser = ap.add_subparsers(dest="command")
ap.add_argument("-v", "--version", action="version", version="%(prog)s 2.0.0")

download = subparser.add_parser("download")
delete = subparser.add_parser("delete")
trim = subparser.add_parser("trim")

download.add_argument("-u", "--url", type=str, required=True, help="youtube link url (example: https://youtu.be/YtIVUR0BckQ)")

delete.add_argument("-u", "--url", type=str, required=True, help="sufix youtube link url (example: YtIVUR0BckQ) if have `-` delete char")

trim.add_argument("-u", "--url", type=str, required=True, help="sufix youtube link url (example: YtIVUR0BckQ) if have `-` delete char")
trim.add_argument("-s", "--start", required=True, default="00:00", help="start duration")
trim.add_argument("-e", "--end", required=True, default="00:10", help="start duration")

args = ap.parse_args()

def download_audio(url):
    ydl_opts = {
                    "format": "bestaudio/best",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }],
                }
    
    print(f"Starting downloading ...\n")

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

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
    t1 = get_video_time_in_ms(final)
    audio = MP3(mp3_filename)
    
    if (t1<=audio.info.length*1000 or t0<=audio.info.length*1000):
        print(f"\nBeginning trimming process for file", mp3_filename,f".\n")
        print("Starting from", initial, "...")

        if (t1<=audio.info.length*1000):
            print("...up to", final,".\n")
            return sound[t0:t1]
        else:
            print("...up to end of MP3.\n")
            return sound[t0:]
    else:
        raise Exception("Length MP3 is to short.")

def delete_file(filename):
    os.remove(filename)

def main():
    print(f"\n======= YOUTUBE DOWNLOADER =======\n")

    if args.command == "download":
        print("-> Download Youtube Video to MP3")
        print("Downloading", args.url, f"...\n")

        url = args.url.split("/")[-1]

        download_audio(args.url)

        print(f"\nSuccess Downloading", args.url, "!")

        mp3s = glob.glob('./*.mp3')
        destination = os.path.join("data", mp3s[0])

        print(f"\n-> Moving MP3 File")
        print("Move", mp3s[0], "to /data folder ...")

        shutil.copy(mp3s[0], destination)

        list_mp3s = glob.glob('./data/*.mp3')

        if any(url in s for s in list_mp3s):
            print(f"\nSuccess Copying file", mp3s[0], "!")
        else:
            print(f"\nFailedCopying file", mp3s[0], "!")
        
        print(f"\n-> Deleteing MP3 File from Root")
        print("Delete file", mp3s[0], "from Root ...")

        delete_file(mp3s[0])

        print(f"\nSuccess Deleteing", mp3s[0], "!")

    elif args.command == "delete":
        print("-> Delete MP3 File")

        list_mp3s = glob.glob('./data/*.mp3')

        if any(args.url in s for s in list_mp3s):
            file = [s for s in list_mp3s if args.url in s]
            print("Delete file", args.url, "from Data ...")

            delete_file(file[0])

            print(f"\nSuccess Deleteing", args.url, "!")
        else:
            print(f"\nSufix File", args.url, "not Found !")

    elif args.command == "trim":
        print("-> Trim MP3 File")

        list_mp3s = glob.glob('./data/*.mp3')

        if any(args.url in s for s in list_mp3s):
            file = [s for s in list_mp3s if args.url in s]
            print("Trim file", args.url, "from", args.start, "to", args.end, "...")

            trimmed_file = get_trimmed(file[0], args.start, args.end)
            trimmed_filename = "".join([file[0].split(".mp3")[0], args.start, "to", args.end, "-TRIM.mp3"])
            trimmed_filename = os.path.join("dataset", trimmed_filename.split("/")[-1])
            print(f"Process concluded successfully.\nSaving trimmed file as ", trimmed_filename)
            trimmed_file.export(trimmed_filename, format="mp3")

            print(f"\nSuccess Trimming", args.url, "!")
        else:
            print(f"\nSufix File", args.url, "not Found !")
            
    else:
        print(f"Oppss, Command didn't found!")

    print(f"\n==================================\n")

if __name__ == "__main__":
    main()