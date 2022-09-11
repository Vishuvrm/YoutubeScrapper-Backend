from webdriver_manager.chrome import ChromeDriverManager
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from pytube import YouTube


def get_channel_videos_data(channel_link, num_videos):
    channel_videos_link = channel_link + "/videos"

    driver = get_driver_connectivity()
    driver.get(channel_videos_link)

    scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web

    # driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=1))  
    i = 1

    while True:
        # scroll one screen height each time
        
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.documentElement.scrollHeight;")  
        videos = driver.find_element(By.ID, "items").find_elements(By.XPATH, "//*[@id='thumbnail']")

        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height or len(videos) >= num_videos+1:
            videos = videos[1:num_videos+1]
            break 

    video_data = {}

    for video in videos:
        video_link = video.get_attribute("href")
        video_data[video_link] = {}

    for link in video_data:
        driver.get(url=link)
        time.sleep(scroll_pause_time)
        while True:
            try:
                title_html = driver.find_element(by=By.XPATH, value="""//*[@id="container"]/h1/yt-formatted-string""").get_attribute("outerHTML")
                title = BeautifulSoup(title_html, 'html.parser').find("yt-formatted-string").text
                author = driver.find_element(by=By.XPATH, value="""//*[@id="text"]/a""").text
                likes_html = driver.find_element(by=By.XPATH, value="""//*[@id="top-level-buttons-computed"]/ytd-toggle-button-renderer[1]/a""").get_attribute("outerHTML")
                likes = BeautifulSoup(likes_html, 'html.parser').find("yt-formatted-string").attrs["aria-label"]
                thumbnail = driver.find_element(by=By.XPATH, value='//*[@id="watch7-content"]/link[2]').get_attribute("href")
                # comments = get_comments(driver)
                
                video_data[link] = {
                    "channel_link": channel_link,
                    "title": title,
                    "author": author,
                    "likes": likes,
                    "thumbnail": thumbnail
                    # "comments": comments
                }
                
            except selenium.common.exceptions.NoSuchElementException as e:
                print("Error with the URL:", link)
                print("ERROR:", e)
            finally:
                break
    driver.close()
    return video_data


def download_video(url, location, filename, *args, **kwargs):
    try:
        youtube_object = YouTube(url)
        stream = youtube_object.streams.get_by_itag(22)
        stream.download(output_path=location, filename=filename, *args, **kwargs,)
        return 1
    except Exception as e:
        print(e)
        return 0

def get_comments(url, max_extra_scrolls = 2):
    scroll_pause_time = 1
    driver = get_driver_connectivity()
    driver.get(url)
    time.sleep(1)
    screen_height = driver.execute_script("return window.screen.height;")
    driver.execute_script(f"window.scrollTo(0, {60});") 
    time.sleep(scroll_pause_time)
    i = 1
    prev_num_comments = 0
    num_extra_scrolls = 0
    while True:
        # scroll one screen height each time
        driver.execute_script(f"window.scrollTo(0, {screen_height*i});")  
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.documentElement.scrollHeight;")  
        # Break the loop when the height we need to scroll to is larger than the total scroll height

        comments_data = driver.find_elements(By.CSS_SELECTOR, '#comment #main')
        new_num_comments = len(comments_data)
        
        if new_num_comments == prev_num_comments and num_extra_scrolls < max_extra_scrolls:
            num_extra_scrolls += 1
            i += 1
            continue
        elif new_num_comments != prev_num_comments:
            num_extra_scrolls = 0

        if ((screen_height) * i > scroll_height or new_num_comments==prev_num_comments) and num_extra_scrolls==max_extra_scrolls:
            comments = []
            for c_data in comments_data:
                commenter = c_data.find_element(By.CSS_SELECTOR, "#body #header #header-author > h3 #author-text").text
                comment = c_data.find_element(By.CSS_SELECTOR, "#content #content-text")
                comments.append({"commenter_name": commenter, "comment" : f"""{BeautifulSoup(comment.get_attribute("outerHTML"), "html.parser").find_all()[0].text}"""})
            return comments 

        prev_num_comments = new_num_comments


def get_driver_connectivity():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    return webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)


__all__ = ["get_channel_videos_data", "download_video", "get_comments"]


if __name__ == "__main__":
    channel_link = "https://www.youtube.com/user/krishnaik06"
    print(get_channel_videos_data(channel_link, 2))
