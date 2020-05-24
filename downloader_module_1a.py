import requests
def downloader(song_requested,link,dest):  # Download the data using @param link & saves to @param dest & @param song_requested is raw song name
    print("Downloading...")
    data = requests.get(link).content
    with open(dest+'/'+song_requested+".mp3", 'wb') as f:
        f.write(data)
    print("{} downloaded to {}".format(song_requested, dest))

#@param song_request is direct user inserted songname
#@param bitrate_available is type list for availble download options as webelement
#@param dest is string destination to download the song
def qualitySelector(song,bitrate_available,dest):
    if len(bitrate_available)>=2:
        print("""=====Quantity Selector======
        Press 1 for 128Kbps
        Press 2 for 320Kbps
        """)
        selected = int(input())
        if selected==1:
            downloader(song,bitrate_available[0].get_attribute('href'),dest)
        elif selected == 2:
            downloader(song,bitrate_available[1].get_attribute('href'),dest)
        else:
            print("No such option")
            qualitySelector(song,bitrate_available,dest)
    else:
        downloader(song,bitrate_available[0].get_attribute('href'),dest)