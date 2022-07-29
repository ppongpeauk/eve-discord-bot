# eve
# 6/24/2021
import discord
import json, base64
import os, requests, asyncio
import globals
from dotenv import load_dotenv # for getting the spotify token
load_dotenv()

async def check_activity(client=None):
  spotify_tokens = {
    "access_token": "",
    "refresh_token": ""
  }
  with open("satoken.txt", "r") as f:
    spotify_tokens["access_token"] = f.read()
  with open("stoken.txt", "r") as f:
    spotify_tokens["refresh_token"] = f.read()
  while True:
    try:
      if client and client.is_ready():
        def get_token():
          nonlocal spotify_tokens
          x = (os.getenv('SPOTIFY_CLIENT') + ':' + os.getenv('SPOTIFY_SECRET'))
          response = requests.post("https://accounts.spotify.com/api/token",
            data={
              "grant_type": "authorization_code",
              "code": spotify_tokens["refresh_token"],
              "redirect_uri": "https://127.0.0.1/callback"
            },
            headers={
              "Authorization": f"Basic {base64.b64encode(x.encode()).decode()}"
            })
          to_json = response.json()
          print(to_json)
          spotify_tokens = to_json
          with open("satoken.txt", "w") as f:
            f.write(to_json["access_token"])
          with open("stoken.txt", "w") as f:
            f.write(to_json["refresh_token"])

        if spotify_tokens["access_token"] != "":
          get_token()
          with open("satoken.txt", "r") as f:
            spotify_tokens["access_token"] = f.read()
          with open("stoken.txt", "r") as f:
            spotify_tokens["refresh_token"] = f.read()
        headers = {
          "Accept": "application/json",
          "Content-Type": "application/json; charset=utf-8",
          "Authorization": f"Bearer {spotify_tokens['access_token']}"
        }
        response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)
        if response.status_code == 200:
          to_json = response.json()
          if to_json['is_playing'] == True:
            activity = discord.Activity(type=discord.ActivityType.listening, name=f"{to_json['item']['name']} by {to_json['item']['artists'][0]['name']}")
            await client.change_presence(activity=activity)
          else: # if not playing
            get_cached_activity = globals.activity_object.get_cache()
            await client.change_presence(activity=get_cached_activity)
        else:
          get_token()
    except Exception as e:
      pass
    await asyncio.sleep(5)

