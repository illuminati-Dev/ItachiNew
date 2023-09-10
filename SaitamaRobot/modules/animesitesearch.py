import html

import bs4
import requests
from SaitamaRobot import dispatcher
from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,
                      Update)
from telegram.ext import CallbackContext, run_async

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

info_btn = "More Information"
kayo_btn = "Kayo 🏴‍☠️"
animespot_btn = "Animespot ☠️"
animetm_btn = "Animetm ☠️"
prequel_btn = "⬅️ Prequel"
sequel_btn = "Sequel ➡️"
close_btn = "Close ❌"

def shorten(description, info='anilist.co'):
    msg = ""
    if len(description) > 700:
        description = description[:500] + '....'
        msg += f"\n*Description*:\n_{description}_[Read More]({info})"
    else:
        msg += f"\n*Description*:\n_{description}_"
    return msg

def t(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)} Days, " if days else "")
        + (f"{str(hours)} Hours, " if hours else "")
        + (f"{str(minutes)} Minutes, " if minutes else "")
        + (f"{str(seconds)} Seconds, " if seconds else "")
        + (f"{str(milliseconds)} ms, " if milliseconds else "")
    )

    return tmp[:-2]

def site_search(update: Update, context: CallbackContext, site: str):
    message = update.effective_message
    args = message.text.strip().split(" ", 1)
    more_results = True

    try:
        search_query = args[1]
    except IndexError:
        message.reply_text("Give something to search")
        return

    if site == "anidl":
        search_url = f"https://anidl.org/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "post-title"})

        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>anidl</code>: \n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>anidl</code>"
                more_results = False
                break

            post_link = entry.a['href']
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"

    elif site == "indi":
        search_url = f"https://indianime.com/?s={search_query}"
        html_text = requests.get(search_url , headers=headers).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "post-title"})

        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>indianime</code>: \n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>indianime</code>"
                more_results = False
                break

            post_link = entry.a['href']
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"

    elif site == "kaizoku":
        search_url = f"https://animekaizoku.com/?s={search_query}"
        html_text = requests.get(search_url , headers=headers).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        if search_result := soup.find_all("h2", {'class': "post-title"}):
            result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>: \n"
            for entry in search_result:
                post_link = "https://animekaizoku.com/" + entry.a['href']
                post_name = html.escape(entry.text)
                result += f"• <a href='{post_link}'>{post_name}</a>\n"
        else:
            more_results = False
            result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>"

    elif site == "kayo":
        search_url = f"https://kayoanime.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "post-title"})

        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>KayoAnime</code>: \n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>KayoAnime</code>"
                more_results = False
                break

            post_link = entry.a['href']
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"

    buttons = [[InlineKeyboardButton("See all results", url=search_url)]]

    if more_results:
        message.reply_text(
            result,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True)
    else:
        message.reply_text(
            result, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
           

def kayo(update: Update, context: CallbackContext):
    site_search(update, context, "kayo")
    
def kaizoku(update: Update, context: CallbackContext):
    site_search(update, context, "kaizoku")

def indi(update: Update, context: CallbackContext):
    site_search(update, context, "indi")

def anidl(update: Update, context: CallbackContext):
    site_search(update, context, "anidl")


__help__ = """
 ◆/anime - Fetches info on single anime (includes
          buttons to look up for prequels and
          sequels)
 ◆/anilist - Fetches info on multiple possible
            animes related to query
 ◆/character - Fetches info on multiple possible
              characters related to query
 ◆/manga - Fetches info on multiple possible
          mangas related to query
 ◆/airing - Fetches info on airing data for anime
 ◆/browse - get popular, trending or upcoming
           animes
 ◆/whatanime - search any anime media powered by
              tracemoepy
 ◆/watchorder - Fetches watch order for anime
               series
 ◆/fillers - To get list of anime fillers
 ◆/top - to retrieve top animes for a genre or
         tags
 ◆/gettags - Get list of available Tags
 ◆/getgenres - Get list of available Genres
 
               **Anilist Account Help🈚 :**
               
 ◆/auth - Fetches info on how to authorize
          anilist account                
 ◆/flex - Fetches anilist info of an authorised
          user
 ◆/user - Fetches anilist info as per query
 ◆/schedule - Fetches scheduled animes
 ◆/logout - removes authorization
 ◆/favourites - Get Anilist favourites
 ◆/me or /activity - Get Anilist recent activity
  
     **NSFW lock , Anime News and aniCommand disabling☮️ :**

 ◆/anisettings - To toggle nsfw lock and airing
                 notifications in groups
 ◆/anidisable - To disable a command in group
 ◆/anienable - To enable a command in group
 ◆/anidisabled - To list disabled commands in a group
 
         **Anime  Sites Help♐ :**
         
 ◆/kayo*:* Find anime from animekayo website.
 ◆/kaizoku*:* Find anime from kaizoku website.
 ◆/indi*:* Find anime from indianime.com 
 ◆/anidl*:* search an anime on anidl.org
"""
    
__mod_name__ = "Anime ♓"
KAYO_SEARCH_HANDLER = DisableAbleCommandHandler("kayo", kayo, run_async=True)
KAIZOKU_SEARCH_HANDLER = DisableAbleCommandHandler("kaizoku", kaizoku, run_async=True)
INDI_SEARCH_HANDLER = DisableAbleCommandHandler("indi", indi, run_async=True)
ANIDL_SEARCH_HANDLER = DisableAbleCommandHandler("anidl", anidl, run_async=True)

dispatcher.add_handler(KAYO_SEARCH_HANDLER)
dispatcher.add_handler(KAIZOKU_SEARCH_HANDLER)
dispatcher.add_handler(INDI_SEARCH_HANDLER)
dispatcher.add_handler(ANIDL_SEARCH_HANDLER)

__handlers__ = [ KAYO_SEARCH_HANDLER,
     KAIZOKU_SEARCH_HANDLER,  INDI_SEARCH_HANDLER,  ANIDL_SEARCH_HANDLER  ]
