import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url", required=True,
	help="youtube link url")
args = vars(ap.parse_args())

print("Youtube link {}".format(args["url"]))