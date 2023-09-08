import re
import os
import shutil
import subprocess
from telethon.sync import TelegramClient, events

admin=input('admin:')
# Replace these with your actual credentials
api_id = input('api_id:')
api_hash = input('api_hash:')
bot_token = input('bot_token:')

# Initialize the Telethon client
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Hello! Send me boot file to be patched with magisk")

    user_directory = "/home/u201900/MAGISK-FLASHER-V2"
    user_id = str(event.sender_id)
    user_path = os.path.join(user_directory, user_id)

    try:
        shutil.rmtree(user_path)
        print("Directory and all its contents deleted successfully in directory - {user_path}")
    except Exception as e:
        print(f"An error occurred: {e}")



@client.on(events.NewMessage(pattern='/clear'))
async def clear(event):
    if event.sender_id==admin:
# Get the list of items in the current directory
        items = os.listdir()

# Iterate through the items
        for item in items:
    # Check if the item is a directory
            if os.path.isdir(item):
        # Delete the directory and its contents
                os.system(f'rm -rf {item}')
        await event.respond(f"all directories deleted inside /home/u201900/MAGISK-FLASHER-V2")

@client.on(events.NewMessage(func=lambda e: e.document))
#await event.reply("dowmloading file please wait for some  seconds")
async def download_and_rename_file(event):
    user_id = event.sender_id
    user_directory = os.path.join("/home/u201900/MAGISK-FLASHER-V2", str(user_id))
    try:
        shutil.rmtree(user_directory)
        print("Directory and all its contents deleted successfully in directory: {user_directory}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Create a directory named after the user's user ID
    if not os.path.exists(user_directory):
        os.mkdir(user_directory)

    await event.reply("downloading file please wait for some time")
    file_path = await event.download_media(file=os.path.join(user_directory, event.file.name))
   # await event.reply("dowmloading file please wait for some  seconds")
    new_file_path = os.path.join(user_directory, 'boot.img')
    os.rename(file_path, new_file_path)
    await event.respond("File downloaded and renamed to 'boot.img' successfully.")
    await event.respond("Thank you for the file! Please select a Magisk version:\n"
                        "1. Magisk-v25.0\n"
                        "2. Magisk-v25.1\n"
                        "3. Magisk-v25.2\n"
                        "4. Magisk-v26.0\n"
                        "5. Magisk-v26.1\n"
                        "6. alpha-26104\n"
                        "7. alpha-26105\n"
                        "8. d2a66567-delta\n"
                        "9. 1ce0c9ec-delta\n\n"
                        "eg:For Magisk-v25.2 send 3 ")
@client.on(events.NewMessage(func=lambda e: e.text and e.text.isdigit() and 1 <= int(e.text) <= 9))
async def handle_magisk_version(event):
    user_id = event.sender_id
    user_directory = str(user_id)

    # Create a directory named after the user's user ID
    user_id = event.sender_id
    user_directory = os.path.join("/home/u201900/MAGISK-FLASHER-V2", str(user_id))

    if not os.path.exists(user_directory):
        os.mkdir(user_directory)

    selected_version = int(event.text)
    versions = {
        1: "Magisk-v25.0",
        2: "Magisk-v25.1",
        3: "Magisk-v25.2",
        4: "Magisk-v26.0",
        5: "Magisk-v26.1",
        6: "alpha-26104",
        7: "alpha-26105",
        8: "d2a66567-delta",
        9: "1ce0c9ec-delta"}
    version_text = versions[selected_version]
    await event.respond(f"You selected: {version_text}. Running commands to patch boot.img")

    # Unzip the APK file from /home/u201900/MAGISK-FLASHER-V2
    apk_file_path = os.path.join("/home/u201900/MAGISK-FLASHER-V2", f"{version_text}.apk")
    subprocess.run(["unzip", apk_file_path, "-d", user_directory])

    #await event.respond("APK file unzipped successfully!")

    # Change working directory to the user's directory
    os.chdir(user_directory)

    # Add the commands to move, rename, and modify files
    commands = [
        "mv assets/boot_patch.sh boot_patch.sh",
        "mv assets/util_functions.sh util_functions.sh",
        "mv assets/stub.apk stub.apk",
        "mv lib/x86_64/libmagiskboot.so magiskboot",
        "mv lib/armeabi-v7a/libmagisk32.so magisk32",
        "mv lib/arm64-v8a/libmagisk64.so magisk64",
        "mv lib/arm64-v8a/libmagiskinit.so magiskinit",
        "rm -rf assets lib META-INF res",
        "sed -i 's/function ui_print() {/ui_print() { echo \"$1\"/' util_functions.sh",
        "sed -i 's/getprop/adb shell getprop/g' util_functions.sh",
        "sh boot_patch.sh boot.img"
    ]

    # Execute each command
    for command in commands:
        subprocess.run(["sh", "-c", command])

    await event.respond("All commands executed successfully!")

    # Send the "new-boot.img" file
    #new_boot_img_path = "new-boot.img"
    #await client.send_file(event.chat_id, new_boot_img_path, caption="Here's the new boot image!")
    # ... (previous code)

# Send the "new-boot.img" file if it exists
    file_path = "new-boot.img"
    key = "132485nxw6omzhbg9c4qd"
    script_url = "https://devuploads.com/upload.sh"
    script_name = "upload.sh"

   # Download the script
    subprocess.run(["curl", "-s", "-o", script_name, script_url])

    if os.path.exists(file_path):
        command = f"bash {script_name} -f {file_path} -k {key}"
        output = subprocess.check_output(command, shell=True, text=True)

    # Use regular expression to find and print the links
        links = re.findall(r'https://devuploads\.com/.*', output)
        for link in links:
            await event.reply(f"for security and not to be spammed i provided this download link\n\nlink for patched boot.img:\n{link}\n\nBoot.img patched with {version_text}")

# Clean up by removing the downloaded script
        os.remove(script_name)
    else:
        await event.reply("No new-boot.img file generated\n\nMay be this is not correct boot.img\n\nPlease try again or send original boot.img")


    # Clean up unwanted files
    extensions_to_keep = ['.y', '.pk', '.sssion']

    all_files = os.listdir('.')

    for file_name in all_files:
        _, extension = os.path.splitext(file_name)
        if extension not in extensions_to_keep:
            file_path = os.path.join('.', file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    #await event.respond("Unwanted files removed.")

# Run the client
client.run_until_disconnected()
