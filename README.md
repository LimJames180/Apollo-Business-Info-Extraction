# Apollo Business Info Extraction

This project provides a function `apollo_business_info` to extract structured business information from Apollo.io using a web crawler and LLM-based extraction strategy.

## Prerequisites

Ensure you have the following installed on your system:
- Python 3.8 or higher
- `pip` (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is not available, manually install the dependencies:
   ```bash
   pip install crawl4ai pydantic
   ```
   
3. Run the `crawl4ai-setup` command to complete the setup:
   ```bash
   crawl4ai-setup
   
What does it do? - Installs or updates required Playwright browsers (Chromium, Firefox, etc.) - Performs OS-level checks (e.g., missing libs on Linux) - Confirms your environment is ready to crawl

4. Set up your browser profile for the crawler:
   - Ensure you have a Chromium-based browser installed.
   - Update the `user_data_dir` in the `BrowserConfig` to point to your browser profile directory.


## Configuring Login with a Custom User Data Directory

If your application requires login or specific browser configurations, you can set up a custom user data directory for Playwright's Chromium browser. Follow these steps:

### Step 1: Locate the Playwright Chromium Binary
Playwright manages its own Chromium installation. To find the binary path:
1. Run the following command to see an overview of installed browsers:
   ```bash
   python -m playwright install --dry-run
   ```
   or
   ```bash
   playwright install --dry-run
   ```
2. This will display the path to the Chromium binary. For example:
   - **Linux**: `~/.cache/ms-playwright/chromium-1234/chrome-linux/chrome`
   - **macOS**: `~/Library/Caches/ms-playwright/chromium-1234/chrome-mac/Chromium.app/Contents/MacOS/Chromium`
   - **Windows**: `C:\Users\<you>\AppData\Local\ms-playwright\chromium-1234\chrome-win\chrome.exe`

### Step 2: Launch Chromium with a Custom User Data Directory
Use the Chromium binary to create or reuse a custom user data directory:
- **Linux**:
  ```bash
  ~/.cache/ms-playwright/chromium-1234/chrome-linux/chrome \
      --user-data-dir=/home/<you>/my_chrome_profile
  ```
- **macOS**:
  ```bash
  ~/Library/Caches/ms-playwright/chromium-1234/chrome-mac/Chromium.app/Contents/MacOS/Chromium \
      --user-data-dir=/Users/<you>/my_chrome_profile
  ```
- **Windows** (PowerShell/cmd):
  ```powershell
  "C:\Users\<you>\AppData\Local\ms-playwright\chromium-1234\chrome-win\chrome.exe" ^
      --user-data-dir="C:\Users\<you>\my_chrome_profile"
  ```

This will open Chromium with the specified profile directory. Log into any required sites or configure the browser as needed. Once done, close the browser to save the session data.

### Step 3: Use the Custom Profile in Your Code
Update your `BrowserConfig` to use the custom user data directory:
```python
from crawl4ai import AsyncWebCrawler, BrowserConfig

browser_config = BrowserConfig(
    headless=True,
    use_managed_browser=True,
    user_data_dir="/home/<you>/my_chrome_profile",  # Replace with your path
    browser_type="chromium"
)

crawler = AsyncWebCrawler(config=browser_config)
```

### Notes
- The custom user data directory preserves session data, cookies, and local storage for future runs.
- Ensure the path to the user data directory is correct and accessible.
- This setup is useful for automating tasks that require login or specific browser configurations.




## Usage

1. Import the function in your script:
   ```python
   from apollo_scraper import apollo_business_info
   ```

2. Prepare the required inputs:
   - `domain`: The domain of the business website (e.g., `"example.com"`).
   - `sesh`: A unique session ID for the crawler.
   - `crawler`: An instance of `AsyncWebCrawler` configured with `BrowserConfig`.
   - `apollo_key`: Your Apollo.io API key.
   - `deepseek_key`: Your DeepSeek API key.

3. Example implementation:
   ```python
   import asyncio
   from crawl4ai import AsyncWebCrawler, BrowserConfig
   from apollo_scraper import apollo_business_info

   async def main():
       browser_config = BrowserConfig(
           verbose=True,
           headless=False,
           use_managed_browser=True,
           browser_type="chromium",
           user_data_dir="/path/to/your/chrome/profile"
       )
       crawler = AsyncWebCrawler(config=browser_config)
       await crawler.start()

       try:
           data = await apollo_business_info(
               domain="www.microsoft.com",
               sesh="unique_session_id",
               crawler=crawler,
               apollo_key="your_apollo_api_key",
               deepseek_key="your_deepseek_api_key"
           )
           print(data)
       finally:
           await crawler.close()

   if __name__ == "__main__":
       asyncio.run(main())
   ```

4. Run your script:
   ```bash
   python your_script.py
   ```

## Notes

- Ensure your API keys (`apollo_key` and `deepseek_key`) are valid and have the necessary permissions.
- The `apollo_business_info` function returns a dictionary structured according to the `ReturnInfo` schema.
- If you encounter issues, check the browser configuration and ensure the required dependencies are installed.

## Dependencies

- `crawl4ai`: For web crawling and data extraction.
- `openai`: For LLM-based extraction.
- `pydantic`: For data validation and schema definition.

## License

This project is licensed under the terms of the MIT License.