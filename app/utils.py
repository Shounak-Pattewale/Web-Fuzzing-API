import subprocess
import json
import requests
from bs4 import BeautifulSoup

class FuzzingError(Exception):
    """Custom exception for fuzzing errors."""
    pass

def add_fuzz_url(target_url):
    if "FUZZ" not in target_url:
        if target_url[-1] != "/":
            target_url = target_url + "/FUZZ"
        else:
            target_url = target_url + "FUZZ"
    return target_url

def build_command_with_options(base_command, cookies=None, headers=None):
    command = base_command.copy()
    # Add cookies
    if cookies:
        for cookie in cookies:
            command.extend(["-b", cookie])
    # Add headers
    if headers:
        for header in headers:
            command.extend(["-H", header])
    return command

def run_wfuzz_command(command):
    try:
        # Execute the command using subprocess
        result = subprocess.run(command, capture_output=True)
        # Decode the standard output and error
        output = result.stdout
        error_output = result.stderr
        # Check if there was an error in executing the command
        if result.returncode != 0:
            raise FuzzingError(f"Command failed: {error_output}")
        # Check if the output is empty
        if not output:
            raise FuzzingError("No output returned from the fuzzer")
        # Try to parse the JSON output
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            raise FuzzingError(f"Failed to decode JSON: {output}")
    except Exception as e:
        return {"error": str(e)}

def fuzz_common_directories(url, wordlist, cookies=None, headers=None):
    try:
        base_command = ["wfuzz", "-o", "json", "-w", f"{wordlist}", "--hc", "404"]
        command = build_command_with_options(base_command, cookies, headers)
        command.append(url)
        return run_wfuzz_command(command)

    except requests.RequestException as e:
        raise FuzzingError(f"Request error: {str(e)}")
    except Exception as e:
        raise FuzzingError(str(e))

def fuzz_common_files(url, wordlist, cookies=None, headers=None):
    try:
        base_command = ["wfuzz", "-o", "json", "-w", f"{wordlist}", "--hc", "404"]
        command = build_command_with_options(base_command, cookies, headers)
        command.append(url)
        return run_wfuzz_command(command)
    
    except requests.RequestException as e:
        raise FuzzingError(f"Request error: {str(e)}")
    except Exception as e:
        raise FuzzingError(str(e))

def fuzz_parameters_in_urls(url, range_values, cookies=None, headers=None):
    try:
        base_command = ["wfuzz", "-o", "json", "-z", f"range,{range_values}", "--hl", "97", "--hc", "404"]
        command = build_command_with_options(base_command, cookies, headers)
        command.append(url)
        return run_wfuzz_command(command)
    except requests.RequestException as e:
        raise FuzzingError(f"Request error: {str(e)}")
    except Exception as e:
        raise FuzzingError(str(e))

def fuzz_post_requests(url, data, wordlist, cookies=None, headers=None):
    try:
        base_command = ["wfuzz", "-o", "json", "-z", f"file,{wordlist}", "-d", f"{data}", "--hc", "302"]
        command = build_command_with_options(base_command, cookies, headers)
        command.append(url)
        return run_wfuzz_command(command)
    except requests.RequestException as e:
        raise FuzzingError(f"Request error: {str(e)}")
    except Exception as e:
        raise FuzzingError(str(e))

def fuzz_recursion(url, wordlist, recursion_depth, cookies=None, headers=None):
    try:
        base_command = ["wfuzz", "-o", "json", "-z", f"file,{wordlist}", "-R", f"{recursion_depth}", "--hc", "404"]
        command = build_command_with_options(base_command, cookies, headers)
        command.append(url)
        return run_wfuzz_command(command)
    except requests.RequestException as e:
        raise FuzzingError(f"Request error: {str(e)}")
    except Exception as e:
        raise FuzzingError(str(e))

def fuzz_http_verbs(url, wordlist, cookies=None, headers=None):
    try:
        base_command = ["wfuzz", "-o", "json", "-z", f"file,{wordlist}", "-X", "FUZZ", "--hc", "405"]
        command = build_command_with_options(base_command, cookies, headers)
        command.append(url)
        return run_wfuzz_command(command)
    except requests.RequestException as e:
        raise FuzzingError(f"Request error: {str(e)}")
    except Exception as e:
        raise FuzzingError(str(e))

def get_forms(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        forms = soup.find_all('form')
        form_details = []

        for form in forms:
            action = form.get('action')
            method = form.get('method', 'get').lower()
            inputs = [(input_tag.get('name'), input_tag.get('type', 'text')) for input_tag in form.find_all('input')]
            form_details.append({
                'action': action,
                'method': method,
                'inputs': inputs
            })

        return form_details

    except requests.RequestException as e:
        raise FuzzingError(f"Request error: {str(e)}")
    except Exception as e:
        raise FuzzingError(str(e))

def fuzz_form(url, wordlist, cookies=None, headers=None):
    try:
        forms = get_forms(url)
        if "error" in forms:
            return forms

        results = []
        base_url = url.rsplit('/', 1)[0]  # Base URL without the page

        for form in forms:
            action = form['action']
            method = form['method']
            inputs = form['inputs']

            # Construct the full target URL
            if action.startswith('/'):
                target_url = f"{base_url}{action}"
            elif not action.startswith('http'):
                target_url = f"{base_url}/{action}"
            else:
                target_url = action

            # Determine the fuzzing payloads for GET or POST
            if method == 'get':
                fuzzing_url = f"{target_url}?"
                fuzzing_url += '&'.join([f"{name}=FUZZ" for name, _ in inputs if name])
                url = fuzzing_url
                command = ["wfuzz", "-o", "json", "-w", f"{wordlist}", "--hc", "302"]
            elif method == 'post':
                fuzzing_data = '&'.join([f"{name}=FUZZ" for name, _ in inputs if name])
                command = ["wfuzz", "-o", "json", "-w", f"{wordlist}", "-d", fuzzing_data, "--hc", "302"]
                url = target_url

            command = build_command_with_options(command, cookies, headers)
            command.append(url)
            result = run_wfuzz_command(command)
            results.append({
                "target_url": target_url,
                "method": method,
                "result": result
            })

        return results
    
    except requests.RequestException as e:
        raise FuzzingError(f"Request error: {str(e)}")
    except Exception as e:
        raise FuzzingError(str(e))