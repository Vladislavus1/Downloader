# Youtube Video Downloader

This technology allow you tu download video right from <span style="color: red">**YouTube**</span>. All you need to do is to write needed channels in the table and my program will download all required videos into **Download** folder.

## How to use

To install all the requirements for the project run

	pip install -r requirements.txt

In the root directory. After the modules have been installed you can run the project by using python

	python parser.py

## How it works

In the main file, *parser.py*, the program reads data from the table:

    workbook = openpyxl.load_workbook("test_table.xlsx")
    worksheet = workbook.active

    data = []

    for row in worksheet.iter_rows(min_row=1, max_row=worksheet.max_row, min_col=1, max_col=worksheet.max_column,
                                   values_only=True):
        data.append(list(row))

Once the data is ready, the parser creates a driver:

    driver = webdriver.Chrome(service=service, options=options)

After creating a driver, the parser runs the *get_youtube_shorts_data(<span style="color: blue">driver</span>, <span style="color: blue">channel_id</span>, <span style="color: blue">channel_url</span>, <span style="color: blue">content_type</span>, <span style="color: blue">language</span>, <span style="color: blue">labels</span>, <span style="color: blue">download_limit</span>)* function, where:

    get_youtube_shorts_data(driver,
        channel_id,      # An id of the channel
        channel_url,     # The URL of the channel
        content_type,    # The type of content this channel produces
        language,        # The language spoken on this channel
        labels,          # Labels for this channel (Labels are saved in a text file)
        download_limit   # The limit of required videos
    )

After fetching the required data from YouTube, the program starts downloading videos:

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

When all the required videos are downloaded, the program stops.

# Thanks for attention!
