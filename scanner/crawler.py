import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

class crawler():

    urls = []
    inputs = []
    #outputs = {}
    target = ""
    
    def __init__(self, target, choice):
        if target[-1:] == "/":
            self.target = target[:-1]
        else:
            self.target = target
        
        if choice == 1:
            self.crawl(self.target)
        elif choice == 2:
            self.crawl_browser(self.target, 1)
        elif choice == 4:
            self.crawl_browser(self.target, 2)
        elif choice == 5:
            self.crawl_browser(self.target, 3)
        elif choice == 6:
            self.crawl_browser(self.target, 4)
        else:
            self.crawl(self.target)
            self.crawl_browser(self.target, 1)
            
    def crawl(self, target):
        """
        this methode finds hopefully all linked pages of the target and inputs on these and saves them to the class attributes
        """ 
        
        #------------------------------------------------------------------------
        #Request the page via requests and do the standard checks
        
        page = requests.get(url = target, timeout=10, verify=False)
        if page:
            self.urls.append(target)
        else:
            return
            
        soup = BeautifulSoup(page.content, 'lxml')
        
        print("--------------------------------------")
        print("Current Page: ", target)
        print("")
        #print(page.text)
        #print("")
        
        #find all available and maybe injectable inputs
        inputs = soup.find_all("input")
        for inp in inputs:
            if inp.has_attr('id'):
                if target+ "?"+inp['id'] not in self.inputs:
                    #print("Input(id): ", target+ "?"+inp['id'])
                    self.inputs.append(target+ "?"+inp['id'])
            elif inp.has_attr('name'):
                if target+ "?"+inp['name'] not in self.inputs:
                    #print("Input(name): ", target+ "?"+inp['name'])
                    self.inputs.append(target+ "?"+inp['name'])


        #find all links and follow them
        links = soup.find_all("a", href=True)
        for link in links:
            if link['href'].startswith("./"):
                link['href'] = self.target + "/" + link['href']
            if link['href'].startswith("/"):
                link['href'] = self.target + "/" + link['href']
            if link['href'].startswith(self.target):
                if link['href'] in self.urls:
                    links.remove(link)
                #else:
                    #print("Link:", link['href'])
            else:
                links.remove(link)
        
        for link in links:
            link['href'] = link['href'].replace("localhost", "127.0.0.1")
            if link['href'] not in self.urls:
                try:
                    if requests.get(url = link['href']):
                        self.crawl(link['href'])
                    else:
                        print("Page ", link['href'], " not found")
                except Exception as e:
                    print("Error occured: ", e)
                    
    def crawl_browser(self, target, browserSelection):
        """crawling the given target with selenium firefox or chrome"""  
            
        if browserSelection == 1 or browserSelection == 3:
            options = Options()
            if browserSelection == 3 or browserSelection == 4:
                options.headless = True
            else:
                options.headless = False 
            #options.add_argument("-profile")
            #options.add_argument("/home/kali/.mozilla/firefox/9lm0adll.default-esr")
            browser = webdriver.Firefox(options=options)
        if browserSelection == 2 or browserSelection == 4:
            options = webdriver.ChromeOptions()
            if browserSelection == 3 or browserSelection == 4:
                options.headless = True
            else:
                options.headless = False 
            #options.add_argument("--user-data-dir=/home/kali/.config/chromium")
            browser = webdriver.Chrome(options=options)
            
        browser.set_page_load_timeout(30)
        self.browser = browser
        urls = [target]
        inputs = []
        buttons = []
        newButtons = []

        #check every url currently found (new ones append at the end => constantly expanding)
        i = 0
        while i < len(urls):
            url = urls[i]
            i+=1
            try:
                browser.get(url)
            except:
                browser.back()
            
            #print(browser.get_cookies())
            #print(browser.page_source)
            
            #get the interesting elements from the page
            if browser.current_url.startswith(self.target):
                self.check_Inputs(url, inputs, browser)
                self.check_Links(urls, browser)
                newButtons = self.check_Buttons(buttons, browser)
            
                #press all new found buttons and check after each if there where changes
                j = 0
                while j < len(newButtons):
                    button = newButtons[j]
                    j+=1
                    try:
                        button.click()
                        self.check_Inputs(url, inputs, browser)
                        self.check_Links(urls, browser)
                        newButtons.append(self.check_Buttons(buttons, browser))
                    except Exception as e:
                        browser.back()
            
            #debug output of the results of the current page
            """
            print("-----------------------------------------------")
            print("Current Page result:", browser.current_url)
            for elem in urls:
                print("url:", elem)
            for elem in inputs:
                print("Input:", elem)   
            for elem in buttons:
                print("button:", elem)
            #"""

        #append found urls and inputs to class vars
        for url in urls:
            if url not in self.urls:
                self.urls.append(url)
        for inp in inputs:
            if inp not in self.inputs:
                self.inputs.append(inp)
        browser.quit()
        
    def check_Buttons(self, buttons, browser):
        """check current url for new buttons"""
        
        #find all "button" tags and inputs of type "submit" and check if they are known
        newButtons = browser.find_elements_by_tag_name("button")
        try:
            newButtons.append(browser.find_element_by_xpath("//input[@type='submit']"))
        except:
            True
        for button in newButtons:
            if button in buttons:
                newButtons.remove(button)
        
        #new buttons are appended to old ones and returned
        if newButtons:
            for button in newButtons:
                buttons.append(button)
        return newButtons
        
    
    def check_Inputs (self, url, inputs, browser):
        """check current url for new inputs"""
        
        newInputs = []
        
        #check all "input" tags for id or name attribute and append new ones to newInputs
        allInputs = []
        allInputs = browser.find_elements_by_tag_name("input")
        for inp in allInputs:
            if inp.get_attribute('id'):
                if url+"?"+inp.get_attribute('id') not in inputs:
                    #print("Input(id): ", url+ "?"+inp.get_attribute('id'))
                    newInputs.append(url+ "?"+inp.get_attribute('id'))
            elif inp.get_attribute('name'):
                if url+"?"+inp.get_attribute('name') not in inputs:
                    #print("Input(name): ", url+ "?"+inp.get_attribute('name'))
                    newInputs.append(url+ "?"+inp.get_attribute('name'))   
                        
        #append the new Inputs to the old ones and return the new
        if newInputs:
            for inp in newInputs:
                inputs.append(inp)
        #return newInputs
        
    def check_Links(self, urls, browser):
        """check current url for new urls"""
    
        newUrls = []
        
        #check all "a"-tags for hrefs
        links = browser.find_elements_by_tag_name("a")
        for link in links:
            if link.get_attribute('href'):
                linkPrep = link.get_attribute('href').replace("localhost", "127.0.0.1")
                if linkPrep.startswith("./"):
                    linkPrep = self.target + "/" + linkPrep[-2:]
                if linkPrep.startswith("/"):
                    linkPrep = self.target + "/" + linkPrep[-1:]  
                if linkPrep.startswith(self.target):
                    if linkPrep not in urls:
                        try: 
                            if requests.get(url = linkPrep):
                                #print("Link: ", linkPrep)
                                newUrls.append(linkPrep)
                        except Exception as e:
                            True
        
        #check current URL (can be changed by buttons)
        currentURL = browser.current_url
        if currentURL not in urls:
            if "?" not in currentURL:
                newUrls.append(currentURL)
        
        #append the new urls to the older ones and return them 
        if newUrls:
            for url in newUrls:
                urls.append(url)
        #return newUrls

    
    def get_urls(self):
        for url in self.urls:
            url = url.replace("localhost", "127.0.0.1")
        return self.urls
        
    def get_inputs(self):
        for inp in self.inputs:
            inp = inp.replace("localhost", "127.0.0.1")
        return self.inputs
        
    #def get_outputs(self):
        #return self.outputs
        
        