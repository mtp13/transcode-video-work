#!/usr/bin/env bash
export LANG=en_US.UTF-8

# Anchorman The Legend of Ron Burgundy (2004) - The Movie Database (TMDb)
#
# paste the TMDb webpage title for the movie that was found
# convert accented characters into non accented characters (iconv)
# get rid of all punctation except for ()!- space
# strip off the end of the title " - The Movie Database (TMDb)"
# copy the result back to the clipboard

echo -n $(pbpaste | iconv -f UTF-8 -t ASCII//TRANSLIT |	sed 's/[^a-zA-Z0-9()! \-]//g' | sed 's/ \- The Movie Database (TMDb).*$//') | pbcopy
