# Import dependencies
import pandas as pd
import datetime as dt

# Import scraping tools
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# Create scrape_all function
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless = True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featured_image(browser),
            "facts": mars_facts(),
            "last_modified": dt.datetime.now()}
    
    # Stop webdriver and return data
    browser.quit()
    return data

### News Article

# Create NASA Mars News scraping function
def mars_news(browser):

    # Visit NASA Mars News site
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # Optional delay for loading page
    browser.is_element_present_by_css("div.list_text", wait_time = 1)

    # Parse HTML
    html = browser.html
    news_soup = soup(html, "html.parser")
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("div.list_text")
        # Use parent element to find first "div" tag and save it as "news_title"
        news_title = slide_elem.find("div", class_ = "content_title").get_text()
        # Use parent element to find article summary
        news_p = slide_elem.find("div", class_ = "article_teaser_body").get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

### Featured Image

# Create Space Images scraping function
def featured_image(browser):

    # Visit Space Images site
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    # Find and click full image button
    full_image_elem = browser.find_by_tag("button")[1]
    full_image_elem.click()

    # Parse resulting HTML
    html = browser.html
    img_soup = soup(html, "html.parser")

    # Add try/except for error handling
    try:
        # Find relative image URL
        img_url_rel = img_soup.find("img", class_ = "fancybox-image").get("src")

    except AttributeError:
        return None

    # Use base URL to create absolute URL
    img_url = f"https://spaceimages-mars.com/{img_url_rel}"
    
    return img_url

### Facts

# Create Mars Facts scraping function
def mars_facts():

    # Add try/except for error handling
    try:
        # Scrape table from Mars Facts site
        df = pd.read_html("https://galaxyfacts-mars.com/")[0]
    
    except BaseException:
        return None

    # Assign columns and set index of DF
    df.columns = ["Description", "Mars", "Earth"]
    df.set_index("Description", inplace = True)

    # Convert DF to HTML and add bootstrap
    return df.to_html(classes = "table table-striped")

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())