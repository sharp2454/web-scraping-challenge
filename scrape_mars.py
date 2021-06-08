

#import dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager



#setup path & initialize browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)



#visit Mars news site 
def mars_news(browser):
    url = "https://redplanetscience.com/"
    browser.visit(url)



#parse results with BeautifulSoup - collect the latest News Title and Paragraph Text
    html = browser.html
    news_soup = BeautifulSoup(html,"html.parser")




#slide_element = news_soup.select_one("div.content_title").text
#slide_element
    try:

        news_paragraph = news_soup.find("div", class_="article_teaser_body").text
        news_title = news_soup.find("div", class_="content_title").text
    except AttributeError:
        return None, None    
    return news_title, news_paragraph







# ## JPL Mars Space Images - Featured Image

def featred_image(browser):
#visit Mars space site
    url = "https://spaceimages-mars.com/"
    browser.visit(url)



    html = browser.html
    mars_image_soup = BeautifulSoup(html,"html.parser")
    mars_image_soup


    try:
        mars_image = mars_image_soup.find("img", class_="headerimage fade-in").get("src")
    
    except AttributeError:
        return None
        


    featured_image_url = f'https://spaceimages-mars.com/{mars_image}'
    return featured_image_url


# ## Mars facts

def mars_facts():
#visit Mars facts site and use Pandas to read


    try:
        mars_df = pd.read_html ("https://galaxyfacts-mars.com/")[1]
    except BaseException:
        return None
    mars_df.columns=['description', 'value']
    #mars_df.set_index('description', inplace=True)


    return mars_df.to_html()

# ## Mars Hemispheres

def hemisphere(browser):
#visit the astrogeology site 
    url = "https://marshemispheres.com/"
    browser.visit(url)

hemisphere_image_urls = []


#obtain images of all hemispheres



    #html = browser.html
    #hemispheres_soup = BeautifulSoup(html,"html.parser")
    #hemispheres_soup



    

# First, get a list of all of the hemispheres
    links = browser.find_by_css("a.product-item h3")

# Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(4):
        hemisphere = {}
    
    # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()
    
    # Next, we find the Sample image anchor tag and extract the href
    # sample_elem = browser.find_link_by_text('Sample').first
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
    
    # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text
    
    # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)
    
    # Finally, we navigate backwards
        browser.back()
    return hemisphere_image_urls   

##    
    def scrape_hemisphere(html_text):
        hemisphere_soup = BeautifulSoup(html_text, "html.parser")
        try:
            title_element = hemisphere_soup.find("h2", class_="title").get_text()
            sample_element = hemisphere_soup.find("a", text="Sample").get("href")
        except AttributeError:
            title_element = None
            sample_elem = None
        hemisphere = {
            "title": title_element,
            "img_url": sample_elem
    }      

        return hemisphere  


#######
    def scrape_all():
        executable_path =  {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)  
        news_title, news_paragraph = mars_news(browser)
        featured_img_url =  featred_image(browser)
        mars_df = mars_facts()
        hemisphere_image_urls = hemisphere 

        data = {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featured_img_url,
            "mars_df": mars_facts,
            "hemisphere": hemisphere_image_urls
        }

        browser.quit()

        return data

    if __name__=="__main__":
    print(scrape_all())