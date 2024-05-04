# 1. Youtube Music to iTunes (Apple Music) converter
<a id="markdown-youtube-music-to-itunes-apple-music-converter" name="youtube-music-to-itunes-apple-music-converter"></a>

Script for MacOS that downloads and adds newly added Youtube Music songs to iTunes.



Proud ![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-raw/prawwtocol/ytm-to-itunes) enjoyer;     ![GitHub License](https://img.shields.io/github/license/prawwtocol/ytm-to-itunes)


<img src="https://www.pngall.com/wp-content/uploads/4/MacOS-PNG-Clipart.png" height="40px" /> : <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.mm.bing.net%2Fth%3Fid%3DOIP._N-T1X-ZVBFMrcY7RUYcBwHaHa%26pid%3DApi&f=1&ipt=47590b5edde2fb01b0d551d8b8c125724509e19f032a0b521a2a15268fce712a&ipo=images" height="40px" /> ➡️ <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.pngarts.com%2Ffiles%2F8%2FApple-Music-Logo-PNG-Photo.png&f=1&nofb=1&ipt=9b2025a02ec0b35cf0a14817f52add29ee4985302def60d30f667fb015b5d05d&ipo=images" alt="Apple Music Logo PNG Photo | PNG Arts" height="40px" />



Youtube Music:

- has better recommendations
- has more content

Apple Music:

- better library organinzation
- files always offline
- free download of songs on Android



I want to listen and discover songs on Youtube Music, and periodically sync any new songs to my iTunes library; which is why I wrote this script.


<!-- TOC -->

- [1. Youtube Music to iTunes Apple Music converter](#1-youtube-music-to-itunes-apple-music-converter)
    - [1.1. Running form releases](#11-running-form-releases)
        - [1.1.1. Prerequisites:](#111-prerequisites)
        - [1.1.2. Running:](#112-running)
    - [1.2. Running from source](#12-running-from-source)
        - [1.2.1. Prerequisites:](#121-prerequisites)
        - [1.2.2. Running:](#122-running)
    - [1.3. Building executables:](#13-building-executables)
    - [1.4. Similar projects:](#14-similar-projects)

<!-- /TOC -->


## 1.1. Running form releases
<a id="markdown-running-form-releases" name="running-form-releases"></a>


### 1.1.1. Prerequisites:
<a id="markdown-prerequisites%3A" name="prerequisites%3A"></a>

1. Ensure you have enough space on drive for your songs

### 1.1.2. Running:
<a id="markdown-running%3A" name="running%3A"></a>


1. Download binaries from [latest release](https://github.com/prawwtocol/ytm-to-itunes/releases/latest)
2. `chmod +x main ytm_oauth`
    1. If you don't have `oauth.json`, login to Apple Music by running: `ytm_oauth` in Terminal
        1. Follow instructions in browser, after that return to Terminal and press [ENTER]
    2. If you do have `oauth.json`, run `main`. Specify full or relative path to `oauth.json`
3. Sit back and relax




## 1.2. Running from source
<a id="markdown-running-from-source" name="running-from-source"></a>


### 1.2.1. Prerequisites:
<a id="markdown-prerequisites%3A" name="prerequisites%3A"></a>

1. [`python 3.12.1`](https://github.com/prawwtocol/ytm-to-itunes/blob/main/Pipfile#L18) or any of your liking
2. <img src="https://www.pngall.com/wp-content/uploads/4/MacOS-PNG-Clipart.png" height="40px" /> MacOS with applescript support
3. [`pipenv`](https://pipenv.pypa.io/en/latest/) python package
4. Ensure you have enough space on drive for your songs

### 1.2.2. Running:
<a id="markdown-running%3A" name="running%3A"></a>


1. `git clone https://github.com/prawwtocol/ytm-to-itunes.git`
2. `cd ytm-to-itunes`
1. `pipenv install`
4. `ytmusicapi oauth`
    - Authenticate with Youtube Music, then return to Terminal and press [ENTER]
5. Run with `python main.py` when you need to sync. Specify full or relative path to `oauth.json`
3. Sit back and relax


## 1.3. Building executables:
<a id="markdown-building-executables%3A" name="building-executables%3A"></a>

```sh
pyinstaller main.spec
pyinstaller ytm_oauth.spec
```


## 1.4. Similar projects:
<a id="markdown-similar-projects%3A" name="similar-projects%3A"></a>

- https://soundiiz.com/ – freemium, doesn't add to local storage

- https://alternativeto.net/software/soundiiz/ – also freemium alternatives

