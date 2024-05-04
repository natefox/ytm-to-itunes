"""
This module provides functionality to download songs from YouTube Music
playlists and add them to iTunes playlists.

It uses the `ytmusicapi` to interact with YouTube Music and get playlist
information. The `yt_dlp` library is used to download the audio from YouTube
videos. The downloaded songs are then added to iTunes playlists using
AppleScript commands executed via the `subprocess` module.

This script is intended to be run as a standalone program. When run, it
iterates over all playlists in the user's YouTube Music library, downloads
all songs in those playlists, and adds them to corresponding playlists
in iTunes.
"""

import subprocess
import os
import logging
from tqdm import tqdm  # type: ignore

# https://ytmusicapi.readthedocs.io/en/stable/reference.html#ytmusicapi.YTMusic.get_library_playlists
from ytmusicapi import YTMusic  # type: ignore
import yt_dlp  # type: ignore
from util import create_dir_if_not_exist, create_file_if_not_exist
import datetime


# Set up logging
logging_level = logging.DEBUG

logging.basicConfig(level=logging_level)
logger = logging.getLogger(__name__)
logger.setLevel(logging_level)
# in order to not get 2 log messages:
# Set the logger to not propagate messages:
# logger.propagate = False.
# This will prevent the logger from sending messages up to the root logger
logger.propagate = False

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create a file handler
log_file = (
    "log" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".log"
)
handler = logging.FileHandler(log_file)
handler.setLevel(logging_level)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging_level)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


oauth_path = input("Please enter the path to your oauth.json file: ")
if not os.path.isfile(oauth_path):
    print("File does not exist. Please try again.")
else:
    ytmusic = YTMusic(oauth_path)
    # ytmusic = YTMusic("oauth.json")


# TODO add badges


def scpt_add_file_to_plst(file_path: str, playlist_name: str) -> str:
    """
    Adds a file to a playlist in the Music application.

    Args:
        file_path (str): The path of the file to be added.
        playlist_name (str): The name of the playlist to add the file to.

    Returns:
        str: An AppleScript command to add the file to the playlist.
    """
    return f"""
tell application "Music"
    set filePath to "{file_path}"
    set fileAlias to POSIX file filePath as alias
    add fileAlias to playlist "{playlist_name}"
end tell
"""


def itunes_add(playlist_name: str, file_path: str) -> None:
    """
    Add a file to an iTunes playlist.

    Args:
        playlist_name (str): The name of the playlist to add the file to.
        file_path (str): The path to the file to add to the playlist.
    """
    # TODO mypy
    logger.debug(
        "iTunes: Adding a song with path: %s to playlist: %s",
        file_path,
        playlist_name,
    )
    subprocess.call(
        ["osascript", "-e", scpt_add_file_to_plst(file_path, playlist_name)]
    )


def scpt_get_plst_id(playlist_name):
    """
    Returns an AppleScript command to get the ID of a playlist in the
    Music app.

    Parameters:
    - playlist_name (str): The name of the playlist.

    Returns:
    - str: An AppleScript command to get the ID of the specified playlist.
    """
    return f"""tell application "Music"
get id of playlist "{playlist_name}"
end tell"""


def itunes_get_plst_id(playlist_name):
    """
    Get the playlist ID for a given playlist name.

    Args:
        playlist_name (str): The name of the playlist to get the ID for.

    Returns:
        str: The playlist ID.
    """

    playlist_id = (
        subprocess.check_output(
            ["osascript", "-e", scpt_get_plst_id(playlist_name)]
        )
        .decode("utf-8")
        .strip()
    )
    logger.debug(
        "iTunes: got playlist id: %s from name: %s", playlist_id, playlist_name
    )
    return playlist_id


def scpt_new_plst(playlist_name):
    """
    Create a new user playlist in the Music application with the given name.

    Parameters:
    - playlist_name (str): The name of the playlist to create.

    Returns:
    - str: An AppleScript string that creates a new user playlist
    swith the specified name.
    """
    return f"""
tell application "Music"
    make new user playlist with properties {{name:"{playlist_name}"}}
end tell
"""


def itunes_new_plst(playlist_name):
    """
    Create a playlist in iTunes with the given name.

    Args:
        playlist_name (str): The name of the playlist to create.
    """
    logger.debug("iTunes: creating new playlist with name: %s", playlist_name)
    subprocess.call(["osascript", "-e", scpt_new_plst(playlist_name)])


