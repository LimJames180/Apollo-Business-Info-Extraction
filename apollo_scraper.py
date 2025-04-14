import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, LLMConfig, MemoryAdaptiveDispatcher
from crawl4ai.extraction_strategy import LLMExtractionStrategy

from apollo_api import apollo_link
from instructions import instruction
from return_basemodel import ReturnInfo


async def apollo_business_info(domain : str, sesh : str, crawler : AsyncWebCrawler, apollo_key : str, deepseek_key : str, show_usage=False):
    """
    This function utilizes Apollo's API to generate a link for the organization's data and DeepSeek's LLM-based extraction strategy to scrape and extract structured business information. It employs a web crawler to navigate and extract data from the generated Apollo link.

Args:
    domain (str): The domain of the business website (e.g., "example.com").
    sesh (str): The session ID for the web crawler.
    crawler (AsyncWebCrawler): An instance of the asynchronous web crawler.
    apollo_key (str): API key for Apollo.io, used to generate the organization link.
    deepseek_key (str): API key for DeepSeek, used for LLM-based data extraction.
    show_usage (bool, optional): Whether to display token usage statistics. Defaults to False.

Returns:
    dict: A dictionary containing the extracted business information, structured according to the `ReturnInfo` schema.

Raises:
    Exception: If the crawling or data extraction process fails.

    :param domain:
    :param sesh:
    :param crawler:
    :param apollo_key:
    :param deepseek_key:
    :param show_usage:
    :return:
    """
    try:
        urls = apollo_link(domain, apollo_key)

        # 1. Define the LLM extraction strategy
        llm_strategy = LLMExtractionStrategy(
            llm_config = LLMConfig( provider="deepseek/deepseek-chat",
                api_token=deepseek_key),
                schema=ReturnInfo.model_json_schema(), # Or use model_json_schema()
                extraction_type="schema",
                instruction=instruction,
                chunk_token_threshold=1000,
                overlap_rate=0.0,
                apply_chunking=False,
                input_format="markdown",   # or "html", "fit_markdown"
                extra_args={"temperature": 0.0, "max_tokens": 800},
                timeout=60,

        )
        # 2. Build the crawler config
        crawl_config = CrawlerRunConfig(
            wait_for="""js:() => {
                    return document.querySelectorAll('td.zp_dqVxo').length > 1;
                }""",

            js_code="document.querySelector('a.zp-link.zp_d0CTE.zp_aFxA1').click();",
            exclude_external_links=False,
            process_iframes=True,
            remove_overlay_elements=True,
            wait_for_images=True,
            session_id=sesh,
            cache_mode=CacheMode.DISABLED  # Use cache if available

        )

        config2 = CrawlerRunConfig(
            js_code="document.querySelector('a.zp-link.zp_d0CTE.zp_aFxA1').click();",
            js_only=True,
            wait_for="""js:() => {
                            return document.querySelector('button.zp_brMBQ');
                        }""",
            session_id=sesh,
            extraction_strategy=llm_strategy,

        )
        await crawler.arun(
                url=urls,
                config=crawl_config
            )
        result = await crawler.arun(
                url=urls,
                config=config2
            )

        if result.success:
                # 5. The extracted content is presumably JSON
            data = json.loads(result.extracted_content)
                # 6. Show usage stats
            if show_usage:
                llm_strategy.show_usage()  # prints token usage
            return data[0]
        else:
            print("Error:", result.error_message)
            return
    except:
        raise Exception("apollo_business_info FAILED")

