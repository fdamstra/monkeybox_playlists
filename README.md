# Generates MonkeyBOX Playlists
Start by following the setup instructions:
```
pip3 install ytmusicapi
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
