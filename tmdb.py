#!/usr/bin/env python
"Get the DVD title from Safari and save to the queue file."
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

import re
import fileinput
from subprocess import Popen, PIPE
from unidecode import unidecode


def run_this_ascript(ascript, args=None):
    "Run the given AppleScript and return the standard output."
    args = args or []
    pipe = Popen(['osascript', '-'] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = pipe.communicate(ascript)
    return stdout


def set_clipboard_data(data):
    "Copy the data to the system clipboard."
    pipe = Popen(['pbcopy'], stdin=PIPE)
    pipe.communicate(data)


QUEUE = '/Volumes/Media Disk/transcode-video-work/queue.txt'
DVD_FOLDER = '/Volumes/Media Disk/DVD Backups/'

ASCRIPT = """
tell application "Safari"
set theTitle to the name of the front document
end tell
"""
DVD_TITLE = run_this_ascript(ASCRIPT)
DVD_TITLE = unidecode(unicode(DVD_TITLE, 'utf-8'))

DVD_TITLE = re.sub(r'[^a-zA-Z0-9()! \-]', '', DVD_TITLE)
DVD_TITLE = re.sub(r' -- .*', '', DVD_TITLE)

for line in fileinput.input(QUEUE, inplace=1):
    if re.search(r'\S', line):
        print line.strip()
with open(QUEUE, 'a') as q:
    q.write(DVD_FOLDER + DVD_TITLE + '.mkv\n')
print DVD_FOLDER + DVD_TITLE + '.mkv'

set_clipboard_data(DVD_TITLE)
