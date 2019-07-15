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
#https://pypi.org/project/beautifulsoup4/
import time
import requests
#https://gitlab.spritecloud.com/johnlock/link_checker/tree/4f073d6a819d8f0f2e2e087bf9f34a6fad2aba08/venv/Lib/site-packages/requests-2.21.0.dist-info

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
    #print(html.prettify())
    return html    

def request_deed_html(scriptManager,target,numbers):
    """
    #Use requests library to obtain the content of each deed and with Beautifulsoup 
    parse and extract the html.

    Params:
        scriptManager...Parameter used for requests
        target...Parameter used for requests
        numbers...List that contains the PIN number
    Return:
        HTML file of each deed scraped with beautiful soop
    """
    #Create header and data structure for requests
    headers = {
            'Referer': 'http://162.217.184.82/i2/default.aspx',
            'Cache-Control': 'no-cache',
            'Origin': 'http://162.217.184.82',
            'X-Requested-With': 'XMLHttpRequest',
            'X-MicrosoftAjax': 'Delta=true',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'IsImageUndock=False; DetailsViewMode=True; ASP.NET_SessionId=nfoaz3nj55la5izzzvvga155; BIGipServerpool_rod_public_website=1376261292.20480.0000; TS01688ffb=0169e52ff5a485c60e48506141c828b7b9875d9b3c122e165183e1b3bf0d347b0470762ba0b18496f27fa38d4ab219eaffb1ed3c64c2bb2c8ccdb8a9aad3564effc0c555ef644d84529359fb70f7e231216c0c0040', 
            }

    data = {
            'ScriptManager1': scriptManager,
            'ScriptManager1_HiddenField': ';;AjaxControlToolkit, Version=3.5.40412.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:1547e793-5b7e-48fe-8490-03a375b13a33:effe2a26;;AjaxControlToolkit, Version=3.5.40412.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:1547e793-5b7e-48fe-8490-03a375b13a33:475a4ef5:5546a2b:497ef277:a43b07eb:d2e10b12:37e2e5c9:5a682656:1d3ed089:f9029856:d1a1d569',
            '__EVENTTARGET': target,
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': '',
            'Navigator1$SearchOptions1$DocImagesCheck': 'on',
            'SearchFormEx1$PINTextBox0': numbers[0],
            'SearchFormEx1$PINTextBox1': numbers[1],
            'SearchFormEx1$PINTextBox2': numbers[2],
            'SearchFormEx1$PINTextBox3': numbers[3],
            'SearchFormEx1$PINTextBox4': numbers[4],
            'SearchFormEx1$ACSTextBox_Subdivision': '',
            'SearchFormEx1$ACSTextBox_BlockNo': '',
            'SearchFormEx1$ACSTextBox_LotNo': '',
            'SearchFormEx1$ACSTextBox_PartOfLotNo': '',
            'SearchFormEx1$ACSTextBox_DeclarationCondoNo': '',
            'SearchFormEx1$ACSTextBox_BuildingNo': '',
            'SearchFormEx1$ACSTextBox_UnitNo': '',
            'SearchFormEx1$ACSTextBox_AcresNo': '',
            'SearchFormEx1$ACSTextBox_Quarter3': '',
            'SearchFormEx1$ACSTextBox_Quarter2': '',
            'SearchFormEx1$ACSTextBox_Quarter1': '',
            'SearchFormEx1$ACSTextBox_Part1Code': '',
            'SearchFormEx1$ACSTextBox_Part2Code': '',
            'SearchFormEx1$ACSTextBox_OneHalfCode': '',
            'ImageViewer1$ScrollPos': '',
            'ImageViewer1$ScrollPosChange': '',
            'ImageViewer1$_imgContainerWidth': '0',
            'ImageViewer1$_imgContainerHeight': '0',
            'ImageViewer1$isImageViewerVisible': 'true',
            'ImageViewer1$hdnWidgetSize': '',
            'ImageViewer1$DragResizeExtender_ClientState': '',
            'CertificateViewer1$ScrollPos': '',
            'CertificateViewer1$ScrollPosChange': '',
            'CertificateViewer1$_imgContainerWidth': '0',
            'CertificateViewer1$_imgContainerHeight': '0',
            'CertificateViewer1$isImageViewerVisible': 'true',
            'CertificateViewer1$hdnWidgetSize': '',
            'CertificateViewer1$DragResizeExtender_ClientState': '',
            'PTAXViewer1$ScrollPos': '',
            'PTAXViewer1$ScrollPosChange': '',
            'PTAXViewer1$_imgContainerWidth': '0',
            'PTAXViewer1$_imgContainerHeight': '0',
            'PTAXViewer1$isImageViewerVisible': 'true',
            'PTAXViewer1$hdnWidgetSize': '',
            'PTAXViewer1$DragResizeExtender_ClientState': '',
            'DocList1$ctl09': '',
            'DocList1$ctl11': '0',
            'NameList1$ScrollPos': '',
            'NameList1$ScrollPosChange': '',
            'NameList1$_SortExpression': '',
            'NameList1$ctl03': '',
            'NameList1$ctl05': '',
            'DocDetails1$PageSize': '',
            'DocDetails1$PageIndex': '',
            'DocDetails1$SortExpression': '',
            'BasketCtrl1$ctl01': '',
            'BasketCtrl1$ctl03': '',
            'OrderList1$ctl01': '',
            'OrderList1$ctl03': '',
            '__ASYNCPOST': 'true',
            }
    #Navigate to link with push
    r = requests.post('http://162.217.184.82/i2/default.aspx', headers=headers, data=data)
    #Obtain content of object r
    page_content = r.content
    #Create beautifulsoup object containing the html as python Objects.
    deed_soup = BeautifulSoup(page_content, "html.parser")   
    #Find and extract the html information needed
    html = deed_soup.find(lambda tag: tag.name=='div' and tag.has_attr('id') and tag['id']=='DocDetails1_ContentContainer1')
    return html
    
