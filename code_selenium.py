## v0.0.1

## Some helpful libraries
# BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
#   You can use this to parse the HTML DOM
# Selenium: https://www.seleniumhq.org/
#   You can use this to help scrape JavaScript loaded pages
# Requests: https://2.python-requests.org/en/master/
#   You can use this to help scrape non-JavaScript loaded pages.

## Other links
# Cook County Recorder of Deeds: http://162.217.184.82/i2/default.aspx
# If you are interested, all Cook County pin numbers can be downloaded here:
#   https://datacatalog.cookcountyil.gov/GIS-Maps/Historical-ccgisdata-Parcels-2016/a33b-b59u
# Test out your script and see how it performs on the many pin numbers that are found in cook county!

# Use this example pin to test your script
example_pin = '09-22-418-034-0000'
pin1='09-26-400-016-0000'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
#https://pypi.org/project/selenium/
#Download geckodriver for windows, linux or macos from: https://github.com/mozilla/geckodriver/releases
#Extract and add it to path
from bs4 import BeautifulSoup
#To install https://pypi.org/project/beautifulsoup4/
import time

def enter_pin(pin,driver):
    """
    #Use selenium driver to automate entering the PIN number

    Params:
        pin...The PIN number of the Cook County that will be scraped
        driver...The Selenium Object containing the html as python Objects.
    Returns:
        The html scraped
    """
    numbers = pin.split("-")
    nbox = 5
    n = 0
    for i in range(nbox):
        m = str(n)
        css = '#SearchFormEx1_PINTextBox' + m
        box = driver.find_element_by_css_selector(css)
        time.sleep(.2)
        box.send_keys(numbers[n])
        n+=1
    box.send_keys(Keys.RETURN)
    time.sleep(.3)
    
def beautifulsoup_scrape_html(id_table,deed_soup):
    """
    #Use beautifulsoup to scrape the html needed.

    Params:
        id_table...The id of the table that will be scraped
        deed_soup...The BeautifulSoup Object containing the html as python Objects.
    Returns:
        The html scraped
    """
    html = deed_soup.find(lambda tag: tag.name=='div' and tag.has_attr('id') and tag['id']==id_table)
    return html    
    
def page_scraping(p,driver):
    """
    #Use Selenium driver to move through the different deed links and select them to extract
    the information needed.

    Params:
        p...The page number that is going to be scraped
        driver...The Selenium Object containing the html as python Objects.
    Output:
        HTML files of each deed stored in the Resukts folder
    """
    #Create values to iterate through the deedlinks and initialize html to extract information
    a,b,html = [2,0,[]]
    #Find out the number of deeds listed on the page
    num_links1 = len(driver.find_elements_by_class_name('DataGridRow'))
    num_links2 = len(driver.find_elements_by_class_name('DataGridAlternatingRow'))
    num_links = num_links1 + num_links2
    #Iterate through the list of deeds on the page to extract the html wanted
    for i in range(num_links):
        #Transform int to string
        x = str(a) 
        y = str(b)
        z = str(p)
        #Define the id name to find the element for clicking
        if a<10:
            id = "DocList1_GridView_Document_ctl0" + x + "_ButtonRow_Recorded Date_" + y
        else:
            id = "DocList1_GridView_Document_ctl" + x + "_ButtonRow_Recorded Date_" + y
        #Navigate to link
        button = driver.find_element_by_id(id)
        button.click()
        time.sleep(.25)
        #Create BeautifulSoup Object containing the html as python Objects.
        deed_soup = BeautifulSoup(driver.page_source, 'html.parser')
        #Extract the html information needed and save it in an html    
        id_table = "DocDetails1_ContentContainer1"
        html=beautifulsoup_scrape_html(id_table,deed_soup)
        #Write HTML String to file_x.html
        path = "results/deed_" + y + "_Page" + z +".html"
        with open(path, "w") as file:
            file.write(str(html))
    
        a+=1
        b+=1

def scrape_and_change_pages(driver):
    """
    #Use Selenium driver to select and move through the pages of the Cook County website. 

    Params:
        driver...The Selenium Object containing the html as python Objects.
    
    """
    num_pages = len(driver.find_elements_by_class_name('PagerNumberButton'))
    p=1
    page_scraping(p,driver)
    for i in range(num_pages):
        #Navigate to page number
        page = driver.find_element_by_class_name("PagerNumberButton")
        page.click()
        time.sleep(.5)
        p+=1 
        page_scraping(p,driver)
    print("All pages have been scraped")    
        
def shut_down_browser(driver):
    """
    #Close the window browser.

    Params:
        driver...The Selenium Object containing the html as python Objects.
    
    """
    driver.quit()     
    

def main():
    start = time.time()
    print("Enodo Scraping Test")
    
    # 1. Obtain url for scraping
    url = "http://162.217.184.82/i2/default.aspx#"
    
    # 2. Use Selenium webdriver to open a new browser window.
    opts = Options()
    opts.headless = True
    # Set headless mode on
    driver = webdriver.Firefox(options=opts)
    #driver = webdriver.Firefox() #Use to see the browser
    driver.get(url)
    driver.implicitly_wait(100)
    
    # 3. Automatically enter pin number that will be scraped
    enter_pin(example_pin,driver)
    
    # 4. Scraped through the different deeds and through the different pages
    scrape_and_change_pages(driver)
    
    # 5. Close the window browser
    shut_down_browser(driver)
    
    print('It took', time.time()-start, 'seconds.')

if __name__ == "__main__":
    main()
    
