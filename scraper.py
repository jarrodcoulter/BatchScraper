from firecrawl import FirecrawlApp
import os
import dotenv
import markdown2
from xhtml2pdf import pisa
import base64
import re
import time

dotenv.load_dotenv()

app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

def sanitize_filename(filename):
    """Sanitizes a string to be a valid filename."""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Truncate if too long (optional, but good practice)
    return filename[:200] + ".pdf"

def scrape_and_create_pdf(url_to_scrape):
    """Scrapes a single URL and creates a PDF from its content."""
    try:
        print(f"Scraping {url_to_scrape}...")
        scraped_data = app.scrape_url(
            url_to_scrape,
        )

        if scraped_data and scraped_data.success:
            metadata = scraped_data.metadata if hasattr(scraped_data, 'metadata') else {}
            article_title = metadata.get('title') if metadata else None

            if not article_title:
                article_title = scraped_data.title if hasattr(scraped_data, 'title') and scraped_data.title else 'scraped_content'
            
            # Sanitize title for filename, using a default if it's somehow still None or empty
            safe_title = article_title if article_title else 'untitled_scrape'
            output_pdf_filename = sanitize_filename(safe_title)
            markdown_content = scraped_data.markdown if hasattr(scraped_data, 'markdown') else None

            if markdown_content:
                print("Markdown content extracted. Converting to HTML...")
                html_content_from_markdown = markdown2.markdown(markdown_content)
                html_for_pdf = "<html><head><meta charset='UTF-8'><title>Scraped Content</title></head><body>"
                html_for_pdf += html_content_from_markdown
                html_for_pdf += "</body></html>"

                print(f"Generating PDF: {output_pdf_filename}...")
                with open(output_pdf_filename, "wb") as pdf_file:
                    pisa_status = pisa.CreatePDF(html_for_pdf, dest=pdf_file)
                if not pisa_status.err:
                    print(f"PDF saved as {output_pdf_filename}")
                else:
                    print(f"Error generating PDF for {url_to_scrape}: {pisa_status.err}")
            else:
                print(f"No markdown content found for {url_to_scrape}.")
                if scraped_data:
                    print(f"Full response (no markdown): {vars(scraped_data) if hasattr(scraped_data, '__dict__') else scraped_data}")
        else:
            print(f"Failed to scrape content or scrape was unsuccessful for {url_to_scrape}.")
            if scraped_data:
                print(f"Response: {vars(scraped_data) if hasattr(scraped_data, '__dict__') else scraped_data}")

    except Exception as e:
        print(f"An error occurred while processing {url_to_scrape}: {e}")

if __name__ == "__main__":
    urls_filename = "urls.txt"
    try:
        with open(urls_filename, 'r') as f:
            urls_to_process = [line.strip() for line in f if line.strip()]
        
        if not urls_to_process:
            print(f"No URLs found in {urls_filename}.")
        else:
            print(f"Found {len(urls_to_process)} URL(s) to process from {urls_filename}.")
            for i, url in enumerate(urls_to_process):
                print(f"\nProcessing URL {i+1}/{len(urls_to_process)}: {url}")
                scrape_and_create_pdf(url)
                if i < len(urls_to_process) - 1: # Add delay if not the last URL
                    print("Waiting 1 second before next request...")
                    time.sleep(1)
            print("\nAll URLs processed.")

    except FileNotFoundError:
        print(f"Error: The file {urls_filename} was not found. Please create it with one URL per line.")
    except Exception as e:
        print(f"An unexpected error occurred in the main process: {e}")
