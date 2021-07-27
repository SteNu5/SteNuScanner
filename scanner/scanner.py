from crawler import crawler
from sqlinjection import sqlinjection
from xss import xss, xss_dom
from pathtraversal import pathtraversal
from cmdinjection import cmdinjection
from phpinjection import phpinjection

import requests
from datetime import datetime

#selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException

class scanner():

    urls = []
    inputs = []
    #outputs = {}
    vulns = []
    target = ""
    requestNr = 0
    
    def __init__(self, target, level=1, crawlChoice=1, seleniumChoice=0):
        
        """Firstly the reachable urls will be crawled and inputs on the pages gathered. After that the attacks commence"""
        
        print("Start scanning page ", target)
        self.target = target
        self.target = self.target.replace("localhost", "127.0.0.1")
        #crawling
        crawlr = crawler(self.target, crawlChoice)
        self.urls = crawlr.get_urls()
        self.inputs = crawlr.get_inputs()
        #self.outputs = crawlr.get_outputs()
        print("\n++++++++++++++++++++++++++++++++++++++")
        for url in self.urls:
            print("URL: ", url)
        print("")
        for inp in self.inputs:
            print("Input: ", inp)
        """
        print("")
        for out in self.outputs:
            print("Output: ", out + ":", self.outputs[out])
        """
        print("\n\n++++++++++++++++++++++++++++++++++++++")
        print("start attacking:")
        
        #attacking
        self.attack(level, seleniumChoice)
        
        print("\n\n++++++++++++++++++++++++++++++++++++++")
        print("Requests made: ", self.requestNr)
        print("Attack result: ")
        resultfile = open("results/bench_scan_level_"+ str(level) +"_"+ datetime.now().strftime("%d-%m-%Y_%H-%M"), "w")
        resultfile.write("Target: " + self.target + "\n")
        resultfile.write("Date: " + datetime.now().strftime("%d-%m-%Y %H:%M") + "\n\n")
        resultfile.write("findings: \n")
        for vuln in self.vulns:
            if isinstance(vuln, list):
                for elem in vuln:
                    resultfile.write(elem[0] + "\n")
        resultfile.write("\n\nDetails: \n")
        for vuln in self.vulns:
            if isinstance(vuln, list):
                for elem in vuln:
                    print(elem[0])
                    resultfile.write(elem[0] + "\n")
                    resultfile.write("-----------------------------------\n")
                    resultfile.write("request answer:\n")
                    if len(elem) > 1:
                        #print("Elem1", elem[1])
                        resultfile.write(elem[1] + "\n")
                    resultfile.write("-----------------------------------------------------------------------------\n")
            else:
                print(vuln)
        resultfile.close()

    def attack (self, level=1, sel=0):
        """
        here the attacks are started:
            level 1: partly no precautions to prevent false positives
            level 2: vulnerablility only accepted if there is some kind of evidence 
        additionally the attacks can be executed with selenium
            sel 1: no selenium
            sel 2: firefox
            sel 3: chrome
            sel 4: firefox headless
            sel 5: chrome headless
        """
        
        browser = ""
        if sel > 1:
            try:
                if sel == 2 or sel == 4:
                    options = Options()
                    if sel == 4:
                        options.headless = True
                    browser = webdriver.Firefox(options=options)
                else:
                    options = webdriver.ChromeOptions()
                    if sel == 5:
                        options.headless = True
                    browser = webdriver.Chrome(options=options)
                    
                browser.set_page_load_timeout(10)
            except:
                print("Failed to initialize the necessary browser")
                exit()
        
        #scanning for SQL Injections
        #"""
        for inp in self.inputs:
            if sel == 1:
                result = sqlinjection(inp, self, level)
            else:
                result = sqlinjection(inp, self, level, True, browser)
            if result:
                self.vulns.append(result)
        
        #"""
        #"""
        
        #scanning for CMD Injection
        for inp in self.inputs:
            if sel == 1:
                result = cmdinjection(inp, self, level)
            else:
                result = cmdinjection(inp, self, level, True, browser)
            if result:
                self.vulns.append(result)
        
        #""" 
        #"""
        #scanning for PHP Injection
        for inp in self.inputs:
            if sel == 1:
                result = phpinjection(inp, self, level)
            else:
                result = phpinjection(inp, self, level, True, browser)
            if result:
                self.vulns.append(result)
        #""" 
        
        #"""
        
        #scanning for Path Traversal/Local File Inclusion
        for inp in self.inputs:
            if sel == 1:
                result = pathtraversal(inp, self.target, self, level)
            else:
                result = pathtraversal(inp, self.target, self, level, True, browser)
            if result:
                self.vulns.append(result)
        
        #""" 
        
        #"""
        #scanning for XSS(Permanent)
        for inp in self.inputs:
            if sel == 1:
                result = xss(inp, self, level)
            else:
                result = xss(inp, self, level, True, browser)
            if result:
                self.vulns.append(result)
        #"""
        
        if sel > 1:
            browser.quit()
        
    
    def request(self, req, tout = 10):
        """handles the sending of the requests to the webserver"""
        try:
            res = requests.get(url = req, timeout=tout, verify=False)
        except requests.exceptions.Timeout as e:
            res = []
        self.requestNr += 1
        print("Request Nr", self.requestNr ,":", req)
        """
        if res:
            print("Request Nr", self.requestNr ,": ", res.text)
        #"""
        if isinstance(res, list):
            return res
        else:
            return res.text
        
    def requestSel(self, inp, text, browser, alertAvoidance = 1):
        """handles the sending of the requests to the webserver"""
        #get the input and fill it
        try:
            #get page url and input id/name
            urlparts = inp.split("?")
            #navigate to page url
            #print("-----------------------------")
            #print("new Request", inp)
            browser.get(urlparts[0])
            #check for alerts
            if alertAvoidance:
                self.closeAlerts(browser)
            #get the target input
            target = ""
            try:
                target = browser.find_element_by_id(urlparts[1])
            except Exception as e:
                try:
                    target = browser.find_element_by_name(urlparts[1])
                except:
                    pass
            if target == "":
                print("Input not found:", urlparts[0], urlparts[1])
                res = []
            else:
                #write the given text to target input
                target.send_keys(text)
                target.send_keys(Keys.ENTER)
                #get the page source for inspection of the answer
                #input("Press next")
                #check for alerts
                if alertAvoidance:
                    self.closeAlerts(browser)
                res = browser.page_source
        except UnexpectedAlertPresentException:
            print("Alert interrupted execution")
            #browser.execute_script("window.stop();")
            browser.get(self.target)
            res = []
        except Exception as e:
            print("Exception:", e, ": ", type(e))
            browser.execute_script("window.stop();")
            browser.get(self.target)
            res = []
        
        #manage the request number and return the result (res)
        self.requestNr += 1
        print("Request Nr", self.requestNr ,":", inp + "=" + text)
        """
        if res:
            print("Request Nr", self.requestNr ,": ", res)
        #"""
        return res
        
    def closeAlerts (self, browser):
        """closes all alerts on the page"""
        
        running = True
        while running:
        
            try:
                WebDriverWait(browser, 1).until(EC.alert_is_present())
                alert = browser.switch_to.alert
                alert.dismiss()
                #print("alert dismissed")
                running = True
            except TimeoutException:
                #print("no alerts")
                running = False
            
        


