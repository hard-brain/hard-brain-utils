import json


def parse_json():
  """A script that processes a raw IIDX game data json file to a simplified version for use with Hard Brain"""
  song_data = {"songs": {}}

  with open("iidx.json", "r", encoding="utf-8") as file:
    iidx_json = json.load(file)
    for song_raw in iidx_json:
      song_id = str(song_raw['entry_id']).zfill(5)
      alt_titles = []
      title = str(song_raw['title']).strip()
      title_ascii = song_raw["title_ascii"]
      if title_ascii != song_raw['title']:
        alt_titles.append(title_ascii)
      song = {
          "song_id": str(song_id),
          "filename": f"{song_id}.mp3",
          "title": title,
          "alt_titles": alt_titles,
          "genre": song_raw['genre'],
          "artist": song_raw['artist']
        }
      song_data["songs"][str(song_id)] = song

  with open("iidx_output.json", "w") as out:
    json.dump(song_data, out)


if __name__ == "__main__":
  parse_json()
