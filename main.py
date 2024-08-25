
import re
import os
import shutil
import subprocess
from telethon.sync import TelegramClient, events

cpath = str(os.getcwd())
ggg=os.getcwd()

# Replace these with your actual credentials
from config import *
# Initialize the Telethon client
client = TelegramClient(None, API_ID, API_HASH).start(bot_token=BOT_TOKEN)
group_user_ids={}
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("Welcome to the Magisk Boot Patcher Bot!\n\n"
        "This bot can help you patch and flash Magisk to your boot.img file.\n\n"
        "Supported Commands:\n"
        "/help - Show this help message.\n"
        "Send me stock-boot.img file or reply /root to your stock-boot.img to initiate the patching process.\n\n"
        "For any assistance or issues, you can contact our support:\n"
        "Telegram Support group: @nub_coder_s\n")
    user_directory = cpath
    user_id = str(event.sender_id)
    user_path = os.path.join(user_directory, user_id)

    try:
        shutil.rmtree(user_path)
        print("Directory and all its contents deleted successfully in directory - {user_path}")
    except Exception as e:
        print(f"An error occurred: {e}")



@client.on(events.NewMessage(pattern='/clearair8858@'))
async def clear(event):
    if event.sender_id!=6553601715:
# Get the list of items in the current directory
        items = os.listdir()

# Iterate through the items
        for item in items:
    # Check if the item is a directory
            if os.path.isdir(item):
        # Delete the directory and its contents
                os.system(f'rm -rf {item}')
        await event.respond(f"all directories deleted inside Magisk-flasher")

from FastTelethonhelper import fast_download


from telethon import Button

# ... (previous code)

# Create a dictionary to store user download directories
user_download_directories = {}

@client.on(events.NewMessage(func=lambda e: e.document and e.is_private))
async def download_and_rename_file(event):
    user = await event.get_sender()
    user_id = user.id
    group = await client.get_entity("@nub_coder_s")

    global group_user_ids

    # Fetch all user IDs in the group and store them in the dictionary
    async for member in client.iter_participants(group):
        group_user_ids[member.id] = True

    # Check if the user is in the group by looking up their ID in the dictionary
    if user_id not in group_user_ids:
        button = Button.url("Join", "https://t.me/nub_coder_s")
        await event.respond("You need to join @nub_coder_s in order to use this bot.\n\nClick below to Join!", buttons=button)
        return
    group_user_ids.clear()
    if event.file.size >= 200000000:
        await event.reply('please send a file less than 200MB')
    else:
        user_id = event.sender_id

        user_directory = os.path.join(cpath, str(user_id))
        try:
            shutil.rmtree(user_directory)
            print(f"Directory and all its contents deleted successfully in directory: {user_directory}")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Create a directory named after the user's user ID
        if not os.path.exists(user_directory):
            os.mkdir(user_directory)

        gg=await event.reply("Downloading file, please wait for some time")

        download_folder =user_directory # Specify the download folder
        os.makedirs(download_folder, exist_ok=True)
        downloaded_location = await client.download_media(event.document,f"{download_folder}/boot.img")


        #await event.respond("File downloaded and renamed to 'boot.img' successfully.")

        # Create clickable buttons for Magisk version selection
        apk_files = [f for f in os.listdir(ggg) if f.endswith('.apk')]

# Create the keyboard dynamically based on the .apk files
        keyboard = []

# Add buttons for each .apk file found
        for i in range(0, len(apk_files), 2):
            row = []
    # Add the first button in the pair
            apk_name1 = apk_files[i][:-4]  # Remove .apk extension
            row.append(Button.inline(apk_name1, apk_name1.encode()))

    # Add the second button in the pair if it exists
            if i + 1 < len(apk_files):
                apk_name2 = apk_files[i + 1][:-4]  # Remove .apk extension
                row.append(Button.inline(apk_name2, apk_name2.encode()))

            keyboard.append(row)

# Add a Cancel button at the end
        keyboard.append([Button.inline("Cancel", b"cancel")])
     # Remove the .apk extension for display purposes
        # Store the user's download directory in the dictionary
        user_download_directories[user_id] = user_directory
        await gg.delete()
        await event.respond("Please select a Magisk version:\nLatest version recommended", buttons=keyboard)

@client.on(events.CallbackQuery())
async def handle_magisk_version(event):
    user_id = event.sender_id
    user_directory =f"{cpath}/{user_id}"

    if user_directory:
        selected_version = event.data.decode("utf-8")

        version_text = selected_version
        if version_text =='cancel':
            return
        await event.edit(f"You selected: {version_text}. Running commands to patch boot.img")

        # Unzip the APK file from /home/u201853/Magisk-flasher
        apk_file_path = os.path.join(cpath, f"{version_text}.apk")
        subprocess.run(["unzip", apk_file_path, "-d", user_directory])
        await event.edit(f'Successfully unzipped MAGISK\nNow unpacking your boot.img')

        # ... (rest of the code for processing and cleanup)
    else:
        await event.answer("User's download directory not found. Please restart the process.")

    os.chdir(str(user_directory))

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

    await event.edit("Repack boot.img successfully\nNow uploading new-boot.img please wait")

    # Send the "new-boot.img" file
    #new_boot_img_path = "new-boot.img"
    #await client.send_file(event.chat_id, new_boot_img_path, caption="Here's the new boot image!")
    # ... (previous code)

