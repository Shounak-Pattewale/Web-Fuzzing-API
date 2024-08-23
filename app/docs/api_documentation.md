# Advanced Fuzzing Framework API Documentation

## Overview
This API provides a set of endpoints for fuzzing various aspects of web applications, including directories, HTTP methods, SQL injection, XSS, XML injection, and form-based fuzzing. The API is designed to help in vulnerability detection by automating the fuzzing process using `wfuzz`.

## Endpoints

### 1. `/` [GET]
- **Description**: Displays the API status.
- **Response**: Displays if the connection is healthy or not.

### 2. `/fuzz_common_directories` [POST]
- **Description**: Fuzzes common directories on the target URL.
- **Request Body**:
  - `url`: The base URL to fuzz (default: `"http://testphp.vulnweb.com/FUZZ"`).
  - `wordlist`: Path to the wordlist file to use for fuzzing (default: `"wordlist/general/common.txt"`).
  - `cookies`: Optional list of cookies to include in the request.
  - `headers`: Optional list of headers to include in the request.
- **Response**: JSON object with the fuzzing results.

### 3. `/fuzz_common_files` [POST]
- **Description**: Fuzzes for common files on the target URL. It attempts to find commonly used files like `.php`, `.asp`, etc., by appending them to the provided URL.
- **Request Body**:
  - `url`: The base URL to fuzz (default: `"http://testphp.vulnweb.com/FUZZ"`). The `FUZZ` placeholder in the URL is automatically adjusted to test for various file extensions.
  - `wordlist`: Path to the wordlist file to use for fuzzing (default: `"wordlist/general/common.txt"`).
  - `cookies`: Optional list of cookies to include in the request (e.g., `["sessionid=abc123"]`).
  - `headers`: Optional list of headers to include in the request (e.g., `["Authorization: Bearer token"]`).
- **Response**: JSON object with the fuzzing results.

### 4. `/fuzz_parameters_in_urls` [POST]
- **Description**: Fuzzes parameters in URLs by replacing values with fuzzed data. This method is useful for testing how parameters in the URL handle various inputs, such as ranges or specific patterns.
- **Request Body**:
  - `url`: The URL to fuzz with parameters (e.g., `"http://testphp.vulnweb.com/listproducts.php?cat=FUZZ"`).
  - `range`: Range of values to use in fuzzing (default: `"0-10"`).
  - `cookies`: Optional list of cookies to include in the request (e.g., `["sessionid=abc123"]`).
  - `headers`: Optional list of headers to include in the request (e.g., `["Authorization: Bearer token"]`).
- **Response**: JSON object with the fuzzing results.

### 5. `/fuzz_post_requests` [POST]
- **Description**: Fuzzes POST requests by submitting different payloads to the target URL. This is useful for testing how POST request parameters handle various inputs, potentially exposing vulnerabilities like SQL injection, XSS, etc.
- **Request Body**:
  - `url`: The URL to fuzz (e.g., `"http://testphp.vulnweb.com/userinfo.php"`).
  - `data`: The POST data to fuzz (default: `"uname=FUZZ&pass=FUZZ"`). The `FUZZ` placeholder is replaced with fuzzed data.
  - `wordlist`: Path to the wordlist file to use for fuzzing (default: `"wordlist/general/common.txt"`).
  - `cookies`: Optional list of cookies to include in the request (e.g., `["sessionid=abc123"]`).
  - `headers`: Optional list of headers to include in the request (e.g., `["Authorization: Bearer token"]`).
- **Response**: JSON object with the fuzzing results.

### 6. `/fuzz_recursion` [POST]
- **Description**: Performs recursive fuzzing, starting from a base set of directories and recursively fuzzing deeper into discovered directories. This is useful for finding hidden directories and files within a web application.
- **Request Body**:
  - `url`: The base URL to start fuzzing (default: `"http://testphp.vulnweb.com/FUZZ"`). The `FUZZ` placeholder is automatically adjusted.
  - `wordlist`: Path to the wordlist file to use for fuzzing (default: `"wordlist/general/test_recursion.txt"`).
  - `recursion_depth`: The depth of recursion for fuzzing (default: `1`).
  - `cookies`: Optional list of cookies to include in the request (e.g., `["sessionid=abc123"]`).
  - `headers`: Optional list of headers to include in the request (e.g., `["Authorization: Bearer token"]`).
- **Response**: JSON object with the fuzzing results.

### 7. `/fuzz_http_verbs` [POST]
- **Description**: Fuzzes different HTTP verbs on the target URL.
- **Request Body**:
  - `url`: The URL to fuzz with different HTTP verbs.
  - `wordlist`: Path to the wordlist for form fuzzing (default: `"wordlist/general/http_methods.txt"`).
  - `cookies`: Optional list of cookies to include in the request.
  - `headers`: Optional list of headers to include in the request.
- **Response**: JSON object with the fuzzing results.

### 8. `/fuzz_forms` [POST]
- **Description**: Automatically finds forms on the target URL, extracts method and action, and fuzzes the form fields.
- **Request Body**:
  - `url`: The URL to scrape and fuzz forms.
  - `wordlist`: Path to the wordlist for form fuzzing (default: `"wordlist/general/common.txt"`).
  - `cookies`: Optional list of cookies to include in the request.
  - `headers`: Optional list of headers to include in the request.
- **Response**: JSON object with the fuzzing results for each form found on the page.

### 9. `/automated_fuzzing` [POST]
- **Description**: Automates the entire fuzzing process by first running directory and file fuzzing, collecting successful URLs, and then performing form fuzzing based on the selected injection type. The final output is a detailed report of all fuzzing activities.
- **Request Body**:
  - `url`: The base URL to start fuzzing (default: `"http://testphp.vulnweb.com/FUZZ"`).
  - `dir_wordlist`: Path to the wordlist for directory fuzzing (default: `"wordlist/general/common.txt"`).
  - `file_wordlist`: Path to the wordlist for file fuzzing (default: `"wordlist/general/common.txt"`).
  - `injection_type`: Type of injection to perform during form fuzzing. Options are `'word'`, `'sql'`, `'xml'`, `'xss'` (default: `'word'`).
  - `cookies`: Optional list of cookies to include in the request.
  - `headers`: Optional list of headers to include in the request.
- **Response**: JSON object with a detailed report of all fuzzing activities, including initial directory and file fuzzing, successful URLs, and the results of form-based injection fuzzing.

### 10. `/api_documentation` [GET]
- **Description**: Displays the API documentation.
- **Response**: Plain text or Markdown content of the API documentation.
