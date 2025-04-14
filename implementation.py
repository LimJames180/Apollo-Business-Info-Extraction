import asyncio

from crawl4ai import AsyncWebCrawler, BrowserConfig

from apollo_scraper import apollo_business_info

browser_config = BrowserConfig(verbose=True, headless=False,
                               use_managed_browser=True,  # Enables persistent browser strategy
                               browser_type="chromium",
                               user_data_dir="/Users/jameslim/my_chrome_profile"
                               )

async def main():
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()
    data = await apollo_business_info("www.microsoft.com", "sesh1", crawler, "XXX", "XXX")
    print(data)

    await crawler.close()


if __name__ == "__main__":
    asyncio.run(main())