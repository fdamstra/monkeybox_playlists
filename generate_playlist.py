#! /usr/bin/env python3

import argparse
import json
import logging

from ytmusicapi import YTMusic

def get_songs(ytmusic, title=None, artist=None, album=None):
    searchstring = " ".join(filter(None, [ artist, album, title ]))

    results = ytmusic.search(searchstring, filter='songs')
    return [ r for r in results if r['resultType'] == 'song'  ]

def find_playlist(ytmusic, title):
    logging.debug(f'Searching for playlist "{title}"')
    playlists = ytmusic.get_library_playlists()
    for pl in playlists:
        if pl['title'] == title:
            logging.info(f'Found existing playlist {pl["title"]}')
            return pl['playlistId']
    logging.info(f'No playlist {title} found. Creating.')
    return None

def clear_playlist(ytmusic, playlistId):
    logging.debug(f'Loading playlist "{playlistId}"')
    pl = ytmusic.get_playlist(playlistId=playlistId, limit=0)
    if len(pl['tracks']) > 0:
        logging.info(f'Clearing playlist of {len(pl["tracks"])} tracks.')
        status = ytmusic.remove_playlist_items(playlistId=playlistId, videos=pl['tracks'])
        return True
    logging.info(f'No tracks to remove.')
    return True

#def pick_best(request, results):
# Thought about using fuzzy string matching. Still might. Look at https://www.datacamp.com/community/tutorials/fuzzy-string-python
#    # use fuzzy logic to pick the best match
#    logging.debug('Using fuzzy logic to pick best match.')
#    if request.get('videoId'):
#        logging.debug('VideoID specified
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('playlist', help='The playlist file to process.')
    parser.add_argument('--debug', help='Verbose output.', action='store_true')
    args = parser.parse_args()

    if(args.debug):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('Level set to debug')
    else:
        logging.basicConfig(level=logging.INFO)
        logging.debug('Level set to info')
    
    logging.debug('Initializing ytmusic...')
    ytmusic = YTMusic('headers_auth.json')

    logging.info(f'Opening playlist {args.playlist}')
    with open(args.playlist, 'r') as playlist:
        playlist = json.load(playlist)

    playlistId = find_playlist(ytmusic, title=playlist['title'])
    if playlistId is None:
        playlistId = ytmusic.create_playlist(
            title=playlist['title'], 
            description=playlist['description'],
            privacy_status=playlist['privacy_status']
        )
        logging.info(f'Created playlist with id "{playlistId}"')
    else:
        status = ytmusic.edit_playlist(
            playlistId=playlistId,
            title=playlist['title'], 
            description=playlist['description'],
            privacyStatus=playlist['privacy_status']
        )
        logging.info(f'Updated playlist. Status={status}')

    clear_playlist(ytmusic, playlistId)

    for s in playlist['songs']:
        if s.get('playlistId') is not None:
            status = ytmusic.add_playlist_items(
                playlistId=playlistId,
                videoIds = [ ],
                source_playlist=s["playlistId"]
            )
            logging.info(f'Added playlist "{s["playlistId"]}" ("{s["title"]}"); Status={status}')
            continue
        if s.get('videoId') is not None:
            logging.info(f'Adding "{s["title"]} by "{s["artist"]}" directly by video ID ("{s["videoId"]}")')
            results = [ { 'title': s["title"], 'artists': [ { 'name': s["artist"] } ], 'videoId': s["videoId"], 'album': { 'name': "n/a" } } ]
        else:
          logging.debug(f'Searching for "{s["title"]}" by "{s["artist"]}"')
          results = list(get_songs(ytmusic, title=s['title'], artist=s['artist']))

        for r in results:
            if r["album"] is None:
                r["album"] = { 'name': '' }
            try:
                logging.debug(f'  Found candidate: {r["title"]} - {r["artists"][0]["name"]} - {r.get("album", {}).get("name")} ({r["videoId"]})')
            except:
                logging.error(f'  FATAL: Could not output: {json.dumps(r)}')
        if len(results) > 0:
            status = ytmusic.add_playlist_items(
                playlistId=playlistId,
                videoIds=[ results[0]['videoId'] ],
                duplicates=False
            )
            #logging.info(f'Added "{results[0]["title"]} - {results[0]["artists"][0]["name"]} - {results[0]["album"]["name"]} ({results[0]["videoId"]})" to playlist. status={status}')
            logging.info(f'Match: "{s["title"]}" by "{s["artist"]}" ==> "{results[0]["title"]} - {results[0]["artists"][0]["name"]} - {results[0].get("album", {}).get("name")} ({results[0]["videoId"]})" to playlist. status={status}')
        else:
            logging.warning(f'NOT FOUND!!!! No results found for "{s["title"]}" by "{s["artist"]}"')

    logging.info(f'Done. URL is https://music.youtube.com/playlist?list={playlistId}')
