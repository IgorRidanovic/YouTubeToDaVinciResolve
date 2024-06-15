#! /usr/bin/env python

'''
This script uses youtube-dl to download a user supplied list of YouTube videos to
a local storage and import them into the the current bin in DaVinci Resolve.

Place the script in:

macOS: /Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Deliver
Windows: %PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Deliver

Invoke from the Resolve Script dropdown menu. Basic reporting is available in the
Resolve console.

© 2024 Igor Riđanović, www.metafide.com
'''


import youtube_dl


def download_videos(youtubeUrl, downloadPath):
    # youtube-dl settings
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{downloadPath}/%(title)s.%(ext)s',
        'quiet': True,  # Resolve internal script will fail in verbose mode due to lack of flush.
    }

    # Iterate the list of video URLs and download
    for yturl in youtubeUrl:

        # Print updates to the console
        print(f'Downloading: {yturl}')

        # Download the video from this YouTube URL
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yturl])    # youtubeUrl has to be a list

        # Import downloaded video to the current bin. To avoid using progress_hooks
        # and complicating youtube-dl we'll just attempt to import all the files
        # Each time a new file is available. Resolve will ignore any existing bin clips.
        mediaPool.ImportMedia(downloadPath)


if __name__=='__main__':

    # Make DaVinci Resolve instances
    projectManager = resolve.GetProjectManager()
    currentProject = projectManager.GetCurrentProject()
    mediaPool      = currentProject.GetMediaPool()


    # Prompt user for the file containing the YouTube video URLs> One URL per line.
    youtubeUrl =  fusion.RequestFile()
    with open(youtubeUrl, 'r', encoding='utf-8') as f:
        youtubeUrl = [line.strip() for line in f]
    

    # Ask user where to download the YouTube files
    downloadPath = fusion.RequestDir()

    # Download the videos
    download_videos(youtubeUrl, downloadPath)