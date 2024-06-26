#!/bin/bash


# Replace all occurrences of /home/u209464 with the current directory in the file
#sed -i "s#/home/u209602#$replacement#g" $file_path
# Replace all occurrences of /home/u209464/Work with opt/render in the 
# Define an array of process names and their corresponding commands
python -m venv myenv
source myenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
declare -A processes
processes["zipper.py"]="python3 main.py"
# Declare an associative array to track process PIDs
declare -A pids


# Monitor and restart processes
while true; do
    for process_name in "${!processes[@]}"; do
        # Get the PID of the process
        pid="${pids[$process_name]}"

        if [[ -z "$pid" ]] || ! kill -0 "$pid" 2>/dev/null; then
            echo "Starting $process_name..."
            eval "${processes[$process_name]}"
            # Store the PID of the newly started process
            pids["$process_name"]="$!"
        fi
    done
    sleep 1
done

