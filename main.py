import subprocess
import os
from ytmusicapi import YTMusic

import yt_dlp
import os
import os
ytmusic = YTMusic("oauth.json")


def add_to_itunes(playlist_name, file_path):
    """
    Add a file to an iTunes playlist.

    Args:
        playlist_name (str): The name of the playlist to add the file to.
        file_path (str): The path to the file to add to the playlist.
    """

    # Get the playlist ID
    # playlist_id = get_playlist_id(playlist_name)

    script = f"""
tell application "Music"
    set filePath to "{file_path}"
    set fileAlias to POSIX file filePath as alias
    add fileAlias to playlist "{playlist_name}"
end tell
"""

    # Add the file to the playlist
    subprocess.call(["osascript", "-e", script])


def get_playlist_id(playlist_name):
    """
    Get the playlist ID for a given playlist name.

    Args:
        playlist_name (str): The name of the playlist to get the ID for.

    Returns:
        str: The playlist ID.
    """

    # Get the playlist ID
    playlist_id = subprocess.check_output(
        ["osascript", "-e", f"tell application \"Music\"\nget id of playlist \"{playlist_name}\"\nend tell"]).decode("utf-8").strip()

    return playlist_id


def create_itunes_playlist(playlist_name):
    """
    Create a playlist in iTunes with the given name.

    Args:
        playlist_name (str): The name of the playlist to create.
    """

    # Create the playlist

    applescript = f"""
tell application "Music"
    make new user playlist with properties {{name:"{playlist_name}"}}
end tell
"""

    # process = subprocess.Popen(
    #     ['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # stdout, stderr = process.communicate(applescript.encode())
    subprocess.call(
        ["osascript", "-e", applescript])


if __name__ == "__main__":
    # playlist_name = 'My Playlist'
    # file_path = 'path/to/file.mp3'

    # Add the file to the playlistor

    # add any new playlist that has not been added yet
    plsts = (ytmusic.get_library_playlists())
    for pl in plsts[1:2]:
        ytm_pl_name = pl['title']
        ytm_pl_id = pl['playlistId']
        print(ytm_pl_name, ":::::::")
        try:
            xx = get_playlist_id(ytm_pl_name)
        except subprocess.CalledProcessError:
            create_itunes_playlist(ytm_pl_name)
            xx = get_playlist_id(ytm_pl_name)
            # xx = 'created!!'
        print(xx, 'asljhfdaslkf')

        # TODO for every playlist add their songs
        # https://ytmusicapi.readthedocs.io/en/stable/reference.html#ytmusicapi.YTMusic.get_library_playlists
        res = ytmusic.get_playlist(ytm_pl_id)
        print('working with playlist ', ytm_pl_name, ' yt id: ', ytm_pl_id)
        # print(res['tracks'])
        for x in res["tracks"][:]:
            dir2 = f'./result/{ytm_pl_id}'
            if not os.path.exists(dir2):
                os.mkdir(dir2)

            # os.makedirs()

            with open(f'./result/{ytm_pl_id}/!downloaded.txt', 'r+', encoding='utf-8') as f:
                already_downloaded = False
                for l in f:
                    if x['videoId'] in l:
                        already_downloaded = True
                        break

                if not already_downloaded:
                    # URL of the video you want to download
                    URL = f'https://www.youtube.com/watch?v={x["videoId"]}'

                    # Options for yt-dlp
                    ydl_opts2 = {'extract_flat': 'discard_in_playlist',
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

                    ydl_opts = {
                        'format': 'm4a/bestaudio/best',  # Choose the best quality format
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',  # Extract audio using ffmpeg
                            'preferredcodec': 'm4a',
                        }],
                        'outtmpl': f'./result/{ytm_pl_id}/%(title)s.%(ext)s',
                        'overwrites': True,
                    }

                    # Download the video
                    try:
                        with yt_dlp.YoutubeDL(ydl_opts2) as ydl:
                            # info = ydl.download(URL)
                            # Extract information
                            info = ydl.extract_info(URL, download=False)
                            fppp_local = ydl.prepare_filename(
                                info)  # Get the file path
                            ydl.download([URL])  # Download the video
                            fppp_local = fppp_local.replace(".webm", ".m4a")
                            # Get the absolute path of the file
                            file_path2 = os.path.abspath(fppp_local)

                            add_to_itunes(ytm_pl_name, file_path2)
                            # add_to_itunes(ytm_pl_name, file_path)
                            # add_to_itunes(ytm_pl_name, file_path)
                            # Delete the file at file_path
                        print()

                        # write to file the id of the video just downloaded
                        f.write(x['videoId'] + '\n')
                    except Exception:
                        # AttributeError: 'NoneType' object has no attribute 'setdefault'
                        # ERROR: [youtube] _2I7utmtm0Q: Video unavailable. The uploader has not made this video available in your country
                        with open(f'./result/{ytm_pl_id}/!errored.txt', 'r+', encoding='utf-8') as f2:
                            f2.write(x['videoId'] + '\n')

                        pass
    # add_to_itunes(playlist_name, file_path)
