# Click on these to Listen! MonkeyBOX Playlists:

* [Were there monkeys in the 80s](https://music.youtube.com/playlist?list=PL5O3j7EHU9drsNR_MQXBQYcGjOmykxQKE)
* [Cornelius the Liar Detective](https://music.youtube.com/playlist?list=PL5O3j7EHU9doVZBlkgxUDX224yDy15J53) [(notes)](playlist-cornelius.notes.md)
* [And Good Taste Prevailed...](https://music.youtube.com/playlist?list=PL5O3j7EHU9dos_K9hnsbccAFxir0Mto4f)

* Scraps
  * [Disk 1](https://music.youtube.com/playlist?list=PL5O3j7EHU9drX2Z3lkCyF13uWuYx5me-q) [(notes)](playlist-scraps.notes.md)
  * [Disk 2](https://music.youtube.com/playlist?list=PL5O3j7EHU9dpgflMh288Y6PJvYO5Fh8b4)
* Five Bucks a Throw (missing)
* [

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
