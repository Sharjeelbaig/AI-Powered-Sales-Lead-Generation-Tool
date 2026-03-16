# Import the DuckDuckGo search tool from LangChain community package
from langchain_community.tools import DuckDuckGoSearchRun

# Import the generic Tool wrapper from LangChain CORE (v1 correct import)
from langchain_core.tools import Tool

# Standard libraries for scraping and saving
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re

# Save-to-text tool: saves the output to a text file
def save_to_txt(data: str, filename: str = "./leads_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Leads Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    # Open the file in append mode so it keeps growing over time
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

# Scrape raw text from a website (renamed for Tool func)
def scrape_website(url: str) -> str:
    try:
        # Send GET request to the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad HTTP codes

        # Parse and clean up the raw HTML content
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace

        # Limit to 5000 characters for performance and API limits
        return text[:5000]
    except Exception as e:
        return f"Error scraping website: {str(e)}"

# Generate search queries to look for IT services related to a company
def generate_search_queries(company_name: str) -> list[str]:
    keywords = ["IT Services", "managed IT", "technology solutions"]
    return [f"{company_name} {keyword}" for keyword in keywords]

# Combined search and scrape operation for a company (fixed logic)
def search_and_scrape(company_name: str) -> str:
    try:
        queries = generate_search_queries(company_name)
        results = []
        search = DuckDuckGoSearchRun()  # Create instance here

        for query in queries:
            # Run web search
            search_results = search.invoke(query)  # Use .invoke() for v1

            # Extract URLs from the search output
            urls = re.findall(
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                search_results
            )

            # Scrape the first valid URL found
            if urls:
                scraped = scrape_website(urls[0])
                results.append(scraped)

        # Combine all the text results into one big chunk
        return " ".join(results) if results else "No results found."
    except Exception as e:
        return f"Error in search_and_scrape: {str(e)}"

# DuckDuckGo search tool
search = DuckDuckGoSearchRun()

# Define all tools with v1 Tool constructor
search_tool = Tool(
    name="search",
    description="Search the web for information",
    func=search.invoke  # Pass the function reference (.invoke for v1)
)

scrape_tool = Tool(
    name="scrape_website",
    description="Scrape raw text content from a website URL",
    func=scrape_website
)

search_and_scrape_tool = Tool(
    name="search_and_scrape",
    description="Search DuckDuckGo for a company and scrape the top website result",
    func=search_and_scrape
)

save_tool = Tool(
    name="save",
    description="Saves structured data (JSON/text) to a text file with timestamp",
    func=lambda data, filename="leads_output.txt": save_to_txt(data, filename),
    # Or use partial for default args: func=functools.partial(save_to_txt, filename="leads_output.txt")
)

# Export for main script
__all__ = ["search_tool", "scrape_tool", "search_and_scrape_tool", "save_tool"]