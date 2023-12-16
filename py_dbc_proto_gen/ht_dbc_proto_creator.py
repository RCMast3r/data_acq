from cantools.database import *
import requests
import re
from ht_can_msg_signals import *


class HyTechCANmsg:
    def __init__(self):
        self.can_id_name = ""
        self.can_id_hex = 0x0
        self.sender_name = ""
        self.packing_type = ""
        self.signals = [can.signal]

    def create_msg() -> can.message:
        msg = can.message()
        return msg


# GitHub API URL to fetch the file content
# extract CAN ids from hytech CAN's definition:
def extract_defines(header_file_content):
    defines = {}
    for line in header_file_content:
        # Check if the line starts with '#define'
        if line.startswith("#define"):
            line_without_comment = re.sub(r"//.*$", "", line)
            if line_without_comment.startswith("#define"):
                parts = line_without_comment.strip().split()
                if len(parts) >= 3:
                    define_name = parts[1]
                    define_value = " ".join(parts[2:])
                    defines[define_name] = define_valueparts = line.strip().split()
            # Extract the name and value of the define
            if len(parts) >= 3:
                define_name = parts[1]
                define_value = " ".join(parts[2:])
                defines[define_name] = define_value

    return defines


def get_header_files_in_folder(owner, repo, folder_path):
    files = []

    # GitHub API URL to get the contents of a folder
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{folder_path}"
    # Fetch the contents of the folder
    response = requests.get(url)

    if response.status_code == 200:
        content = response.json()

        # Extract file names from the response
        for item in content:
            if (
                "type" in item
                and item["type"] == "file"
                and item["name"].endswith(".h")
            ):
                files.append(item["name"])
    else:
        print(f"Failed to fetch folder contents. Status code: {response.status_code}")
    return files


CAN_defines_url = f"https://raw.githubusercontent.com/hytech-racing/code-2024/main/Libraries/HyTech_CAN/CAN_ID.h"

defines_dict = {}

# Fetch the CAN ID define content from the header file
response = requests.get(CAN_defines_url)
if response.status_code == 200:
    content = response.text.split("\n")
    defines_dict = extract_defines(content)
    # Print the extracted defines
else:
    print("ERROR: could not get CAN ID defines")

# create the CAN messages:
listofmsgs = []
for can_name, can_id in defines_dict.items():
    msg = HyTechCANmsg()
    msg.can_id_hex = can_id
    msg.can_id_name = can_name
    listofmsgs.append(msg)
# extract all header files from hytech CAN library

CAN_lib_owner = "hytech-racing"
CAN_lib_repo = "code-2024"
CAN_lib_folder = "Libraries/HyTech_CAN"

# get the names of the header files in the folder on git
files_in_folder = get_header_files_in_folder(
    CAN_lib_owner, CAN_lib_repo, CAN_lib_folder
)

# remove alread processed / extraneous headers we dont need to parse
files_in_folder.remove("CAN_ID.h")
files_in_folder.remove("HyTech_CAN.h")

print(files_in_folder)
# generate list of senders of CAN messages via the string before the first underscore
list_of_senders = []
for file_name in files_in_folder:
    sender_name = file_name.split("_", 1)
    if sender_name[0] not in list_of_senders:
        list_of_senders.append(sender_name[0])


# associate CAN ids with their senders while creating a CAN message:
def extract_between_underscores(input_string):
    # Find the positions of the first and second underscores
    first_underscore = input_string.find("_")
    second_underscore = input_string.find("_", first_underscore + 1)

    # Extract the substring between the first two underscores
    if first_underscore != -1 and second_underscore != -1:
        return input_string[first_underscore + 1 : second_underscore]
    else:
        return None  # Return None if there aren't two underscores


# getting sender from ID name gotten from unique CAN ID's
list_of_sender_ids = []
for msg in listofmsgs:
    pot_sender = extract_between_underscores(msg.can_id_name)
    for sender in list_of_senders:
        if sender == re.sub(r"\d+", "", pot_sender):
            msg.sender_name = sender

# time for some semi-jank


# TODO energy meter
# TODO motor controller
# TODO MCU
# TODO SAB


def create_field_name(name: str) -> str:
    replaced_text = name.replace(" ", "_")
    replaced_text = replaced_text.replace("(", "")
    replaced_text = replaced_text.replace(")", "")
    return replaced_text


def generate_proto_message_from_CAN_message(can_msg: HyTechCANmsg):
    # if the msg has a conversion, we know that the value with be a float
    file_lines = []
    msgname = can_msg.can_id_name
    # type and then name
    file_lines.append("message "+msgname.lower() + " {")
    line_index = 0
    for sig in can_msg.signals:
        line_index += 1
        if sig.is_float or sig.conversion is not None:
            line = "    float " + create_field_name(sig.name) + " = " + str(line_index) + ";"
            file_lines.append(line)
        elif sig.choices is not None:
            line = "    string " + create_field_name(sig.name) + " = " + str(line_index) +";"
        elif sig.length == 1:
            line = "    bool " + create_field_name(sig.name) +  " = " + str(line_index) +";"
        elif sig.length >1:
            line = "    int " + create_field_name(sig.name) +   " = " + str(line_index) +";"
        else:
            print("ERROR")
    file_lines.append("}")
    return file_lines


couloum_count_sigs = get_bms_coulomb_count_signals()

with open('test.proto', 'a') as proto_file:
    proto_file.write("syntax = \"proto3\";\n\n")
    for msg in listofmsgs:
        if msg.can_id_name == "ID_BMS_COULOMB_COUNTS":
            msg.signals = couloum_count_sigs
            lines = generate_proto_message_from_CAN_message(msg)
            for line in lines:
                proto_file.write(line+"\n")
            proto_file.write("\n")