def ytdlp_gen_config(dl_path):
    """
    Generate the configuration dictionary for youtube-dl.

    Args:
        dl_path (str): The path where the downloaded files will be saved.

    Returns:
        dict: The configuration dictionary for youtube-dl.

    """

    """
    https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#embedding-yt-dlp

    For a list of options available, have a look at yt_dlp/YoutubeDL.py or
    help(yt_dlp.YoutubeDL) in a Python shell. If you are already familiar
    with the CLI, you can use devscripts/cli_to_api.py to translate any
    CLI switches to YoutubeDL params.
    """
    return {
        "extract_flat": "discard_in_playlist",
        "final_ext": "m4a",
        "format": "bestaudio/best",
        "fragment_retries": 10,
        "ignoreerrors": True,
        "outtmpl": dl_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "nopostoverwrites": False,
                "preferredcodec": "m4a",
                "preferredquality": "5",
            },
            {
                "add_chapters": True,
                "add_infojson": "if_exists",
                "add_metadata": True,
                "key": "FFmpegMetadata",
            },
            {
                "key": "FFmpegConcat",
                "only_multi_video": True,
                "when": "playlist",
            },
        ],
        "retries": 10,
    }


def ytm_dl_song(url, ydl_opts):
    """
    Downloads a song from YouTube Music and returns the absolute path
    sof the downloaded track.

    Args:
        url (str): The URL of the YouTube Music song.
        ydl_opts (dict): The options to be passed to the YoutubeDL instance.

    Returns:
        str: The absolute path of the downloaded track.
    """
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        logger.debug("ytdlp: downloading song from url: %s", url)
        info = ydl.extract_info(url, download=False)
        # Download the video
        ydl.download([url])
        # Get the file path
        filepath_local = ydl.prepare_filename(info)
        filepath_local = filepath_local.replace(".webm", ".m4a")
        # Get the absolute path of the file
        return os.path.abspath(filepath_local)


def main():
    """
    Main function that performs the conversion of YouTube Music playlists
    to iTunes playlists.
    """

    ytm_all_plsts = ytmusic.get_library_playlists()
    for plst in tqdm(ytm_all_plsts):
        ytm_plst_name = plst["title"]
        ytm_plst_id = plst["playlistId"]
        logger.debug(
            "main: working with playlist: %s [%s]", ytm_plst_name, ytm_plst_id
        )

        ydl_opts = ytdlp_gen_config(
            f"./result/{ytm_plst_id}/%(title)s.%(ext)s"
        )

        try:
            # check if the playlist exists in apple music
            itunes_get_plst_id(ytm_plst_name)
            logger.debug("iTunes: playlist %s exists", ytm_plst_name)
        except subprocess.CalledProcessError:
            # if it doesn't exist, the applescirpt retuns an error
            # subprocess.CalledProcessError
            # then, create the playlist and still get it's id
            logger.debug(
                "iTunes: playlist %s didn't exist; attempting to create",
                ytm_plst_name,
            )
            itunes_new_plst(ytm_plst_name)

        pl_dir_path = f"./result/{ytm_plst_id}"
        create_dir_if_not_exist(pl_dir_path)

        dl_path = f"{pl_dir_path}/downloaded.txt"
        err_path = f"{pl_dir_path}/errored.txt"
        create_file_if_not_exist(dl_path)
        create_file_if_not_exist(err_path)

        tracks = ytmusic.get_playlist(ytm_plst_id, limit=None)["tracks"]

        logger.debug(
            "main: working with playlist tracks: there are %s of them",
            len(tracks),
        )

        # https://stackoverflow.com/questions/56381066/how-to-open-a-file-in-both-read-and-append-mode-at-the-same-time-in-one-variable
        # position in f is at beginning
        with (
            open(dl_path, "r+", encoding="utf-8") as df,
            open(err_path, "r+", encoding="utf-8") as ef,
        ):
            dl_text = df.read()
            err_text = ef.read()
            for track in tqdm(tracks):
                already_downloaded = False
                if not track["videoId"]:
                    # skip if empty track videoId
                    # TODO cron
                    # TODO windows port
                    logger.error(
                        "main: track [[[%s]]] has empty videoID", track
                    )
                    continue

                if track["videoId"] in dl_text:
                    logger.debug
                    (
                        "main: tracks: %s has beed downloaded and added before",
                        track["videoId"],
                    )
                    already_downloaded = True

                if not already_downloaded:
                    download_url = (
                        f'https://www.youtube.com/watch?v={track["videoId"]}'
                    )
                    try:
                        fp2 = ytm_dl_song(download_url, ydl_opts)
                        itunes_add(ytm_plst_name, fp2)
                        df.write(track["videoId"] + "\n")
                        logger.debug(
                            "main: logged track: %s as downloaded",
                            track["videoId"],
                        )
                    except Exception as e:
                        # AttributeError: 'NoneType' object has no
                        # attribute 'setdefault'
                        # ERROR: [youtube] _2I7utmtm0Q: Video unavailable.
                        # The uploader has not made this video available
                        # in your country
                        logger.error(e)
                        if track["videoId"] not in err_text:
                            ef.write(track["videoId"] + "\n")
                            logger.debug(
                                "main: logged track: %s as errored out",
                                track["videoId"],
                            )


if __name__ == "__main__":
    main()