def page_scraping(p,driver,pin):
    """
    #Use  to move through the different deed links and select them to extract
    the information needed.

    Params:
        p...The page number that is going to be scraped
        driver...The Selenium Object containing the html as python Objects
        pin...The PIN number of the Cook County that will be scraped
    Output:
        HTML files of each deed stored in the Results folder
    """
    #Create values to iterate through the deedlinks and initialize html to extract information
    a,b,html = [2,0,[]]
    numbers = pin.split("-")

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
        #Define the target and scriptManager to define the parameters for requests
        if a<10:
            target = "DocList1$GridView_Document$ctl0" + x + "$ButtonRow_Recorded Date_" + y
            scriptManager = "DocList1$UpdatePanel|DocList1$GridView_Document$ctl0" + x + "$ButtonRow_Recorded Date_" + y
        else:
            target = "DocList1$GridView_Document$ctl" + x + "$ButtonRow_Recorded Date_" + y
            scriptManager = "DocList1$UpdatePanel|DocList1$GridView_Document$ctl" + x + "$ButtonRow_Recorded Date_" + y
        
        #Request each deed and extract the html information needed and save it in a .html   
        html=request_deed_html(scriptManager,target,numbers)
        #Write HTML String to file_x.html
        path = "results/deed_" + y + "_Page" + z +".html"
        with open(path, "w") as file:
            file.write(str(html))
    
        a+=1
        b+=1

def scrape_and_change_pages(driver,pin):
    """
    #Use Selenium driver to select and move through the pages of the Cook County website. 

    Params:
        driver...The Selenium Object containing the html as python Objects.
        pin...The PIN number of the Cook County that will be scraped

    """
    num_pages = len(driver.find_elements_by_class_name('PagerNumberButton'))
    p=1
    page_scraping(p,driver,pin)
    for i in range(num_pages):
        #Navigate to page number
        page = driver.find_element_by_class_name("PagerNumberButton")
        page.click()
        time.sleep(.5)
        p+=1 
        page_scraping(p,driver,pin)
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
    scrape_and_change_pages(driver,example_pin)
    
    # 5. Close the window browser
    shut_down_browser(driver)
    
    print('It took', time.time()-start, 'seconds.')

if __name__ == "__main__":
    main()
