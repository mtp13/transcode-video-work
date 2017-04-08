#!/usr/bin/env perl

use 5.010;
use open qw(:std :utf8);
use Text::Unidecode;
use autodie;

# Anchorman The Legend of Ron Burgundy (2004) - The Movie Database (TMDb)
#
# use applescript to get the TMDb webpage title for the movie that
# was found and convert accented characters into non accented
# characters
# get rid of all punctation except for ()!- space
# strip off the end of the title " - The Movie Database (TMDb)"
# remove all line feeds and empty lines from the $QUEUE file
# write the new $dvd_title to the file
# and copy it to the clipboard

my $QUEUE = '/Volumes/Media Disk/transcode-video-work/queue.txt';
my $NEW_QUEUE = '/Volumes/Media Disk/transcode-video-work/new_queue.txt';
my $DVD_FOLDER = '/Volumes/Media Disk/DVD Backups/';

$script = <<'END_SCRIPT';
tell application "Safari"
	set theTitle to the name of the front document
end tell
END_SCRIPT

my $dvd_title = unidecode(`osascript -e '$script'`);
$dvd_title =~ s/[^a-zA-Z0-9()! \-]//g;
$dvd_title =~ s/ -- The Movie Database.*//;
# print "$dvd_title\n";

open(QUEUE, "< $QUEUE");
open(NEW_QUEUE, "> $NEW_QUEUE");
while (<QUEUE>) {
    print NEW_QUEUE if (/\S/);
}
print NEW_QUEUE "$DVD_FOLDER" . "$dvd_title" . ".mkv\n";
close(QUEUE);
close(NEW_QUEUE);
rename($NEW_QUEUE, $QUEUE);

no warnings;
open(CLIPBOARD, '| pbcopy');
print CLIPBOARD "$dvd_title";
