from bs4 import BeautifulSoup
res =  """<html>
    <head>
        <title>SQL-Injection</title>
    </head>
    <body>
        <h1> SQL-Injection </h1>
        <p>An SQL-Injection weakness is present on this site</p>

        <form>
            <label for="sql_insert">SQL data input:
                <input id="sql_insert" name="sql_insert">
            </label>
            <button type="submit" name="submit_insert" value="0">submit</button> <br>
            <label for="out_table_cont">Table content:
                <output id="out_table_cont">[(1, "' or 1=1#"), (2, '" or 1=1#'), (3, "' or 1=1--"), (4, '" or 1=1--'), (5, "' or sleep(5)--"), (6, "' or sleep(5)"), (7, '" or sleep(5)--'), (8, '" or sleep(5)'), (9, "<img src='x' onerror='alert(1)'>"), (10, '<script> alert(1) </script>')]</output>
            </label>
        </form>

        <p id="Exploit">The given Input is injected unchecked into the query "Select * from htmlInput where input = '-input-'"</p>
        <p id="Exploit">Possible exploit: '; drop table htmlInput; select * from htmlInput where input = ' </p>

        <form>
        <!-- Exploit input: '; drop table htmlInput; select * from htmlInput where input = ' -->
            <label for="sql">SQL where query input:
                <input id="sql" name="sql">
            </label>
            <button type="submit" name="submit_where" value="0">submit</button> <br>
            <label for="out">Result:
                <output id="out">[(7, '" or sleep(5)--')]</output>
            </label>
        </form>

        <p id="Links">
            <a href="http://localhost:8000/index.html">This link leads to the homepage</a><br>
            <a href="http://localhost:8000/xss.html">Here you can try XSS-attacks</a><br>
            <a href="http://localhost:8000/fileinclusion.html">Here you can try File Inclusions</a><br>
            <a href="http://localhost:8000/cmdinjection.html">Here you can try command injections</a><br>
            <a href="http://localhost:8000/phpinjection.html">Here you can try PHP-Injections</a><br>
        </p>
    </body>"""
    
soup = BeautifulSoup(res, "html.parser")
result = soup.find("img", onerror="alert(1)")
print(result)
if "<img src='x' onerror='alert(1)'>" in res:
    print("Found")

if "html" in res:
    print("Found html")
    
    
test = """ <html>
    <body>
        <h1> File Inclusion Attacks </h1>
        <p>This site contains the possibility for File Inclusions like Local and Remote File Inclusion</p>
        <p>The given file path will be executed by subprocess.run()</p>
        <p>Example input: test.py</p>

        <form>
            <label for="fi">File input:
                <input id="fi" name="fi"><button type="submit">submit</button><br>
            </label>
        </form>

        <p>File executed: echo kasodjfka; Result: kasodjfka
</p>

        <p id="Links">
            <a href="http://localhost:8000/index.html">This link leads to the homepage</a><br>
            <a href="http://localhost:8000/sqlinjection.html">Here you can try SQL-Injection</a><br>
            <a href="http://localhost:8000/xss.html">Here you can try XSS-attacks</a><br>
            <a href="http://localhost:8000/cmdinjection.html">Here you can try command injections</a><br>
            <a href="http://localhost:8000/phpinjection.html">Here you can try PHP-Injections</a><br>
        </p>
    </body>"""

if "kasodjfka" in test:
    print("kasodjfka")
    
res = []
if res == []:
    print("innen")
    
page = "kdöajfjkdsajölkfjsdkj"
if page.startswith("http://localhost:8000"):
    print("ahlkösjdkf")