# tourism.gov.ru-scraper
This is a Python GUI application for web scraping tourism-related information from the website tourism.gov.ru. 
The application uses various Python libraries, including pandas, tkinter, ttkthemes, selenium, BeautifulSoup, and logging, to automate the data extraction process.

## Features

- Web Scraping: The application scrapes information from multiple pages of the tourism website, extracting data from individual cards.

-    Data Extraction: It extracts data from the "Основная информация" (Main Information) section of each card, collecting relevant information.

-    Multi-Page Scraping: The application supports scraping multiple pages of tourism-related data by specifying the number of pages to scrape.

-    Progress Indicator: It provides a progress indicator, showing the current page being processed out of the total number of pages.

-    Data Export: Extracted data is saved to an Excel file (Туризм_извлеченные_данные.xlsx) for further analysis.

-    Error Logging: Errors and information during the scraping process are logged to a file (логи.log) for debugging purposes.
## Usage
1. Install the required Python libraries using pip:
```python
pip install openpyxl pandas ttkthemes selenium beautifulsoup4

```

2. Make sure you have the Chrome WebDriver installed and the path to the WebDriver is added to your system's PATH.

3. Run the provided Python code. This will launch the Tourism Scraping GUI.

4. Enter the number of pages you want to scrape (between 1 and 20000) in the input field.

5. Click the "Начать парсинг" (Start Scraping) button to begin the scraping process.

6. The application will scrape data from the specified number of pages and save it to an Excel file.
## Disclaimer

Web scraping may be subject to legal and ethical considerations. Ensure that you have the necessary permissions and adhere to the website's terms of service when using this tool. The authors and contributors of this application are not responsible for any misuse or legal consequences resulting from its use. Use it responsibly and within legal boundaries.
