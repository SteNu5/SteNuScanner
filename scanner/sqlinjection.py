from datetime import datetime

#sql injection
def sqlinjection(inp, scanner, level = 1, sel = False, browser = 0):
    """this function tests the given input for sql injections"""
    
    vulns = []
    
    #------------------------------------------------------------------------------------------------------------------------
    #Check if the input can be made true without result returned (# for termination of query)
    text = "'; set @test = 'ksdjkfl'; select @test; #"
    req = inp + "=" + text
    if not sel:
        res = scanner.request(req)
    else:
        res = scanner.requestSel(inp, text, browser)
    if res:
        if "ksdjkfl" in res:
            if level > 1:
                if not "'; set @test = 'ksdjkfl'; select @test; #" in res:
                    vuln = []
                    vuln.append("Possible SQL injection (Blind): "+ req + "; Evidence: The Input 'ksdjkfl' is found in the response without it´s injection string")
                    vuln.append(res)
                    vulns.append(vuln)
            else:
                vuln = []
                vuln.append("Possible SQL injection (Blind): "+ req + "; Evidence: The Input 'ksdjkfl' is found in the response")
                vuln.append(res)
                vulns.append(vuln)
        if "SQL" in res and " error " in res:
            vuln = []
            vuln.append("Possible SQL injection (Error): "+ req + "; Evidence: The words SQL and error are in the answer")
            vuln.append(res)
            vulns.append(vuln)
    elif level == 1:
        vuln = []
        vuln.append("Possible SQL injection (Error): "+ req + "; Evidence: no request answer received")
        vuln.append(res)
        vulns.append(vuln)

    #------------------------------------------------------------------------------------------------------------------------
    #Check if the input can be made true without result returned (# for termination of query)
    text = "'+or+1%3D1%23'"
    req = inp + "=" + text
    if not sel:
        res = scanner.request(req)
    else:
        res = scanner.requestSel(inp, text, browser)
    if res:
        if "' or 1=1#" not in res:
            if sel:
                negResult = scanner.requestSel(inp, "'+or+1%3D2%23'", browser)
            else:
                negResult = scanner.request(inp + "=" + "'+or+1%3D2%23'")
            if negResult != res:
                vuln = []
                vuln.append("Possible SQL injection (Blind): "+ req + "; Evidence: The Input is not found in the response and check with negative '1=2' input differs")
                if isinstance(negResult, list):
                    vuln.append(res + "\n negative Result: \n")
                else:
                    vuln.append(res + "\n negative Result: \n" + negResult)
                vulns.append(vuln)
            elif level == 1:
                vuln = []
                vuln.append("Possible SQL injection (Blind): "+ req + "; Evidence: The Input is not found in the response")
                vulns.append(vuln)
        if "SQL" in res and " error " in res:
                vuln = []
                vuln.append("Possible SQL injection (Error): "+ req + "; Evidence: The words SQL and error are in the answer")
                vuln.append(res)
                vulns.append(vuln)
    elif level == 1:
        vuln = []
        vuln.append("Possible SQL injection (Error): "+ req + "; Evidence: no request answer received")
        vuln.append(res)
        vulns.append(vuln)
        
    text = '"+or+1%3D1%23"'
    req = inp + "=" + text
    if not sel:
        res = scanner.request(req)
    else:
        res = scanner.requestSel(inp, text, browser)
    if res:
        if '" or 1=1#"' not in res:
            if sel:
                negResult = scanner.requestSel(inp, '"+or+1%3D2%23"', browser)
            else:
                negResult = scanner.request(inp + "=" + '"+or+1%3D2%23"')
            if negResult != res:
                vuln = []
                vuln.append("Possible SQL injection (Blind): "+ req + "; Evidence: The Input is not found in the response and check with negative '1=2' input differs")
                if isinstance(negResult, list):
                    vuln.append(res + "\n negative Result: \n")
                else:
                    vuln.append(res + "\n negative Result: \n" + negResult)
                vulns.append(vuln)
            elif level == 1:
                vuln = []
                vuln.append("Possible SQL injection (Blind): "+ req + "; Evidence: The Input is not found in the response")
                vuln.append(res)
                vulns.append(vuln)
        if "SQL" in res and " error " in res:
                vuln = []
                vuln.append("Possible SQL injection (Error): "+ req + "; Evidence: The words SQL and error are in the answer")
                vuln.append(res)
                vulns.append(vuln)
    elif level == 1:
        vuln = []
        vuln.append("Possible SQL injection (Error): "+ req + "; Evidence: no request answer received")
        vuln.append(res)
        vulns.append(vuln)
    

    #------------------------------------------------------------------------------------------------------------------------
    #Check if the input can be made true without result returned (-- for termination of query)
    text = "'+or+1%3D1--'"
    req = inp + "=" + text
    if not sel:
        res = scanner.request(req)
    else:
        res = scanner.requestSel(inp, text, browser)
    if res:
        if "' or 1=1--'" not in res:
            if sel:
                negResult = scanner.requestSel(inp, "'+or+1%3D2--'", browser)
            else:
                negResult = scanner.request(inp + "=" + "'+or+1%3D2--'")
            if negResult != res:
                vuln = []
                vuln.append("Possible SQL injection (Blind): "+ req + "; Evidence: The Input is not found in the response and check with negative '1=2' input differs")
                if isinstance(negResult, list):
                    vuln.append(res + "\n negative Result: \n")
                else:
                    vuln.append(res + "\n negative Result: \n" + negResult)
                vulns.append(vuln)
            elif level == 1:
                vuln = []
                vuln.append("Possible SQL injection (Blind): "+ req + "; Evidence: The Input is not found in the response")
                vuln.append(res)
                vulns.append(vuln)
        if "SQL" in res and " error " in res:
                vuln = []
                vuln.append("Possible SQL injection (Error): "+ req + "; Evidence: The words SQL and error are in the answer")
                vuln.append(res)
                vulns.append(vuln)
    elif level == 1:
        vuln = []
        vuln.append("Possible SQL injection (Error): "+ req + "; Evidence: no request answer received")
        vuln.append(res)
        vulns.append(vuln)
        
    text = '"+or+1%3D1--"'
    req = inp + "=" + text 
    if not sel:
        res = scanner.request(req)
    else:
        res = scanner.requestSel(inp, text, browser)
    if res:
        if '" or 1=1--"' not in res:
            if sel:
                negResult = scanner.requestSel(inp, '"+or+1%3D2--"', browser)
            else:
                negResult = scanner.request(inp + "=" + '"+or+1%3D2--"')
            if negResult != res:
                vuln = []
                vuln.append("Possible SQL injection (Blind): "+ req + "; Evidence: The Input is not found in the response and check with negative '1=2' input differs")
                if isinstance(negResult, list):
                    vuln.append(res + "\n negative Result: \n")
                else:
                    vuln.append(res + "\n negative Result: \n" + negResult)
                vulns.append(vuln)
            elif level == 1:
                vuln = []
                vuln.append("Possible SQL injection (Blind): "+ req + "; Evidence: The Input is not found in the response")
                vuln.append(res)
                vulns.append(vuln)
        if "SQL" in res and " error " in res:
                vuln = []
                vuln.append("Possible SQL injection (Error): "+ req + "; Evidence: The words SQL and error are in the answer")
                vuln.append(res)
                vulns.append(vuln)
    elif level == 1:
        vuln = []
        vuln.append("Possible SQL injection (Error): "+ req + "; Evidence: no request answer received")
        vuln.append(res)
        vulns.append(vuln)
    
    if level == 3:
        #------------------------------------------------------------------------------------------------------------------------
        #Check if the response can be delayed = sleep was injected and executed (# for termination of query)
        text = "' or sleep(5)--"
        req = inp + "=" + text
        firstTime = datetime.now()
        if not sel:
            res = scanner.request(req)
        else:
            res = scanner.requestSel(inp, text, browser)
        if (datetime.now() - firstTime).total_seconds() > 4:
            vuln = []
            vuln.append("Time based SQL injection: " + req + "; Evidence: Response was successfully delayed more than 4 seconds")
            vulns.append(vuln)
            
        text = "' or sleep(5)#"
        req = inp + "=" + text
        firstTime = datetime.now()
        if not sel:
            res = scanner.request(req)
        else:
            res = scanner.requestSel(inp, text, browser)
        if (datetime.now() - firstTime).total_seconds() > 4:
            vuln = []
            vuln.append("Time based SQL injection: " + req + "; Evidence: Response was successfully delayed more than 4 seconds")
            vulns.append(vuln)
        
        text = '" or sleep(5)--'
        req = inp + "=" + text
        firstTime = datetime.now()
        if not sel:
            res = scanner.request(req)
        else:
            res = scanner.requestSel(inp, text, browser)
        if (datetime.now() - firstTime).total_seconds() > 4:
            vuln = []
            vuln.append("Time based SQL injection: " + req + "; Evidence: Response was successfully delayed more than 4 seconds")
            vulns.append(vuln)
            
        text = '" or sleep(5)#'
        req = inp + "=" + text
        firstTime = datetime.now()
        if not sel:
            res = scanner.request(req)
        else:
            res = scanner.requestSel(inp, text, browser)
        if (datetime.now() - firstTime).total_seconds() > 4:
            vuln = []
            vuln.append("Time based SQL injection: " + req + "; Evidence: Response was successfully delayed more than 4 seconds")
            vulns.append(vuln)
    
            
    return vulns