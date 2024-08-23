# Advanced Fuzzing Techniques for Web Application Security: Developing an Automated Framework for Vulnerability Detection 

### Introduction
In the context of web application security, fuzzing becomes even more critical due to 
the dynamic nature of web environments and the wide array of inputs that can be 
exploited. Web applications are susceptible to various types of vulnerabilities, such as 
SQL injection, Cross-Site Scripting (XSS), and improper input validation, all of which 
can be effectively identified through fuzzing. 


The development of an automated fuzzing framework for web application security has 
been a process marked by both challenges and successes. Focused on improving the 
detection of vulnerabilities in web applications, this project has offered significant 
insights into the strengths and limitations of both theoretical approaches and practical 
applications in cybersecurity. 

### Project Requirements
* pip install -r requirements.txt

### dot-env(.env) Structure
LOG_FILE_NAME = "fuzzer.log"<br>
DEFAULT_URL = "some/url/FUZZ"<br>
DEFAULT_WORDLIST = "wordlist/test.txt"<br>
DEFAULT_SQL_WORDLIST = "wordlist/Injections/SQL.txt"<br>
DEFAULT_XSS_WORDLIST = "wordlist/Injections/XSS.txt"<br>
DEFAULT_XML_WORDLIST = "wordlist/Injections/XML.txt"<br>
DEFAULT_HTTP_VERBS_WORDLIST = "wordlist/general/http_methods.txt"<br>
DEFAULT_RECURSION_WORDLIST = "wordlist/general/test_recursion.txt"<br>
DEFAULT_RANGE = "0-10"<br>
DEFAULT_POST_DATA = "?FUZZ"<br>
DEFAULT_RECURSION_DEPTH = 1<br>

### Run Command
1. export FLASK_APP=run.py
2. export FLASK_ENV=development
3. flask run