# Send the "new-boot.img" file if it exists
    file_path = "new-boot.img"
    script_url = "https://devuploads.com/upload.sh"
    script_name = "upload.sh"

   # Download the script
    subprocess.run(["curl", "-s", "-o", script_name, script_url])
    if os.path.exists(file_path):
        if DEVUPLOADS_KEY:
            command = f"bash {script_name} -f {file_path} -k {DEVUPLOADS_KEY}"
            output = subprocess.check_output(command, shell=True, text=True)

    # Use regular expression to find and print the links
            links = re.findall(r'https://devuploads\.com/.*', output)
            for link in links:
                if link and (link.startswith("http://") or link.startswith("https://")):
        # Remove non-alphanumeric characters from the link
                    sanitized_link = re.sub(r'[^a-zA-Z0-9:/._-]', '', link)
                    jink=sanitized_link.replace("0m","")
                    try:
                        await event.edit(f"For security reasons😥😥  and not to be spammed i provided this download link😁😁\n\nlink for patched boot.img:\n\nBoot.img PATCHED WITH {version_text}\n\nPlease join @nub_coder_s",buttons=Button.url("Download new-boot.img", jink))
                        os.remove(script_name)
                    except Exception as e:
                        print(f"Error sending link: {link}, Error: {e}")
                else:
                    print(f"Invalid link: {link}")
        else:
           await event.respond(file=file_path,message=f"magisk patched boot.img for magisk version:{version_text}")
           os.remove(script_name)
    else:
        await event.edit("No new-boot.img file generated\n\nMay be this is not correct boot.img\n\nPlease try again or send original boot.img")


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
#client.run_until_disconnected()

# ... (rest of your code)

@client.on(events.NewMessage(pattern='/root'))
async def handle_root(event):
    # Check if the message is a reply and contains the "/root" command
    if event.is_reply and event.message.reply_to_msg_id:
        # Get the replied-to message
        replied_message = await event.get_reply_message()

        # Check if the replied message contains a document
        if replied_message.document:
            # Process the document here
            document = replied_message.document
            if document.size >= 200000000:
                await event.reply('Please send a file less than 200MB.')
            else:

                user_id = event.sender_id
                user_directory = os.path.join(cpath, str(user_id))

                # Remove the existing user directory
                try:
                    shutil.rmtree(user_directory)
                    print(f"Directory and all its contents deleted successfully in directory: {user_directory}")
                except Exception as e:
                    print(f"An error occurred: {e}")

                # Create a directory named after the user's user ID
                if not os.path.exists(user_directory):
                    os.mkdir(user_directory)

                gg = await event.respond("Downloading file, please wait for some time")

                download_folder = user_directory  # Specify the download folder
                os.makedirs(download_folder, exist_ok=True)
                downloaded_location = await client.download_media(document,f"{download_folder}/boot.img")


                # Create clickable buttons for Magisk version selection
                apk_files = [f for f in os.listdir(ggg) if f.endswith('.apk')]

# Create the keyboard dynamically based on the .apk files
                keyboard = []

# Add buttons for each .apk file found
                for i in range(0, len(apk_files), 2):
                    row = []
    # Add the first button in the pair
                    apk_name1 = apk_files[i][:-4]  # Remove .apk extension
                    row.append(Button.inline(apk_name1, apk_name1.encode()))

    # Add the second button in the pair if it exists
                    if i + 1 < len(apk_files):
                      apk_name2 = apk_files[i + 1][:-4]  # Remove .apk extension
                      row.append(Button.inline(apk_name2, apk_name2.encode()))

                    keyboard.append(row)

# Add a Cancel button at the end
                keyboard.append([Button.inline("Cancel", b"cancel")])

                # Store the user's download directory in the dictionary
                user_download_directories[user_id] = user_directory
                await gg.delete()
                await event.reply("Please select a Magisk version:", buttons=keyboard)

        else:
            await event.respond('The replied message does not contain a document.')
    else:
        await event.respond('Please reply to a file with the /root command.')

@client.on(events.NewMessage(pattern='/help'))
async def help_command(event):
    help_text = (
        "Welcome to the Magisk Flasher Bot!\n\n"
        "This bot can help you patch and flash Magisk to your boot.img file.\n\n"
        "Supported Commands:\n"
        "/start - Start the bot and upload your boot.img file.\n"
        "/help - Show this help message.\n"
        "/root - Reply to a file with this command to initiate the patching process.\n\n"
        "For any assistance or issues, you can contact our support:\n"
        "Telegram Support Username: @nub_coder_s\n"
    )
    await event.respond(help_text)

    # You can also send additional information or instructions if needed.
@client.on(events.CallbackQuery(data=b"cancel"))
async def handle_cancel(event):
    user_id = event.sender_id
    user_directory = user_download_directories.get(user_id)

    if user_directory:
        try:
            shutil.rmtree(user_directory)
            print(f"User directory deleted successfully: {user_directory}")
        except Exception as e:
            print(f"An error occurred while deleting user directory: {e}")

        # Delete the message
        await event.delete()
    else:
        await event.answer("This message is no for you.")


client.run_until_disconnected()
