from telethon import TelegramClient, sync, events
import telebot
import requests
import spotipy
import spotipy.util as util
import random
from spotipy.oauth2 import SpotifyClientCredentials
from yandex_music import Client as YMClient
import re


class TGCredentials:
   ''' Данные от телеграма '''
   api_id = 1111111
   api_hash = 'api_hash'
   session_name = 'session_name'


class SpotifyCredentials:
   ''' Данные от spotify '''
   client_id = 'chat_id'
   client_secret = 'client_secret'


class MusikReverse(object):
   def __init__(self, spotify_client_id, spotify_client_secret):
      self.spotify_service = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret))
      self.ym_service = YMClient()

   def reverse(self, link):
      if 'open.spotify.com' in link:
         track_info = self.spotify_service.track(link)
         search_result = self.ym_service.search(track_info['artists'][0]['name'] + track_info['name'])
         ym_link = 'https://music.yandex.ru/track/' + str(search_result['best']['result']['id'])

         return ym_link

      elif 'music.yandex.ru' in link:
         id_song = re.findall(r'track/(\d+)', link)[0]
         track_info = self.ym_service.tracks(id_song)
         search_result = self.spotify_service.search(track_info[0]['title'] + ' ' + track_info[0]['artists'][0]['name'] + ' ' + track_info[0]['albums'][0]['title'])
         spotify_link = search_result['tracks']['items'][0]['external_urls']['spotify']

         return spotify_link


tg_client = TelegramClient(
   TGCredentials.session_name, 
   TGCredentials.api_id, 
   TGCredentials.api_hash)

musik_reverse = MusikReverse(
   SpotifyCredentials.client_id, 
   SpotifyCredentials.client_secret
)


@tg_client.on(events.NewMessage())
async def normal_handler(event):
   if 'open.spotify.com' in event.message.to_dict()['message'] or 'music.yandex.ru' in event.message.to_dict()['message']:
      reverse_link = musik_reverse.reverse(event.message.to_dict()['message'])

      await event.message.reply(reverse_link)

tg_client.start()
tg_client.run_until_disconnected()