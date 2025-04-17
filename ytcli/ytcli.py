#!/usr/bin/env python3
"""
ytcli.py - A unified Linux CLI tool to interact with YouTube using the YouTube Data API,
yt-dlp library, and local media players. Supports search, download, metadata info,
playback in VLC/mpv, playlist/history management, and API key configuration.

Requirements:
    pip install yt-dlp google-api-python-client

Setup:
    - Ensure your Python environment includes the 'ssl' module (standard in most installs).
    - You can set your YouTube Data API v3 key via environment variable or using `setapi`:
        export YOUTUBE_API_KEY="YOUR_API_KEY"
        or
        ytcli.py setapi YOUR_API_KEY

Usage:
    ytcli.py setapi <api_key>                Save API key to config file
    ytcli.py search <query> [-n N]           Search YouTube and record to history
    ytcli.py info <video_id>                 Show metadata for a YouTube video
    ytcli.py download <video_id> [-f FMT]    Download a video (using yt-dlp API)
    ytcli.py play <video_id>                 Play a video in VLC or mpv
    ytcli.py playlist create <name>          Create a new playlist
    ytcli.py playlist add <name> <id>        Add video ID to a playlist
    ytcli.py history                         Show command history
    ytcli.py test                            Run built-in tests

Configuration files:
    CONFIG_FILE: ~/.ytcli_config             (JSON storing your API key)
    HISTORY_FILE: ~/.ytcli_history           (one JSON entry per line)
    PLAYLIST_FILE: ~/.ytcli_playlists        (JSON mapping of playlist to video IDs)
"""
import os
import sys
import argparse
import json
import subprocess
from datetime import datetime

# Attempt to import yt-dlp with SSL check
try:
    from yt_dlp import YoutubeDL
except ModuleNotFoundError as e:
    if 'ssl' in str(e):
        print("Error: This environment does not support 'ssl', required by yt-dlp.")
        sys.exit(1)
    else:
        raise

# Google API imports
from googleapiclient.discovery import build

# Config paths
CONFIG_FILE = os.path.expanduser('~/.ytcli_config')
HISTORY_FILE = os.path.expanduser('~/.ytcli_history')
PLAYLIST_FILE = os.path.expanduser('~/.ytcli_playlists')

# Load API key: environment first, then config file override
API_KEY = os.getenv('YOUTUBE_API_KEY') or ""
if os.path.exists(CONFIG_FILE):
    try:
        cfg = json.load(open(CONFIG_FILE))
        if cfg.get('api_key'):
            API_KEY = cfg['api_key']
    except json.JSONDecodeError:
        pass

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Helpers

def record_history(entry: dict):
    entry['timestamp'] = datetime.utcnow().isoformat()
    with open(HISTORY_FILE, 'a') as f:
        f.write(json.dumps(entry) + "\n")


def load_playlists() -> dict:
    if os.path.exists(PLAYLIST_FILE):
        try:
            return json.load(open(PLAYLIST_FILE))
        except json.JSONDecodeError:
            return {}
    return {}


def save_playlists(plists: dict):
    with open(PLAYLIST_FILE, 'w') as f:
        json.dump(plists, f, indent=2)


def save_config(cfg: dict):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(cfg, f, indent=2)

# Commands

def set_api_key(key: str):
    save_config({'api_key': key})
    print(f"API key saved to {CONFIG_FILE}")
    record_history({'action': 'setapi'})


def search_videos(query, max_results=5):
    if not API_KEY:
        print("Error: API key not configured. Use 'setapi' or export YOUTUBE_API_KEY.")
        sys.exit(1)
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    resp = youtube.search().list(q=query, part='id,snippet', maxResults=max_results).execute()
    results = []
    for item in resp.get('items', []):
        if item['id']['kind'] == 'youtube#video':
            results.append({
                'title': item['snippet']['title'],
                'id': item['id']['videoId'],
                'channel': item['snippet']['channelTitle'],
                'publishedAt': item['snippet']['publishedAt']
            })
    for i, v in enumerate(results, 1):
        print(f"{i}. {v['title']} ({v['id']}) by {v['channel']} @ {v['publishedAt']}")
    record_history({'action': 'search', 'query': query, 'results': len(results)})
    return results


