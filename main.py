import subprocess
import os
from ytmusicapi import YTMusic
import yt_dlp
import config
import time
from tqdm import tqdm

ytmusic = YTMusic("oauth.json")


def add_to_itunes(playlist_name, file_path):
    """
    Add a file to an iTunes playlist.

    Args:
        playlist_name (str): The name of the playlist to add the file to.
        file_path (str): The path to the file to add to the playlist.
    """

    script = f"""
tell application "Music"
    set filePath to "{file_path}"
    set fileAlias to POSIX file filePath as alias
    add fileAlias to playlist "{playlist_name}"
end tell
"""
    subprocess.call(["osascript", "-e", script])


def get_playlist_id(playlist_name):
    """
    Get the playlist ID for a given playlist name.

    Args:
        playlist_name (str): The name of the playlist to get the ID for.

    Returns:
        str: The playlist ID.
    """
    script = f"tell application \"Music\"\nget id of playlist \"{
        playlist_name}\"\nend tell"
    playlist_id = subprocess.check_output(
        ["osascript", "-e", script]).decode("utf-8").strip()
    return playlist_id


def download_track(ydl, download_url):
    """
    returns: absolute path of downloaded track
    """
    info = ydl.extract_info(download_url, download=False)

    # Download the video
    ydl.download([download_url])

    # Get the file path
    filepath_local = ydl.prepare_filename(info)
    filepath_local = filepath_local.replace(".webm", ".m4a")
    # Get the absolute path of the file
    return os.path.abspath(filepath_local)


def download_yt_song(track, download_url, ytm_pl_id, f, f2, actually_download_flag=True):
    ydl_opts = {'extract_flat': 'discard_in_playlist',
                'final_ext': 'm4a',
                'format': 'bestaudio/best',
                'fragment_retries': 10,
                'ignoreerrors': True,
                'outtmpl': f'./result/{ytm_pl_id}/%(title)s.%(ext)s',
                'postprocessors': [{'key': 'FFmpegExtractAudio',
                                    'nopostoverwrites': False,
                                    'preferredcodec': 'm4a',
                                    'preferredquality': '5'},
                                   {'add_chapters': True,
                                    'add_infojson': 'if_exists',
                                    'add_metadata': True,
                                    'key': 'FFmpegMetadata'},
                                   {'key': 'FFmpegConcat',
                                    'only_multi_video': True,
                                    'when': 'playlist'}],
                'retries': 10}

    try:
        if actually_download_flag:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                file_path2 = download_track(ydl, download_url)
                add_to_itunes(ytm_pl_name, file_path2)

            # add newlines for clarity
            print()
            print()

        # write to file the id of the video just downloaded
        f.write(track['videoId'] + '\n')
    except Exception:
        # AttributeError: 'NoneType' object has no attribute 'setdefault'
        # ERROR: [youtube] _2I7utmtm0Q: Video unavailable. The uploader has not made this video available in your country
        # TODO FileNotFoundError: [Errno 2] No such file or directory: './result/PLjuQ2jeykzJUTv3j59UegOAp6kHXfeZyk/!errored.txt'

        f2.write(track['videoId'] + '\n')


def create_itunes_playlist(playlist_name):
    """
    Create a playlist in iTunes with the given name.

    Args:
        playlist_name (str): The name of the playlist to create.
    """
    script = f"""
tell application "Music"
    make new user playlist with properties {{name:"{playlist_name}"}}
end tell
"""
    subprocess.call(
        ["osascript", "-e", script])


if __name__ == "__main__":
    # Add the file to the playlist
    # playlist[0] is Liked Tracks
    for idx, playlist in tqdm(enumerate(ytmusic.get_library_playlists()[0:])):
        ytm_pl_name = playlist['title']
        ytm_pl_id = playlist['playlistId']
        print(f'Doing playlist with name: {ytm_pl_name}')

        try:
            # check if the playlist exists
            apl_pl_id = get_playlist_id(ytm_pl_name)
        except subprocess.CalledProcessError:
            # if it doesn't exist, the applescirpt retuns an error
            # subprocess.CalledProcessError
            # then, create the playlist and still get it's id
            create_itunes_playlist(ytm_pl_name)

            # Wait for 1 second
            time.sleep(1)

            apl_pl_id = get_playlist_id(ytm_pl_name)

        # TODO for every playlist add their songs
        # https://ytmusicapi.readthedocs.io/en/stable/reference.html#ytmusicapi.YTMusic.get_library_playlists
        ytm_pl_current = ytmusic.get_playlist(ytm_pl_id, limit=None)

        pl_dir_path = f'./result/{ytm_pl_id}'
        if not os.path.exists(pl_dir_path):
            os.mkdir(pl_dir_path)
        dl_path = f'{pl_dir_path}/downloaded.txt'
        if os.path.exists(dl_path):
            pass
        else:
            with open(dl_path, "w") as f:
                pass

        if idx == 0:
            tracks = ytmusic.get_liked_songs(limit=None)["tracks"]
        else:
            tracks = ytm_pl_current["tracks"]
        # TODO error doesnt read this

        # https://stackoverflow.com/questions/56381066/how-to-open-a-file-in-both-read-and-append-mode-at-the-same-time-in-one-variable
        # position in f is at beginning
        with open(dl_path, 'r+', encoding='utf-8') as f:

            with open(f'{pl_dir_path}/errored.txt', 'a+',
                      encoding='utf-8') as f2:
                all_text = f.read()
                for track in tqdm(tracks):
                    already_downloaded = False
                    if not track['videoId']:
                        # skip if empty track videoId
                        # TODO logging
                        # TODO cron
                        # TODO windows port
                        continue

                    if track['videoId'] in all_text:
                        already_downloaded = True
                        # break

                    if not already_downloaded:
                        download_url = f'https://www.youtube.com/watch?v={
                            track["videoId"]}'
                        download_yt_song(
                            track, download_url, ytm_pl_id, f, f2, actually_download_flag=True)
