import argparse

ap = argparse.ArgumentParser()

subparser = ap.add_subparsers(dest="command")
ap.add_argument("-v", "--version", action="version", version="%(prog)s 2.0.0")

download = subparser.add_parser("download")
delete = subparser.add_parser("delete")
trim = subparser.add_parser("trim")

download.add_argument("-u", "--url", type=str, required=True, help="youtube link url (example: YtIVUR0BckQ)")

delete.add_argument("-u", "--url", type=str, required=True, help="youtube link url (example: YtIVUR0BckQ)")

trim.add_argument("-u", "--url", type=str, required=True, help="youtube link url (example: YtIVUR0BckQ)")
trim.add_argument("-s", "--start", required=True, default="00:00", help="start duration")
trim.add_argument("-e", "--end", required=True, default="00:10", help="start duration")

args = ap.parse_args()

def main():
    print(f"\n======= YOUTUBE DOWNLOADER =======\n")

    if args.command == "download":
        print("Download Url", args.url)
    elif args.command == "delete":
        print("Url", args.url)
    elif args.command == "trim":
        print("Url", args.url)
        print("Start", args.start)
        print("End", args.end)
    else:
        print(f"Oppss, Command didn't found!")

    print(f"\n==================================\n")

if __name__ == "__main__":
    main()