# Advanced Fuzzing Techniques for Web Application Security: Developing an Automated Framework for Vulnerability Detection 

### Introduction
Web applications are increasingly being targeted by cyber-attacks that exploit vulnerabilities such as SQL injection, Cross-Site Scripting (XSS), and input validation problems. To counter this expanding threat, this study introduces a novel automated fuzzing tool particularly tailored to improve online application 
security. The proposed methodology systematically detects and 
examines a wide range of vulnerabilities using sophisticated fuzzing 
techniques, including intelligent input mutation, recursive testing, 
and HTTP verb fuzzing. It can make extensive API calls, which aids in 
the detection of vulnerabilities such as buffer overflows and type 
confusion. The framework is capable of handling large-scale 
applications and intends to make the process of detecting and 
correcting security problems easier for security experts and 
developers. To guarantee accessibility, the framework comes with a simple API and documentation. 

### Project Requirements
* pip install -r requirements.txt

### dot-env(.env) Structure
LOG_FILE_NAME = "fuzzer.log"<br>
DEFAULT_URL = "https://example.com/FUZZ"<br>
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
