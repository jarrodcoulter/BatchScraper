# Batch URL Scraper to PDF

This script scrapes a list of URLs, extracts the main content as markdown, and converts it into individual PDF files. Each PDF is named after the title of the scraped web page.

## Features

- Reads URLs from a `urls.txt` file.
- Scrapes web content using the Firecrawl API.
- Converts extracted markdown content to HTML.
- Generates a PDF file for each URL using `xhtml2pdf`.
- Saves generated PDFs into a `pdfs/` directory.
- Sanitizes article titles to create valid filenames.

## Setup

1.  **Prerequisites:**
    *   Python 3.x
    *   pip (Python package installer)

2.  **Clone the repository (if applicable) or download the files.**

3.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
    ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up environment variables:**
    *   Create a file named `.env` in the project root.
    *   Add your Firecrawl API key to it:
        ```
        FIRECRAWL_API_KEY="fc-your_api_key_here"
        ```

## Usage

1.  **Populate `urls.txt`:**
    *   Create a file named `urls.txt` in the project root directory.
    *   Add one URL per line that you want to scrape. See `urls.txt.example` for an example.

2.  **Run the scraper:**
    ```bash
    python scraper.py
    ```

3.  **Output:**
    *   The script will process each URL from `urls.txt`.
    *   Generated PDF files will be saved in the `pdfs/` directory within the project root.
    *   Progress and any errors will be printed to the console.

## Project Structure

```
BatchScraper/
├── .env                # API keys and environment variables (not committed)
├── .gitignore          # Specifies intentionally untracked files
├── scraper.py          # The main Python script
├── requirements.txt    # Python package dependencies
├── urls.txt            # List of URLs to scrape (you create this)
├── urls.txt.example    # Example format for urls.txt
├── pdfs/               # Directory where output PDFs are saved (created by script if not present, gitignored)
└── README.md           # This file
```

## Dependencies

- `firecrawl-py`: For scraping web content.
- `python-dotenv`: For managing environment variables.
- `markdown2`: For converting markdown to HTML.
- `xhtml2pdf`: For converting HTML to PDF.
