from bs4 import BeautifulSoup

#sql injection
def xss(inp, scanner, level = 1, sel = False, browser = 0):
    """this function tests the given input for xss-attacks"""
    
    vulns = []
    
    #------------------------------------------------------------------------------------------------------------------------
    #Check if alert disguised by img can be placed
    text = "<img src='x' onerror='alert(1)'>"
    req = inp + "=" + text
    if not sel:
        res = scanner.request(req)
    else:
        res = scanner.requestSel(inp, text, browser, 1)
    if res:
        soup = BeautifulSoup(res, "lxml")
        if soup.find("img", onerror="alert(1)"):
            vuln = []
            vuln.append("Possible XSS (Permanent): "+ req + "; Evidence: <img src='x' onerror='alert(1)'> found in response" )
            vuln.append(res)
            vulns.append(vuln)
        
    
    #------------------------------------------------------------------------------------------------------------------------
    #Check if script tag can be placed
    text = "<script> alert(1) </script>"
    req = inp + "=" + text
    if not sel:
        res = scanner.request(req)
    else:
        res = scanner.requestSel(inp, text, browser, 1)
    if res:
        soup = BeautifulSoup(res, "lxml")
        if soup.find("script", text=" alert(1) "):
            vuln = []
            vuln.append("Possible XSS (Permanent): "+ req + "; Evidence: <script> alert(1) </script> found in response" )
            vuln.append(res)
            vulns.append(vuln)
            
    return vulns
    
    
    
def xss_dom(page, scanner, level = 1):
    """Checking Browser for DOM based xss attacks"""
    
    vulns = []
    
    #------------------------------------------------------------------------------------------------------------------------
    #Check if alert disguised in url of the page is accepted
    text = "?default=default=<script>alert(document.cookie)</script>"
    req = page + text
    res = scanner.request(req)
    if res:
        vuln = []
        vuln.append("Possible XSS (DOM): "+ req + "; Evidence: URL accepted" )
        vuln.append(res)
        vulns.append(vuln)
        
    #------------------------------------------------------------------------------------------------------------------------
    #Check if alert disguised in url with '#' is accepted
    text = "#default=default=<script>alert(document.cookie)</script>"
    req = page + text
    res = scanner.request(req)
    if res:
        vuln = []
        vuln.append("Possible XSS (DOM): "+ req + "; Evidence: URL accepted" )
        vuln.append(res)
        vulns.append(vuln)
    
    return vulns