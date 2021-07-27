from datetime import datetime

def pathtraversal(inp, target, scanner, level = 1, sel = False, browser = 0):
    """Checks the given input for the possibility of path traversal and local file inclusions"""
    
    vulns = []
    
    #------------------------------------------------------------------------------------------------------------------------
    #Check if the root file is accessible (Linux)
    text = "/etc/passwd"
    req = inp + "=" + text
    if not sel:
        res = scanner.request(req)
    else:
        res = scanner.requestSel(inp, text, browser)
    if res:
        if "root:x:0:0" in res:
            vuln = []
            vuln.append("Possible Path Traversal/Local File Inclusion: "+ req + "; Evidence: root:x:0:0 found in response" )
            vuln.append(res)
            vulns.append(vuln)
    elif res == []:
        vuln = []
        vuln.append("Possible Path Traversal/Local File Inclusion: "+ req + "; Evidence: timeout of the response probably because of the open file" )
        vulns.append(vuln)
        
           
    #------------------------------------------------------------------------------------------------------------------------
    #Check if the win.ini file on windows is callable (if the name is not in the response or the response time is higher than normal success is assumed)
    #With Selenium the response time is not usable because selenium answers directly (timeout detection still possible)
    text = "C:\windows\win.ini"
    req = inp + "=" + text
    firstTime = datetime.now()
    if not sel:
        res = scanner.request(req)
    else:
        res = scanner.requestSel(inp, text, browser)
    if res:
        if (datetime.now() - firstTime).total_seconds() >= 3:
            vuln = []
            vuln.append("Possible Path Traversal/Local File Inclusion: "+ req + "; Evidence: response delayed by more than 3 seconds because of the necessity of the user closing the opened file" )
            vuln.append(res)
            vulns.append(vuln)
    elif res == []:
        vuln = []
        vuln.append("Possible Path Traversal/Local File Inclusion: "+ req + "; Evidence: timeout of the response probably because of the open file" )
        vulns.append(vuln)
           
    #------------------------------------------------------------------------------------------------------------------------
    #Call the index page of the website and see if 'index.html' shows up in the response
    text = "index.html"
    req = inp + "=" + text
    if not sel:
        res = scanner.request(req)
    else:
        res = scanner.requestSel(inp, text, browser)
    if res:
        resPage = scanner.request(target+"/index.html")
        if resPage:
            if resPage in res and not resPage == res:
                vuln = []
                vuln.append("Possible Path Traversal/Local File Inclusion: "+ req + "; Evidence: index.html content found in response" )
                vuln.append(res)
                vulns.append(vuln)
        if level == 1:
            if "index.html" not in res:
                vuln = []
                vuln.append("Possible Path Traversal/Local File Inclusion: "+ req + "; Evidence: 'index.html' not found in response" )
                vuln.append(res)
                vulns.append(vuln)
           
    return vulns