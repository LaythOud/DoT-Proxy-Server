# DNS to DNS-over-TLS Proxy

This Python script provides a simple DNS to DNS-over-TLS proxy. It listens on a specified DNS port, accepts incoming DNS queries, and forwards them to a DNS-over-TLS server (e.g., Cloudflare) for enhanced privacy.

## Usage

1. Configure the proxy settings (proxy_port, target_host, target_port) in the script.

2. Run the script:

```bash 
    python3 dns_proxy.py
```

or with sudo if needed:

```bash 
    sudo python3 dns_proxy.py
```

3. Configure your machine to use the IP address of the machine running the script as its DNS server.

4. Test DNS queries using tools like `nslookup` or `dig`.

## Additional Notes

- Make sure to check and adjust firewall settings to allow incoming connections on the specified DNS port.

- **Error Handling**: Added try-except blocks to handle exceptions and log any errors that may occur during client handling or proxy setup.

- **Logging**: Introduced logging to provide informative messages and error logs. Adjust the logging level according to your needs.

- **Graceful Shutdown**: Added a KeyboardInterrupt handler to gracefully shut down the proxy when a user interrupts the script (e.g., using Ctrl+C).

- Error handling, logging, and other production considerations have been implemented for a more robust system.

- This is a basic example, and further customization may be needed based on specific production requirements.

- Always revert DNS settings to their original configuration after testing the DNS proxy.

For any issues or improvements, feel free to report them.
