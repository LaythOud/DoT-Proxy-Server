import socket
import ssl
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_client(client_socket, target_host, target_port, addr):
    try:
        # Receive DNS query from the client
        request = client_socket.recv(4096)
        logger.info(f"[*] Wrapping request with TLS")
         # Connect to the DNS-over-TLS server (e.g., Cloudflare)
        tls_socket = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        tls_socket.connect((target_host, target_port))
        # Forward the DNS query to the DNS-over-TLS server
        tls_socket.send(request)
        # Receive the response from the DNS-over-TLS server
        response = tls_socket.recv(4096)
        logger.info(f"[*] Sending response to the address {addr}")
        # Send the DNS response back to the client
        client_socket.send(response)
    except Exception as e:
        # Log any errors that may occur during client handling
        logger.error(f"Error handling client: {e}")
    finally:
        # Close client and DNS-over-TLS sockets
        client_socket.close()
        tls_socket.close()

def start_proxy(proxy_port, target_host, target_port):
    # Setup a socket for the DNS proxy
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.bind(("0.0.0.0", proxy_port))
    proxy.listen(5)
    logger.info(f"[*] Listening on 0.0.0.0:{proxy_port}")

    while True:
        try:
            # Accept incoming client connections
            client_socket, addr = proxy.accept()
            logger.info(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
            # Handle each client connection in a separate thread
            client_handler = threading.Thread(target=handle_client, args=(client_socket, target_host, target_port, f"{addr[0]}:{addr[1]}"))
            client_handler.start()
        except Exception as e:
            # Log any errors that may occur during connection handling
            logger.error(f"Error accepting connection: {e}")

if __name__ == "__main__":
    # Configuration
    proxy_port = 53  # DNS
    target_host = "1.1.1.1"  # Cloudflare DNS-over-TLS server
    target_port = 853

    try:
        # Start the DNS proxy
        start_proxy(proxy_port, target_host, target_port)
    except KeyboardInterrupt:
        # Gracefully handle a user interrupt (e.g., Ctrl+C)
        logger.info("Proxy shutting down.")