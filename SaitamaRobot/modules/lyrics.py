import re

import lyricsgenius

from SaitamaRobot import *
from SaitamaRobot import GENIUS, dispatcher
from SaitamaRobot.events import register





@register(pattern=r"^/lyrics(?:\s|$)([\s\S]*)")
async def lyrics(event):    # sourcery no-metrics
    "To fetch song lyrics"
    if event.fwd_from:
        return
    if GENIUS is None:
        return await event.reply(
            "`Set genius access token in heroku vars for functioning of this command`",
        )
    match = event.pattern_match.group(1)
    songno = re.findall(r"-n\d+", match)
    listview = re.findall(r"-l", match)
    try:
        songno = songno[0]
        songno = songno.replace("-n", "")
        match = match.replace(f"-n{songno}", "")
        songno = int(songno)
    except IndexError:
        songno = 1
    if songno < 1 or songno > 10:
        return await event.reply(
            "`song number must be in between 1 to 10 use -l flag to query results`",
        )
    match = match.replace("-l", "")
    listview = bool(listview)
    query = match.strip()
    genius = lyricsgenius.Genius(GENIUS, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)
    genius.verbose = False
    if "-" in query:
        args = query.split("-", 1)
        artist = args[0].strip(" ")
        song = args[1].strip(" ")
        webevent = await event.reply(
            f"`Searching lyrics for {artist} - {song}...`"
        )
        try:
            songs = genius.search_song(song, artist)
        except TypeError:
            songs = None
        if songs is None:
            return await webevent.edit(f"Song **{artist} - {song}** not found!")
        result = f"**Search query**: \n`{artist} - {song}`\n\n```{songs.lyrics}```"
    else:
        webevent = await event.reply(f"`Searching lyrics for {query}...`")
        response = genius.search_songs(query)
        msg = f"**The songs found for the given query:** `{query}`\n\n"
        if len(response["hits"]) == 0:
            return await webevent.edit(
                f"**I can't find lyrics for the given query: **`{query}`"
            )
        for i, an in enumerate(response["hits"], start=1):
            msg += f"{i}. `{an['result']['title']}`\n"
        if listview:
            result = msg
        else:
            result = f"**The song found for the given query:** `{query}`\n\n"
            if songno > len(response["hits"]):
                return await webevent.edit(
                    f"**Invalid song selection for the query select proper number**\n{msg}",
                )
            songtitle = response["hits"][songno - 1]["result"]["title"]
            result += f"`{genius.search_song(songtitle).lyrics}`"
    await webevent.edit(result)
