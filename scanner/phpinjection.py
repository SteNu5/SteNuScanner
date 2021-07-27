def phpinjection(inp, scanner, level = 1, sel = False, browser = 0):
    """Checks the given input for the possibility of php injection"""
    
    vulns = []
                    
    #------------------------------------------------------------------------------------------------------------------------
    #Check if the injection of the echo command is possible
    text = "1;echo testtesttest;"
    req = inp + "=" + text
    if not sel:
        res = scanner.request(req)
    else:
        res = scanner.requestSel(inp, text, browser, 1)
    if res:
        if "testtesttest" in res:
            if level > 1:
                if not "1;echo testtesttest;" in res:
                    vuln = []
                    vuln.append("Possible PHP Injection: "+ req + "; Evidence: 'testtesttest' found in response but not the injection command" )
                    vuln.append(res)
                    vulns.append(vuln)
            else:
                vuln = []
                vuln.append("Possible PHP Injection: "+ req + "; Evidence: 'testtesttest' found in response" )
                vuln.append(res)
                vulns.append(vuln)
            
            
    return vulns