#starting point of the scanner
url = input("Enter URL to scan: \n")
level = input("Enter the attack level (1=more false positives, 2=try to avoid false positives (default), \n3=2 with additional time-based SQL-Injection-Attacks (Can crash websites)):\n")
crawl = input("Enter the crawler (1=html (default), 2=selenium(firefox), 3=html+selenium(firefox), 4=selenium(chrome), \n5=selenium(firefox) windowless, 6=selenium(chrome) windowless:\n")
seleniumChoice = input("Enter the attack methode (1=python requests (default), 2= firefox selenium , \n3 = chrome selenium , 4 = firefox selenium headless, 5 = chrome selenium headless): \n")

#check if it is an url
if url == "":
    url = "http://localhost:8000"
else:
    if not url.startswith("http://"):
        if not url.startswith("https://"):
            print("Your url has to start with 'http'")
            exit()
    
#check the given level     
if level == "":
    level = 2
else:
    if level != "1" and level != "2":
        print("There are only two levels to choose (1 or 2)")
        exit()
        
#check the given level     
if crawl == "":
    crawl = 1
else:
    if crawl != "1" and crawl != "2" and crawl != "3" and crawl != "4" and crawl != "5" and crawl != "6":
        print("You have to choose a crawler option (1, 2, 3, 4, 5 or 6)")
        exit()
        
if seleniumChoice == "":
    seleniumChoice = 1
else:
    if seleniumChoice != "1" and seleniumChoice != "2"  and seleniumChoice != "3"  and seleniumChoice != "4" and seleniumChoice != "5":
        print("You have to choose a attack methode option (0, 1, 2, 3, 4 or 5)")
        exit()
        
level = int(level)
crawl = int(crawl)
seleniumChoice = int(seleniumChoice)

#start scanner    
scanner(url, level, crawl, seleniumChoice)