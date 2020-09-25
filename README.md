* [Were there monkeys in the 80s](https://music.youtube.com/playlist?list=PL5O3j7EHU9drsNR_MQXBQYcGjOmykxQKE)
* [Cornelius the Liar Detective](https://music.youtube.com/playlist?list=PL5O3j7EHU9doVZBlkgxUDX224yDy15J53)

# Regenerating the Playlists

I completely overengineered this project. Not sure why.

Start by following the setup instructions:
```
pip3 install ytmusicapi
#pip3 install fuzzywuzzy # Unused, but may be needed in the future
python3
from ytmusicapi import YTMusic
YTMusic.setup(filepath=`headers_auth.json`)
# Paste in request headers from browser, everything starting with "accept: */*"
quit()
```

Then generate a playlist per json.

```
for i in playlist-*.json; do
  python3 generate_playlist.py $i
done
```

It may take a few minutes before your playlist will show up in your browser.
