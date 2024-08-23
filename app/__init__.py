import logging
from flask import Flask, request, jsonify, abort, render_template_string
import os
import markdown
from . import const
from . import utils

def create_app():
    # Configure the logging
    # Logs will be saved to 'fuzzer.log', with the log level set to DEBUG, 
    # which means all levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) will be logged.
    logging.basicConfig(filename=const.LOG_FILE_NAME, level=logging.DEBUG, 
                        format='%(asctime)s %(levelname)s: %(message)s')
    
    # Create Flask application instance
    app = Flask(__name__)

    @app.route('/')
    def index():
        # Log when the health check endpoint is called
        logging.info("Health check endpoint called")
        # Return a simple JSON response indicating the app is healthy
        return jsonify({"status": "healthy"})

    @app.route('/api_documentation', methods=['GET'])
    def api_document():
        try:
            # Log when the API documentation endpoint is accessed
            logging.info("API documentation endpoint called")
            # Path to the Markdown file containing the API documentation
            md_file_path = os.path.join(os.path.dirname(__file__), 'docs', 'api_documentation.md')

            # Read the Markdown file content
            with open(md_file_path, 'r') as md_file:
                md_content = md_file.read()

            # Convert the Markdown content to HTML
            html_content = markdown.markdown(md_content)

            # Render the HTML content using Flask's render_template_string
            return render_template_string(html_content)
        except FileNotFoundError:
            # Log an error if the Markdown file is not found
            logging.error("API documentation file not found")
            # Return a 404 error if the file is not found
            abort(404, description="API documentation not found.")
        except Exception as e:
            # Log any other exceptions that occur
            logging.error(f"Error occurred in API documentation endpoint: {e}")
            # Return a 500 error with the exception message
            abort(500, description=str(e))

    @app.route('/fuzz_common_directories', methods=['POST'])
    def fuzz_common_directories():
        try:
            # Log when the fuzz common directories endpoint is accessed
            logging.info("Fuzz common directories endpoint called")
            # Get target URL from the request, use a default if not provided
            target_url = request.json.get('url', const.DEFAULT_URL)
            target_url = utils.add_fuzz_url(target_url)
            # Get wordlist, cookies, and headers from the request
            wordlist = request.json.get('wordlist', const.DEFAULT_WORDLIST)
            cookies = request.json.get("cookies", None)
            headers = request.json.get("headers", None)
            # Call the utility function to perform directory fuzzing
            output = utils.fuzz_common_directories(target_url, wordlist, cookies, headers)
            # Return the fuzzing result as a JSON response
            return jsonify(output)
        except Exception as e:
            # Log any exceptions that occur
            logging.error(f"Error occurred in fuzz_common_directories: {e}")
            # Return a 500 error with the exception message
            abort(500, description=str(e))

    @app.route('/fuzz_common_files', methods=['POST'])
    def fuzz_common_files():
        try:
            # Log when the fuzz common files endpoint is accessed
            logging.info("Fuzz common files endpoint called")
            # Get target URL from the request, use a default if not provided
            target_url = request.json.get('url', const.DEFAULT_URL)
            target_url = utils.add_fuzz_url(target_url)
            # Get wordlist, cookies, and headers from the request
            wordlist = request.json.get('wordlist', const.DEFAULT_WORDLIST)
            cookies = request.json.get("cookies", None)
            headers = request.json.get("headers", None)
            # Call the utility function to perform file fuzzing
            output = utils.fuzz_common_files(target_url, wordlist, cookies, headers)
            # Return the fuzzing result as a JSON response
            return jsonify(output)
        except Exception as e:
            # Log any exceptions that occur
            logging.error(f"Error occurred in fuzz_common_files: {e}")
            # Return a 500 error with the exception message
            abort(500, description=str(e))

    @app.route('/fuzz_parameters_in_urls', methods=['POST'])
    def fuzz_parameters_in_urls():
        try:
            # Log when the fuzz parameters in URLs endpoint is accessed
            logging.info("Fuzz parameters in URLs endpoint called")
            # Get target URL and range values from the request, use defaults if not provided
            target_url = request.json.get('url', const.DEFAULT_URL)
            range_values = request.json.get('range', const.DEFAULT_RANGE)
            cookies = request.json.get("cookies", None)
            headers = request.json.get("headers", None)
            # Call the utility function to fuzz parameters in the URL
            output = utils.fuzz_parameters_in_urls(target_url, range_values, cookies, headers)
            # Return the fuzzing result as a JSON response
            return jsonify(output)
        except Exception as e:
            # Log any exceptions that occur
            logging.error(f"Error occurred in fuzz_parameters_in_urls: {e}")
            # Return a 500 error with the exception message
            abort(500, description=str(e))

    @app.route('/fuzz_post_requests', methods=['POST'])
    def fuzz_post_requests():
        try:
            # Log when the fuzz POST requests endpoint is accessed
            logging.info("Fuzz POST requests endpoint called")
            # Get target URL, data, wordlist, cookies, and headers from the request, use defaults if not provided
            target_url = request.json.get('url', const.DEFAULT_URL)
            data = request.json.get('data', const.DEFAULT_POST_DATA)
            wordlist = request.json.get('wordlist', const.DEFAULT_WORDLIST)
            cookies = request.json.get("cookies", None)
            headers = request.json.get("headers", None)
            # Call the utility function to fuzz POST requests
            output = utils.fuzz_post_requests(target_url, data, wordlist, cookies, headers)
            # Return the fuzzing result as a JSON response
            return jsonify(output)
        except Exception as e:
            # Log any exceptions that occur
            logging.error(f"Error occurred in fuzz_post_requests: {e}")
            # Return a 500 error with the exception message
            abort(500, description=str(e))

    @app.route('/fuzz_recursion', methods=['POST'])
    def fuzz_recursion():
        try:
            # Log when the fuzz recursion endpoint is accessed
            logging.info("Fuzz recursion endpoint called")
            # Get target URL, wordlist, recursion depth, cookies, and headers from the request, use defaults if not provided
            target_url = request.json.get('url', const.DEFAULT_URL)
            target_url = utils.add_fuzz_url(target_url)
            wordlist = request.json.get('wordlist', const.DEFAULT_RECURSION_WORDLIST)
            recursion_depth = request.json.get('recursion_depth', const.DEFAULT_RECURSION_DEPTH)
            cookies = request.json.get("cookies", None)
            headers = request.json.get("headers", None)
            # Call the utility function to perform recursive fuzzing
            output = utils.fuzz_recursion(target_url, wordlist, recursion_depth, cookies, headers)
            # Return the fuzzing result as a JSON response
            return jsonify(output)
        except Exception as e:
            # Log any exceptions that occur
            logging.error(f"Error occurred in fuzz_recursion: {e}")
            # Return a 500 error with the exception message
            abort(500, description=str(e))

    @app.route('/fuzz_http_verbs', methods=['POST'])
    def fuzz_http_verbs():
        try:
            # Log when the fuzz HTTP verbs endpoint is accessed
            logging.info("Fuzz HTTP verbs endpoint called")
            # Get target URL, wordlist, cookies, and headers from the request, use defaults if not provided
            target_url = request.json.get('url', const.DEFAULT_URL)
            wordlist = request.json.get('wordlist', const.DEFAULT_HTTP_VERBS_WORDLIST)
            cookies = request.json.get('cookies', [])
            headers = request.json.get('headers', [])
            # Call the utility function to fuzz HTTP verbs
            output = utils.fuzz_http_verbs(target_url, wordlist, cookies, headers)
            # Return the fuzzing result as a JSON response
            return jsonify(output)
        except Exception as e:
            # Log any exceptions that occur
            logging.error(f"Error occurred in fuzz_http_verbs: {e}")
            # Return a 500 error with the exception message
            abort(500, description=str(e))

    @app.route('/fuzz_forms', methods=['POST'])
    def fuzz_forms():
        try:
            # Log when the fuzz forms endpoint is accessed
            logging.info("Fuzz forms endpoint called")
            # Get target URL, wordlist, cookies, and headers from the request, use defaults if not provided
            target_url = request.json.get('url', const.DEFAULT_URL)
            wordlist = request.json.get('wordlist', const.DEFAULT_WORDLIST)
            cookies = request.json.get('cookies', [])
            headers = request.json.get('headers', [])
            # Call the utility function to fuzz forms
            output = utils.fuzz_form(target_url, wordlist, cookies, headers)
            # Return the fuzzing result as a JSON response
            return jsonify(output)
        except Exception as e:
            # Log any exceptions that occur
            logging.error(f"Error occurred in fuzz_forms: {e}")
            # Return a 500 error with the exception message
            abort(500, description=str(e))

    @app.route('/automated_fuzzing', methods=['POST'])
    def automated_fuzzing():
        try:
            # Log when the automated fuzzing endpoint is accessed
            logging.info("Automated fuzzing endpoint called")
            # Parse input from the user
            target_url = request.json.get('url', const.DEFAULT_URL)
            target_url = utils.add_fuzz_url(target_url)
            wordlist = const.DEFAULT_WORDLIST
            dir_wordlist = request.json.get('dir_wordlist', const.DEFAULT_WORDLIST)
            file_wordlist = request.json.get('file_wordlist', const.DEFAULT_WORDLIST)
            injection_type = request.json.get('injection_type', 'word')  # 'word', 'sql', 'xml', 'xss'
            cookies = request.json.get('cookies', [])
            headers = request.json.get('headers', [])
            
            # Run directory and file fuzzing
            directory_results = utils.fuzz_common_directories(target_url, dir_wordlist, cookies, headers)
            file_results = utils.fuzz_common_files(utils.add_fuzz_url(target_url), file_wordlist, cookies, headers)

            # Collect successful URLs
            successful_urls = []
            for result in directory_results:
                if result['code'] not in [404, 500]:
                    successful_urls.append(result['url'])
            for result in file_results:
                if result['code'] not in [404, 500]:
                    successful_urls.append(result['url'])

            # Remove duplicates by converting to set
            successful_urls = list(set(successful_urls))

            # Selecting wordlist file based on injection type
            if injection_type == 'sql':
                wordlist = const.DEFAULT_SQL_WORDLIST
            elif injection_type == 'xml':
                wordlist = const.DEFAULT_XML_WORDLIST
            elif injection_type == 'xss':
                wordlist = const.DEFAULT_XSS_WORDLIST
            else:  # Default to word injection
                wordlist = const.DEFAULT_WORDLIST

            # Perform form fuzzing on successful URLs
            form_results = []
            for url in successful_urls:
                form_result = utils.fuzz_form(url, wordlist, cookies, headers)
                if form_result != []:
                    form_results.append(form_result)
            
            # Compile the report
            report = {
                "initial_fuzzing": {
                    "directories": directory_results,
                    "files": file_results,
                },
                "successful_urls": successful_urls,
                f"form_{injection_type}_injection": form_results
            }

            # Return the full fuzzing report as a JSON response
            return jsonify(report)

        except Exception as e:
            # Log any exceptions that occur
            logging.error(f"Error occurred in automated_fuzzing: {e}")
            # Return a 500 error with the exception message
            abort(500, description=str(e))

    # Return the configured Flask app
    return app
