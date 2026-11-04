"""
Hold the ADG1607 on one channel while ST's demo runs in another terminal.

Type 1-8 to select a channel, 0 to switch everything off, q to quit.
The mux stays on the selected channel until you change it. EN is always
set low (everything off) when the script exits.

Wiring as in README.md: A0 = GPIO17, A1 = GPIO27, A2 = GPIO22, EN = GPIO23.
"""

from gpiozero import DigitalOutputDevice

A0 = DigitalOutputDevice(17)
A1 = DigitalOutputDevice(27)
A2 = DigitalOutputDevice(22)
EN = DigitalOutputDevice(23)


def select(channel: int) -> None:
    EN.off()  # everything off while the address changes
    code = channel - 1
    A0.value = code & 1
    A1.value = (code >> 1) & 1
    A2.value = (code >> 2) & 1
    EN.on()


def main() -> None:
    EN.off()
    print("All switches off.")
    while True:
        cmd = input("Channel 1-8, 0 = off, q = quit: ").strip().lower()
        if cmd == "q":
            break
        if cmd == "0":
            EN.off()
            print("  All off")
        elif cmd.isdigit() and 1 <= int(cmd) <= 8:
            select(int(cmd))
            print(f"  Channel {cmd} on")
        else:
            print("  Type a number 1-8, 0 or q")


if __name__ == "__main__":
    try:
        main()
    finally:
        EN.off()
