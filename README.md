# MAGISK-FLASHER-V2

This tool allows you to patch your stock boot.img with the desired Magisk version using a Telegram bot interface. With this tool, you can easily root your Android device.

## Installation

```bash
   git clone https://github.com/ankitkr23835/MAGISK-FLASHER-V2.git
cd MAGISK-FLASHER-V2
sed -i "s/\/home\/u201900\/Magisk-flasher/$(pwd | sed 's/\//\\\//g')/g" main.py
pip install -r requirements.txt
```

## Run the bot locally
```bash
nohup python3 main.py &
```
