from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd 
import datetime as dt 

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)

mars_information = {}

def scrape_news():
    
        browser = init_browser()
        url = "https://mars.nasa.gov/news"
        browser.visit(url)
        browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")

        title = soup.find('div', class_='content_title').find('a').text
        paragraph = soup.find('div', class_='article_teaser_body').text
    
        return title, paragraph

def scrape_image():

        browser = init_browser()
        url="https://www.jpl.nasa.gov/spaceimages/?search=&categ"
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        featured_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
        main_url = 'https://wwww.jpl.nasa.gov/'
        featured_image_url = main_url + featured_url
        
        return featured_image_url

def scrape_weather():

        browser = init_browser()
        url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        mars_weather = soup.find('div', class_='js-tweet-text-container').find('p').text
    
        return mars_weather

def scrape_facts():
   
    url="https://space-facts.com/mars"
    tables = pd.read_html(url)
    mars_data = pd.DataFrame(tables[0])
    mars_data.columns=['Mars','Data']
    mars_table = mars_data.set_index("Mars")
    mars_info = mars_table.to_html(classes = 'mars_info')
    mars_info = mars_info.replace('\n', ' ') 
    
    return mars_info

def scrape_hemispheres():

        browser = init_browser()
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        hemispheres = soup.find_all('div', class_='item')
        hemisphere_urls = []
        main_url = 'https://astrogeology.usgs.gov'
        for h in hemispheres:
            title = h.find('h3').text
            img_url = h.find('a', class_='itemLink product-item')['href']
            browser.visit(main_url+ img_url)
            img_html = browser.html
            soup = BeautifulSoup(img_html, 'html.parser')
            img_two = main_url+ soup.find('img', class_='wide-image')['src']
            hemisphere_urls.append({"title": title, "img_url": img_two})        

        return hemisphere_urls

def scrape_everything():
    
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)
    title, paragraph = scrape_news()
    image_url = scrape_image()
    mars_weather = scrape_weather
    facts = scrape_facts
    hemisphere_image_urls = scrape_hemispheres

    data = {
        "title": title,
        "paragraph": paragraph,
        "featured_image": image_url,
        "weather": mars_weather,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_everything())