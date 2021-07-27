def cmdinjection(inp, scanner, level = 1, sel = False, browser = 0):
    """Checks the given input for the possibility of command injection"""
    
    vulns = []
    
    #------------------------------------------------------------------------------------------------------------------------
    #Check if the injection of the echo command is possible
    text = "echo kasodjfka"
    req = inp + "=" + text
    if not sel:
        res = scanner.request(req)
    else:
        res = scanner.requestSel(inp, text, browser, 1)
    if res:
        if "kasodjfka" in res:
            if level > 1:
                if not "echo kasodjfka" in res:
                    vuln = []
                    vuln.append("Possible CMD Injection: "+ req + "; Evidence: 'kasodjfka' found in response but not 'echo kasodjfka'" )
                    vuln.append(res)
                    vulns.append(vuln)
            else:
                vuln = []
                vuln.append("Possible CMD Injection: "+ req + "; Evidence: 'kasodjfka' found in response" )
                vuln.append(res)
                vulns.append(vuln)
            
            
    return vulns