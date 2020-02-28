import os
import re
import time
import datetime

"""
This script goes through all files in a given directory and searches for IP addresses in the strings of the files.
The IP addresses are then modified to have their first two octets be 192.168.

NOTE: This script will do the same for all files in subdirectories of the given directory.

NOTE: Certain patterns are skipped (i.e. 127.0.0.1, 8.8.8.8, 255.255.255.0, 255.255.255.255, addresses that start with 192.168, etc.)

NOTE: This script only scrubs IP addresses, it doesn't do anything with hostnames/fqdn.

NOTE: This script overwrites the files, make a copy of the files if you want to keep the originals.
"""

start_time = time.time()  # will be used to determine the full run time
regex_IP = re.compile(r"\b(\d{1,3}\.\d{1,3})(\.\d{1,3}\.\d{1,3})\b", flags=re.DOTALL)  # This regex string finds IP addresses in the logs


def find_and_replace(passed_dir):
    for rootdir, subdirs, files in os.walk(passed_dir):  # Checking the dir/subdirs/files in the provided directory
        for file in files:
            file_path = os.path.join(rootdir, file)  # full file path stored as 'file_path'
            fin = open(file_path, "rt")  # opening the file with read permissions to work with it
            data = fin.readlines()  # doing readlines to have the data as a list of strings
            new_data = []  # we will populate this with the new information, then write this to the file later
            for line in data:  # iterating through all the lines we read into memory earlier
                found_ips = re.findall(regex_IP, line)  # there may be more than 1 IP on a line, need to use re.findall() to get each IP
                if found_ips:  # checking for a match so the script knows which code to execute here
                    for ip_address in found_ips:  # found_ips is a list of the matched IP addresses, remember the IP addresses are divided into groups example: 1.2.3.4 would be stored as ('1.2', '.3.4')
                        old_ip = ip_address[0] + ip_address[1]  # we are combining the two groups from the regex match to get the IP address back -- 1.2.3.4 instead of ('1.2', '.3.4')
                        new_ip = "192.168" + ip_address[1]  # we are replacing the first two octets with 192.168, but keeping the last two octets of the original IP address
                        if old_ip == '127.0.0.1' or old_ip == '8.8.8.8' \
                                or old_ip == '0.0.0.0' or old_ip == '255.255.255.255' \
                                or old_ip == '255.255.255.0' or old_ip.startswith("192.168."):  # checking for IPs we don't care about
                            print(f"\nSkipping IP address {old_ip}.\n")  # printing that we are skipping those IPs
                            continue  # now skipping the IP we don't care about and moving to the next ip_address in found_ips, if no more ip_address in found_ips then move to next line
                        else:  # when the IP address isn't in the list of ones to ignore, then we come here to change the IP
                            line = re.sub(old_ip, new_ip, line, flags=re.DOTALL)  # substituting the old IP address for the new one
                            print(f"\nChanged IP address {old_ip} to be {new_ip}.\n")  # printing to the terminal that we changed the old IP for the new IP
                    new_data.append(line)  # appending the line to the new_data list after handling the line (changing IPs if needed)
                else:  # when no IP address is found on the line, we come here
                    new_data.append(line)  # to append the line to the new_data list without any changes as there is no IPs in the line
            fin.close()  # we are done with the file, so we close it here
            fout = open(file_path, "wt")  # now we open the file with write privileges. This removes all contents from the file making it an empty file
            fout.writelines(new_data)  # writing the lines from new_data to the file to repopulate the file with the scrubbed data
            fout.close()  # we are done with the file, so now we close it


directory_with_logs = input("\nWhat is the directory where the logs are? : ")  # have the user provide the directory to search in
find_and_replace(directory_with_logs)  # executing the function to actually find all the IP addresses and modify them


print("\nReading the files is complete. Please spot check the files to see if any old IP addresses are still there.\n")

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
