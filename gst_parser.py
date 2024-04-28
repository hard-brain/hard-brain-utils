import re
import subprocess
from pathlib import Path

PATH = Path.cwd().as_posix()
gst_dir = Path(f"{PATH}/iidx-gst-all").resolve()
out_dir = Path(f"{PATH}/iidx-gst-mp3").resolve()
files = set(gst_dir.iterdir())

def gst_transcode():
  """transcode output wavs to mp3 and rename to song ID"""
  transcoded_count = 0
  pattern = re.compile(r"_SPN")

  if not gst_dir.exists():
    raise FileNotFoundError("No gst directory found")

  if not out_dir.exists():
    print(f"creating output directory at '{out_dir.as_posix()}'")
    out_dir.mkdir()

  for file in list(files):
    if "SPN" in file.name:
      target_file = Path(gst_dir, file.name)
      output_filename = f"{pattern.split(file.stem)[0]}.mp3"

      ffmpeg_filters = "silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse"
      ffmpeg_commands = [
        "ffmpeg", 
        "-y", 
        "-i", 
        f"{target_file.as_posix()}", 
        "-af", 
        ffmpeg_filters, 
        f"{output_filename}"
      ]

      print(f"transcoding song {file}")
      subprocess.run(ffmpeg_commands, cwd=str(out_dir))
      transcoded_count += 1

  print(f"finished, transcoded {transcoded_count} songs")

if __name__ == "__main__":
  gst_transcode()
