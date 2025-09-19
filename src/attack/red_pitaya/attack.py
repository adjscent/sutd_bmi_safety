from redpitaya_scpi import scpi  
import time

# Initialize Red Pitaya SCPI connection
RP_IP = '192.168.10.251'  # Replace with your Red Pitaya's IP
rp = scpi(RP_IP)

def ads1115_interference_test():
    """Generate RF signals to test ADS1115 vulnerabilities."""
    try:
        # Reset generator
        rp.tx_txt('GEN:RST')

        # Configure Channel 1 for interference
        channel = 1
        freq = 1e5  # Start at 1 MHz (target I2C harmonics or analog input resonance)
        amplitude = 0.9  # Max safe amplitude (±1V)
        waveform = 'NOISE'  # Options: SINE, SQUARE, NOISE, PWM

        # Set signal parameters (using direct SCPI commands)
        rp.tx_txt(f'SOUR{channel}:FUNC {waveform}')
        rp.tx_txt(f'SOUR{channel}:FREQ:FIX {freq}')
        rp.tx_txt(f'SOUR{channel}:VOLT {amplitude}')

        # Enable AM modulation (adds noise to carrier)
        rp.tx_txt(f'SOUR{channel}:AM:STATE ON')
        rp.tx_txt(f'SOUR{channel}:AM:DSIN')  # 50% modulation depth
        rp.tx_txt(f'SOUR{channel}:AM:SOUR INT')  # Internal noise source

        # Enable output
        rp.tx_txt(f'OUTPUT{channel}:STATE ON')
        print(f"Transmitting {freq/1e6} MHz AM noise on channel {channel}...")

        # Optional: Frequency sweep (uncomment to test)
        # for freq in range(1_000_00, 10_000_000, 1_000_00):
        #     rp.tx_txt(f'SOUR{channel}:FREQ:FIX {freq}')
        #     print(f"Transmitting {freq/1e6} MHz AM noise on channel {channel}...")
        #     time.sleep(1)

        input("Press Enter to stop interference...")

    finally:
        # Cleanup
        rp.tx_txt(f'OUTPUT{channel}:STATE OFF')
        rp.close()

if __name__ == "__main__":
    ads1115_interference_test()