def video_info(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {'skip_download': True, 'quiet': True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    for key in ['title', 'uploader', 'upload_date', 'view_count', 'duration', 'like_count']:
        print(f"{key.replace('_',' ').title()}: {info.get(key)}")
    record_history({'action': 'info', 'id': video_id})


def download_video(video_id, fmt=None):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {}
    if fmt:
        ydl_opts['format'] = f'bestvideo[ext={fmt}]+bestaudio/best[ext={fmt}]'
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    record_history({'action': 'download', 'id': video_id, 'format': fmt})


def play_video(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        subprocess.Popen(["vlc", url])
    except FileNotFoundError:
        subprocess.Popen(["mpv", url])
    record_history({'action': 'play', 'id': video_id})


def create_playlist(name):
    plists = load_playlists()
    if name in plists:
        print(f"Playlist '{name}' already exists.")
    else:
        plists[name] = []
        save_playlists(plists)
        print(f"Created playlist '{name}'.")
    record_history({'action': 'playlist_create', 'playlist': name})


def add_to_playlist(name, video_id):
    plists = load_playlists()
    if name not in plists:
        print(f"Playlist '{name}' does not exist.")
        sys.exit(1)
    plists[name].append(video_id)
    save_playlists(plists)
    print(f"Added video {video_id} to playlist '{name}'.")
    record_history({'action': 'playlist_add', 'playlist': name, 'id': video_id})


def show_history():
    if not os.path.exists(HISTORY_FILE):
        print("No history yet.")
        return
    for line in open(HISTORY_FILE):
        try:
            entry = json.loads(line)
            print(entry)
        except json.JSONDecodeError:
            continue

# Built-in tests

def run_tests():
    import tempfile, unittest
    class PlaylistTest(unittest.TestCase):
        def setUp(self):
            self.pfile = tempfile.NamedTemporaryFile(delete=False).name
            self.cfile = tempfile.NamedTemporaryFile(delete=False).name
            self.hfile = tempfile.NamedTemporaryFile(delete=False).name
            global PLAYLIST_FILE, CONFIG_FILE, HISTORY_FILE
            self.orig_pl = PLAYLIST_FILE
            self.orig_cf = CONFIG_FILE
            self.orig_hf = HISTORY_FILE
            PLAYLIST_FILE = self.pfile
            CONFIG_FILE = self.cfile
            HISTORY_FILE = self.hfile
        def tearDown(self):
            os.unlink(self.pfile)
            os.unlink(self.cfile)
            os.unlink(self.hfile)
            global PLAYLIST_FILE, CONFIG_FILE, HISTORY_FILE
            PLAYLIST_FILE = self.orig_pl
            CONFIG_FILE = self.orig_cf
            HISTORY_FILE = self.orig_hf
        def test_create_and_add(self):
            create_playlist('test')
            pl = load_playlists()
            self.assertIn('test', pl)
            self.assertEqual(pl['test'], [])
            add_to_playlist('test', 'xyz')
            pl2 = load_playlists()
            self.assertEqual(pl2['test'], ['xyz'])
        def test_setapi_and_load(self):
            set_api_key('ABC123')
            cfg = json.load(open(CONFIG_FILE))
            self.assertEqual(cfg.get('api_key'), 'ABC123')
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(PlaylistTest)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)

# Argument parsing

def main():
    parser = argparse.ArgumentParser(prog='ytcli')
    sub = parser.add_subparsers(dest='cmd', required=True)

    # setapi
    setapi = sub.add_parser('setapi')
    setapi.add_argument('key', help='YouTube API key')
    # search
    search = sub.add_parser('search')
    search.add_argument('query', help='Search query')
    search.add_argument('-n', '--max-results', dest='max_results', type=int, default=5,
                        help='Number of search results to return')
    # info
    info = sub.add_parser('info')
    info.add_argument('video_id', help='YouTube video ID')
    # download
    dl = sub.add_parser('download')
    dl.add_argument('video_id', help='YouTube video ID')
    dl.add_argument('-f', '--format', dest='format', help='Desired video format ext')
    # play
    play = sub.add_parser('play')
    play.add_argument('video_id', help='YouTube video ID')
    # playlist
    pl = sub.add_parser('playlist')
    pl_sub = pl.add_subparsers(dest='pl_cmd', required=True)
    create = pl_sub.add_parser('create')
    create.add_argument('name', help='Playlist name')
    add = pl_sub.add_parser('add')
    add.add_argument('name', help='Playlist name')
    add.add_argument('video_id', help='YouTube video ID to add')
    # history
    sub.add_parser('history')
    # test
    sub.add_parser('test')

    args = parser.parse_args()
    if args.cmd == 'setapi':
        set_api_key(args.key)
    elif args.cmd == 'search':
        search_videos(args.query, args.max_results)
    elif args.cmd == 'info':
        video_info(args.video_id)
    elif args.cmd == 'download':
        download_video(args.video_id, args.format)
    elif args.cmd == 'play':
        play_video(args.video_id)
    elif args.cmd == 'playlist':
        if args.pl_cmd == 'create':
            create_playlist(args.name)
        elif args.pl_cmd == 'add':
            add_to_playlist(args.name, args.video_id)
    elif args.cmd == 'history':
        show_history()
    elif args.cmd == 'test':
        run_tests()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
