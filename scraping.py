# Import dependencies
import pandas as pd

# Import scraping tools
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# Set up Splinter
executable_path = {"executable_path": ChromeDriverManager().install()}
browser = Browser("chrome", **executable_path, headless = False)

### News Article

# Visit NASA Mars News site
url = "https://redplanetscience.com/"
browser.visit(url)

# Optional delay for loading page
browser.is_element_present_by_css("div.list_text", wait_time = 1)

# Parse HTML
html = browser.html
news_soup = soup(html, "html.parser")
slide_elem = news_soup.select_one("div.list_text")

# Scrape for most recent article title
slide_elem.find("div", class_ = "content_title")

# Use parent element to find first "div" tag and save it as "news_title"
news_title = slide_elem.find("div", class_ = "content_title").get_text()
news_title

# Use parent element to find article summary
news_p = slide_elem.find("div", class_ = "article_teaser_body").get_text()
news_p

### Featured Image

# Visit Space Images site
url = "https://spaceimages-mars.com/"
browser.visit(url)

# Find and click full image button
full_image_elem = browser.find_by_tag("button")[1]
full_image_elem.click()

# Parse resulting HTML
html = browser.html
img_soup = soup(html, "html.parser")

# Find relative image URL
img_url_rel = img_soup.find("img", class_ = "fancybox-image").get("src")
img_url_rel

# Use base URL to create absolute URL
img_url = f"https://spaceimages-mars.com/{img_url_rel}"
img_url

### Facts

# Scrape table from Mars Facts site
df = pd.read_html("https://galaxyfacts-mars.com/")[0]
df.columns = ["Description", "Mars", "Earth"]
df.set_index("Description", inplace = True)
df

# Convert DF to HTML
df.to_html()

# End automated browsing session
browser.quit()