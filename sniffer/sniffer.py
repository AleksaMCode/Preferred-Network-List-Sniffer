import subprocess


def sniff(interface):
    subprocess.run(
        ["airodump-ng", "-w", "traffic", "--output-format", "cap", interface],
        capture_output=True,
    )


sniff("wlan1mon")
