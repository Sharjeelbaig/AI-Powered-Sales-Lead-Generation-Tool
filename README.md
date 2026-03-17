# Scrawler - AI-Powered Sales Lead Generation Tool

Scrawler is an AI-powered sales enablement tool designed to help IT service providers identify and qualify local small businesses that might need IT services. The tool uses natural language processing, web search, and web scraping to gather information about potential leads and generate tailored outreach messages.

## Features

- **AI-Powered Lead Generation**: Uses LangChain with Ollama to understand and execute search queries
- **Web Search**: Integrates with DuckDuckGo to search for local businesses
- **Web Scraping**: Extracts information from company websites using BeautifulSoup
- **Structured Output**: Generates leads with detailed information in a structured format
- **Lead Saving**: Saves generated leads to a text file with timestamps for future reference
- **Outreach Message Generation**: Creates personalized outreach messages based on scraped company information

## Technology Stack

- **Python**: Main programming language
- **LangChain**: Framework for building AI applications
- **Ollama**: Local AI model runner (uses GLM 5 model)
- **DuckDuckGo Search**: Web search integration
- **BeautifulSoup**: Web scraping library
- **Pydantic**: Data validation and parsing
- **LangGraph**: Agent orchestration with memory

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Sharjeelbaig/AI-Powered-Sales-Lead-Generation-Tool
   cd scrawler
   ```

2. Install dependencies using uv (or pip):
   ```bash
   uv pip install -r requirements.txt
   ```

3. Install Ollama and download the required model:
   ```bash
   # Install Ollama (follow instructions at https://ollama.com/)
   ollama pull glm-5:cloud
   ```

## Usage

1. Run the main script:
   ```bash
   uv run python main.py
   ```

2. The tool will:
   - Search for 5 local small businesses in Vancouver, British Columbia that might need IT services
   - Scrape their websites for information
   - Analyze the data using AI
   - Generate personalized outreach messages
   - Save the results to `leads_output.txt`

## Project Structure

```
scrawler/
├── main.py              # Main entry point of the application
├── tools.py             # Custom tools for search, scraping, and saving
├── prompts/
│   └── system.py        # System prompt for the AI agent
├── pyproject.toml       # Project dependencies
├── uv.lock              # Dependency lock file
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Configuration

### Customizing the Search Query

Modify the human message content in `main.py` (line 41) to change the search criteria:

```python
result = agent.invoke(
    {"messages": [HumanMessage(content="Find 5 local small businesses in Vancouver, British Columbia, that might need IT services and provide detailed information about them.")]}, 
    config
)
```

### Adjusting the System Prompt

Edit the system prompt in `prompts/system.py` to change how the AI agent behaves and what information it collects.

## Output

The generated leads are saved to `leads_output.txt` with the following structure:

```
--- Leads Output ---
Timestamp: 2024-03-16 14:30:00

[
  {
    "company": "Example Company Inc.",
    "contact_info": "123-456-7890",
    "email": "contact@example.com",
    "summary": "Small retail business with outdated website and no online presence. Could benefit from IT services including website redesign and digital marketing.",
    "outreach_message": "Hi [Name], I noticed your business could benefit from a modern website and online marketing solutions. We specialize in helping small businesses improve their digital presence...",
    "tools_used": ["search", "scrape_website"]
  },
  ...
]
```

## Dependencies

All dependencies are listed in `pyproject.toml` and include:
- beautifulsoup4
- duckduckgo-search
- langchain
- langchain-community
- langchain-ollama
- langgraph
- pydantic
- python-dotenv

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
