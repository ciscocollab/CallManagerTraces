import os
import re
import time
import datetime

"""
This script goes through a given directory and searches for files with packet capture extensions.

Then the script leverages tcprewrite to scrub the IP addresses.

Read the tcprewrite man pages if you want to understand more about how tcprewrite works.

NOTE: You need to run this script on a system that supports the command "tcprewrite"
NOTE: You may need to run the command 'sudo apt install tcpreplay' to have the command "tcprewrite" be recognized by the system.
NOTE: ALL packets will have the same sorce and destination MAC addresses after the script is done.
      This is due to the parameters "--enet-dmac=00:55:22:AF:C6:37 --enet-smac=00:44:66:FC:29:AF'" that you can find later in this script.
"""

start_time = time.time()  # will be used to determine the full run time


terminal_cmd_list = []  # this will store all the commands which we will execute later

def find_pcap_files(passed_dir):
    for rootdir, subdirs, files in os.walk(passed_dir):  # Checking the dir/subdirs/files in the provided directory
        for file in files:
            if ".cap" in file.lower() or ".pcap" in file.lower() or ".pcapng" in file.lower():  # looking only for packet capture file extensions
                file_path = os.path.join(rootdir, file)  # full file path stored as 'file_path'
                file_path_with_quotes = '"' + file_path + '"'
                output_file_name = "scrubbed_" + file  # creating a new name for the file based off the old name, annotating that it is scrubbed
                full_path_output_file_name = '"' + os.path.join(rootdir, output_file_name) + '"'
                terminal_cmd = f"tcprewrite --seed=423 --infile={file_path_with_quotes} --outfile={full_path_output_file_name}" + ' --dlt="enet" --enet-dmac=00:55:22:AF:C6:37 --enet-smac=00:44:66:FC:29:AF'  # building the command which will be sent to the terminal
                terminal_cmd_list.append(terminal_cmd)


directory_with_logs = input("\nWhat is the directory where the logs are? : ")  # have the user provide the directory to search in

find_pcap_files(directory_with_logs)  # executing the function to actually find all the IP addresses and modify them

print(f"\nReading the files is complete.")


def yes_no():
    while True:
        question = input("Do you want to execute the commands now?: ")
        yes = set(['yes','y'])
        no = set(['no','n'])

        if question.lower() in yes:
            return True
        elif question.lower() in no:
            return False
        else:
            print("\nplease answer with one of the following: 'yes', 'y', 'no', 'n'")
            continue


execute_commands_now = yes_no()  # checking if the user wants to run the tcprewrite commands right now.

if execute_commands_now == True:
    for command in terminal_cmd_list:
            os.system(command)


date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def how_long():
    """
    This function identifies the current time,
    then subtracts the start time,
    then returns the diff so we can document the program's total runtime.
    """
    duration = time.time() - start_time
    duration = duration / 60
    return round(duration, 1)


# The rest tells the consumer about the runtime in the terminal and the location of the file where the script output is stored
runtime = how_long()
print(f"\nIt took {runtime} minutes for the script to complete.\n")