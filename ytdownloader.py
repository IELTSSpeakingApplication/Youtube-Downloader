import argparse

ap = argparse.ArgumentParser()

ap.add_argument("-u", "--url", required=True, help="youtube link url")
ap.add_argument("-s", "--start", required=True, default="00:00", help="start duration")
ap.add_argument("-e", "--end", required=True, default="00:10", help="start duration")
ap.add_argument("-v", "--version", action="version", version="%(prog)s 1.0.0")

args = vars(ap.parse_args())

print("Youtube link {}".format(args["url"]))
print("Start time {}".format(args["start"]))
print("End time {}".format(args["end"]))