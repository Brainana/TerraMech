import glob
import os

for f in glob.glob("lawn*.jpg"):
	os.remove(f)
