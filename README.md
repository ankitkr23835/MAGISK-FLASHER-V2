# MAGISK-FLASHER-V2


This tool allows you to patch your stock boot.img with the desired Magisk version using a Telegram bot interface. With this tool, you can easily root your Android device.






## INSTALLATION

```bash
git clone https://github.com/ankitkr23835/MAGISK-FLASHER-V2.git
```

```bash
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
```

# now installation process

```bash
cd MAGISK-FLASHER-V2
sed -i "s/\/home\/u201900\/Magisk-flasher/$(pwd | sed 's/\//\\\//g')/g" main.py
pip install -r requirements.txt
```

##              RUN  THE  BOT  LOCALLY


# start the bot to generate session file
```bash
python3 main.py 
```
# Now u can run the bot in background for 24x7

```bash
nohup python3 main.py &
```
