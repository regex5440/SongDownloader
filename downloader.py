nfo="""
    Downloader
    Author: Harsh
    version: 1.3 LAST UPDATED: 25/May/2020 4:37AM
"""
if __name__ == "__main__":
    import selenium.webdriver as driver
    import re
    import requests
    import downloader_module_1a as tools
    from time import sleep
    import os
    print("""***********DOWNLOADER**********
    \t\tpowred by Downloadming.se""")
    print("Song Availablity depends upon the website")
    song_requested = input("Song Name: ")
    if song_requested == "":
        print("No SONG")
        quit()
    browser=""
    if not os.path.exists("C:/bin"):
        os.mkdir("C:/bin")
    #DEVELOPERS OPTIONS
    if not input("Press Y/N (Optional) for visual process (Chrome Installed):\t")== ('Y' or 'y'):
        browser=driver.PhantomJS("drivers/phantomjs-2.1.1-windows/bin/phantomjs.exe")
    else:
        browser = driver.Chrome("drivers/chromedriver.exe")

    link = "http://www.downloadming.se"  # DEFAULT DOWNLOADING SITE: DOWNLOADMING
        
    def getDestination():    
        destination = input("Download Destination(Optional)use '/': ")
        if re.match(r"^([A-V]|[a-v]){1,1}(\:\/)(.){0,}",destination):
            print("Preparing to Downloading...")
            return str(destination)
        elif destination=="":
            return str("C:/bin")
        else:
            print('LOCATION NOT FOUND!')
            getDestination()
    try:
            # INITIALIZING THE BROWSER
        browser.get(link)
        browser.implicitly_wait(5)
        print("Connected to website successfully")


        browser.find_element_by_xpath(
            "//input[@placeholder='Search here..']").send_keys(song_requested)
        print("Fetching website data...")
        browser.find_element_by_xpath(
            "//div[@class='promagnifier']/div[@class='innericon']").click()
        print("Looking your results...")
        search_result = browser.find_elements_by_xpath('//a[@rel="bookmark"]')
        if len(search_result) < 1:
            print("NO SONG FOUND")
            quit()
        print(len(search_result), "result(s) found")

        search_result_links = list()  # Fetching links from web elements
        for view in search_result:
            search_result_links.append(view.get_attribute('href'))
        print("Song link(s) Founded!")

        # Selection from Multiple Albums
        selected = 1
        if len(list(search_result_links)) >= 2:  # This code checks if more than one album are there
            print("MORE THAN ONE ALBUM FOUND. Please select:\n")
            i = 1
            for each in search_result_links:
                print("Enter", (str(i)+","), "for", search_result[i-1].text)
                i += 1
            selected = int(input("Choice>>\t"))
        print("Traicing song album:", search_result[selected-1].text)
        browser.get(search_result_links[selected-1])
        # ENDS HERE
        
        if 'table' not in requests.get(search_result_links[selected-1]).text:   # FOR VERY OLD Layout without tables
            downloadable_links=browser.find_elements_by_xpath('//div/p/a/strong[contains(text(),"Download")]/..')
            for each_link in downloadable_links:
                link=each_link.get_attribute('href')
                if ("%20-%20"+song_requested+"%20-%20") in link:
                    tools.downloader(song_requested,link,getDestination())
                    break   
        else:
            bitrates=browser.find_elements_by_xpath("//tbody/tr/td[contains(text(),' {}')]/../td/a/strong[contains(text(),'Download')]/..".format(song_requested))
            if len(bitrates)==0:    #FOR OLD LAYOUT without selectable download quality
                bitrates=browser.find_element_by_xpath("//tbody/tr/td/span[contains(text(),' {}')]/../../td/strong/a[contains(text(),'Download')]".format(song_requested)).get_attribute('href')
                tools.downloader(song_requested,bitrates,getDestination())
            else:
                tools.qualitySelector(song_requested,bitrates,getDestination())

    except:
        print("Unexpected Error occured!")
        raise
    finally:
        browser.close()
        if os.path.exists('ghostdriver.log'):
            os.remove('ghostdriver.log')
        input('Press ENTER to exit')