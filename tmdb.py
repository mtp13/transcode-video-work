#!/usr/bin/env python

# Anchorman The Legend of Ron Burgundy (2004) - The Movie Database (TMDb)
#
# use applescript to get the TMDb webpage title for the movie that
# was found and convert accented characters into non accented
# characters
# get rid of all punctation except for ()!- space
# strip off the end of the title " - The Movie Database (TMDb)"
# remove all blank lines from the QUEUE file
# write the new dvd_title to the file
# and copy it to the clipboard

from subprocess import Popen, PIPE
from unidecode import unidecode
import re
import fileinput


def run_this_ascript(ascript, args=[]):
    "Run the given AppleScript and return the standard output."
    p = Popen(['osascript', '-'] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(ascript)
    return stdout


def setClipboardData(data):
    p = Popen(['pbcopy'], stdin=PIPE)
    p.communicate(data)


QUEUE = '/Volumes/Media Disk/transcode-video-work/queue.txt'
DVD_FOLDER = '/Volumes/Media Disk/DVD Backups/'

ascript = """
tell application "Safari"
set theTitle to the name of the front document
end tell
"""
dvd_title = run_this_ascript(ascript)
dvd_title = unidecode(unicode(dvd_title, 'utf-8'))

dvd_title = re.sub('[^a-zA-Z0-9()! \-]', '', dvd_title)
dvd_title = re.sub(' -- .*', '', dvd_title)

for line in fileinput.input(QUEUE, inplace=1):
    if re.search('\S', line):
        print line.strip()
with open(QUEUE, 'a') as q:
    q.write(DVD_FOLDER + dvd_title + '.mkv\n')
print DVD_FOLDER + dvd_title + '.mkv'

setClipboardData(dvd_title)
