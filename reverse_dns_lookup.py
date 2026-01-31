import socket

def get_ip_address():
    # Get user input
    hostname = input("Enter the website URL (e.g., google.com): ").strip()
    
    # Clean the input (remove http:// or https:// if present)
    if hostname.startswith("https://"):
        hostname = hostname[8:]
    elif hostname.startswith("http://"):
        hostname = hostname[7:]
    
    # Remove trailing slashes or paths
    hostname = hostname.split('/')[0]

    try:
        # Perform the DNS lookup
        ip_address = socket.gethostbyname(hostname)
        print(f"\n--- Results ---")
        print(f"Hostname: {hostname}")
        print(f"IP Address: {ip_address}")
    except socket.gaierror:
        print(f"Error: Could not resolve the hostname '{hostname}'. Check your spelling or internet connection.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    get_ip_address()
