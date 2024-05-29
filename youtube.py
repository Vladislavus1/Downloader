from imports import *


def remove_consecutive_duplicates(input_list):
    """Remove consecutive duplicates from a list."""
    if not input_list:
        return []

    output_list = [input_list[0]]
    for item in input_list[1:]:
        if item != output_list[-1]:
            output_list.append(item)
    return output_list


def scroll_to_bottom(driver):
    """Scroll to the bottom of the page."""
    old_position = 0
    new_position = None

    while new_position != old_position:
        old_position = driver.execute_script(
            "return window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;")
        time.sleep(1)
        driver.execute_script(
            "var scrollingElement = document.scrollingElement || document.body;"
            "scrollingElement.scrollTop = scrollingElement.scrollHeight;")
        new_position = driver.execute_script(
            "return window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0;")


def get_youtube_shorts_data(driver, channel_id, channel_url, content_type, language, labels, download_limit):
    """Scrape YouTube shorts data and download videos."""
    try:
        driver.get(channel_url)
        tabs_content = driver.find_element(By.ID, "tabsContent").find_elements(By.CSS_SELECTOR, "[role*='tab']")
        tabs_text = [tab.text for tab in tabs_content]

        if "YouTube Shorts" in tabs_text:
            driver.get(f"{channel_url}/shorts")
            scroll_to_bottom(driver)

            video_titles = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.ID, "video-title"))
            )

            all_links = driver.find_elements(By.TAG_NAME, "a")
            video_urls = [link.get_attribute("href") for link in all_links if
                          link.get_attribute("href") and "https://www.youtube.com/shorts/" in link.get_attribute(
                              "href")]

            video_urls = remove_consecutive_duplicates(video_urls)

            if download_limit:
                video_titles = [video_titles[i].text for i in range(min(download_limit, len(video_titles)))]
                video_urls = video_urls[:download_limit]
            else:
                video_titles = [title.text for title in video_titles]

            saving_path = os.path.join("Download", "Youtube", language, content_type, str(channel_id))
            os.makedirs(saving_path, exist_ok=True)

            for video_title, video_url in zip(video_titles, video_urls):
                video_title = re.sub(r'[^\w\s]', '', video_title).replace(" ", "_")[:90]
                try:
                    yt = YouTube(video_url)
                    video = yt.streams.first()
                    video.download(saving_path, filename=f"{video_title}.mp4")
                except AgeRestrictedError:
                    print(f"Skipping age-restricted video: {video_url}")

            label_list = [label + ',' for label in labels.split(',')[:-1]] + [labels.split(',')[-1]]
            with open(os.path.join(saving_path, f"{channel_id}.txt"), "w", encoding="utf-8") as label_file:
                for label in label_list:
                    label_file.write(label + "\n")
        else:
            print("No shorts found")
    finally:
        pass