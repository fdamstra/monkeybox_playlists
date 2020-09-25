#! /usr/bin/env python3

import json

from ytmusicapi import YTMusic

def get_songs(ytmusic, title=None, artist=None, album=None):
    searchstring = " ".join(filter(None, [ artist, album, title ]))

    results = ytmusic.search(searchstring, filter='songs')
    return [ r for r in results if r['resultType'] == 'song'  ]

def find_playlist(ytmusic, title):
    playlists = ytmusic.get_library_playlists()
    for pl in playlists:
        if pl['title'] == title:
            print(f'Found existing playlist {pl["title"]}')
            return pl['playlistId']
    print(f'No playlist {pl["title"]} found. Creating.')
    return None

def clear_playlist(ytmusic, playlistId):
    pl = ytmusic.get_playlist(playlistId=playlistId, limit=0)
    #tracklist = []
    #for t in pl['tracks']:
    #    print(json.dumps(t, indent=2))
    if len(pl['tracks']) > 0:
        print(f'Clearing playlist of {len(pl["tracks"])} tracks.')
        status = ytmusic.remove_playlist_items(playlistId=playlistId, videos=pl['tracks'])
        return True
    print(f'No tracks to remove.')
    return True

if __name__ == "__main__":

    ytmusic = YTMusic('headers_auth.json')
    with open('playlist.json', 'r') as playlist:
        playlist = json.load(playlist)

    playlistId = find_playlist(ytmusic, title=playlist['title'])
    if playlistId is None:
        playlistId = ytmusic.create_playlist(
            title=playlist['title'], 
            description=playlist['description'],
            privacy_status=playlist['privacy_status']
        )
        print(f'Created playlist with id {playlistId}')
    else:
        status = ytmusic.edit_playlist(
            playlistId=playlistId,
            title=playlist['title'], 
            description=playlist['description'],
            privacyStatus=playlist['privacy_status']
        )
        print(f'Updated playlist. Status={status}')

    clear_playlist(ytmusic, playlistId)

    for s in playlist['songs']:
        results = get_songs(ytmusic, title=s['title'], artist=s['artist'])
        print(f'Searching for "{s["title"]}" by {s["artist"]}"')
        for r in results:
            print(f'  Found candidate: {r["title"]} - {r["artists"][0]["name"]} - {r["album"]["name"]} ({r["videoId"]})')
        if len(r) > 0:
            status = ytmusic.add_playlist_items(
                playlistId=playlistId,
                videoIds=[ results[0]['videoId'] ],
                duplicates=False
            )
            print(f'Added first candiates. status={status}')

#playlistId = ytmusic.create_playlist("test", "test description")
#search_results = ytmusic.search("Oasis Wonderwall")
#ytmusic.add_playlist_items(playlistId, [search_results[0]['videoId']])

