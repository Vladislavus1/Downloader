from youtube import get_youtube_shorts_data
from imports import *


def update_worksheet_with_data(ws, data):
    """Update the worksheet with data."""
    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, cell_value in enumerate(row_data, start=1):
            ws.cell(row=row_idx, column=col_idx, value=cell_value)


def run_app():
    """Run the application to process YouTube shorts data and update the worksheet."""
    workbook = openpyxl.load_workbook("test_table.xlsx")
    worksheet = workbook.active

    data = []

    # Extract data from the worksheet
    for row in worksheet.iter_rows(min_row=1, max_row=worksheet.max_row, min_col=1, max_col=worksheet.max_column,
                                   values_only=True):
        data.append(list(row))

    # Setup the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Process each row of data
        for data_row in data:
            if data_row[1] == 'Youtube':
                get_youtube_shorts_data(
                    driver=driver,
                    channel_id=data_row[0],
                    channel_url=data_row[2],
                    content_type=data_row[3],
                    language=data_row[4],
                    labels=data_row[7],
                    download_limit=data_row[5]
                )
                data_row[6] = datetime.now().strftime("%d.%m.%Y:%H:%M")

        # Update the worksheet with the new data
        update_worksheet_with_data(worksheet, data)
        workbook.save("test_table.xlsx")

    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    run_app()