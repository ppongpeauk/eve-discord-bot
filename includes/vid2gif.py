import os, subprocess, threading
import requests, random, string, filetype
from urllib.parse import urlparse
from ffprobe import FFProbe
from includes.s3 import upload_to_aws

temp_path = "temp"

async def random_string():
  string = ""
  for x in range(24):
    string += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) # merge arrays
  return string

async def main(**kwargs):
  # check if filetype is valid
  get_ft = filetype.guess(kwargs.get("url"))
  if get_ft.extension.startswith("video/"):

    file_name = os.path.basename(urlparse(kwargs.get("url")).path)
    name_base = os.path.splitext(file_name)
    file_request = requests.get(kwargs.get("url"), allow_redirects=True)
    file_path = os.path.join(temp_path, file_name)

    # write http contents to filesystem
    open(file_path, "wb").write(file_request.contents)

    # check video length
    probe = FFProbe(file_path)
    new_name = f"{kwargs.get('temp_name')}.gif"
    new_path = os.path.join(temp_path, new_name)
    if probe.streams[0].duration <= 30: # if the video is less than 30 seconds long
      subprocess.run([
        "ffmpeg", "-i",
        file_path, new_path
      ])
      if os.path.getsize(new_path)/1000000 > 8:
        uploaded = upload_to_aws(new_path, "restrafes", new_name)
        return {2, f"https://restrafes.s3.amazonaws.com/{new_name}"}
      else:
        return {1, new_path}
  else:
    return {False}

async def run(**kwargs):
  temp_name = await random_string()
  loop = asyncio.get_event_loop()
  process = await loop.run_in_executor(None, lambda: main(data=kwargs))
