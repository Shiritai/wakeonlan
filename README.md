# Wake On LAN using Python Script

A simple Python script that wakes your computer up through LAN/WAN (ip or domain name).

## Usage

```bash
python3 wakeonlan.py [-h] [-i IP | -n DOMAIN_NAME] [-p [PORTS ...]] MAC_ADDR
```

For example...

1. LAN
    ```bash
    python3 wakeonlan.py 01:34:67:9a:cd:ff
    ```
2. WAN with domain name
    ```bash
    python3 wakeonlan.py -n your.domain.name 01:34:67:9a:cd:ff
    # or
    python3 wakeonlan.py --domain_name your.domain.name 01:34:67:9a:cd:ff
    ```
3. WAN with ip
    ```bash
    python3 wakeonlan.py -i 8.8.8.8 01:34:67:9a:cd:ff
    # or
    python3 wakeonlan.py --ip 8.8.8.8 01:34:67:9a:cd:ff
    ```

Default port of WOL is `9`, you can use `-p` argument to specify a list of trying ports.

Note: To use WOL before you run this script, you may need to enable WOL function on both BIOS/UEFI and OS.