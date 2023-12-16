from cantools.database import *
import requests
import re


class HyTechCANmsg:
    def __init__(self):
        self.can_id_name = ""
        self.can_id_hex = 0x0
        self.sender_name = ""
        self.packing_type = ""


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


# multiple different CAN msgs can have the same array of signals, these functions create the individual arrays of signals
# TODO put in units
# TODO verify
def get_bms_balancing_status_signals():
    signals = []
    signals.append(can.Signal(name="group_id", start=0, length=4))
    # for now this is how we doin this
    number_of_cells_per_even_ic = 12
    number_of_cells_per_odd_ic = 9
    # number_of_ics_per_group = 2
    # while i<number_of_cells_per_group:
    #     signals.append(can.Signal(name="cell_"+(i+1)+"_balancing_status"), start=, length=1)
    #     i+=1
    return signals


def get_bms_coulomb_count_signals():
    signals = []
    ch_disch_conv = conversion.LinearConversion(
        scale=(1 / 10000), offset=0, is_float=False
    )
    signals.append(
        can.Signal(name="total charge", start=0, length=32, conversion=ch_disch_conv)
    )
    signals.append(
        can.Signal(
            name="total discharge",
            start=32,
            length=32,
            unit="Coulombs",
            conversion=ch_disch_conv,
        )
    )
    return signals


def get_bms_detailed_temp_signals():
    signals = []
    temp_scale_conv = conversion.LinearConversion(
        scale=(1 / 100), offset=0, is_float=False
    )
    signals.append(can.Signal(name="ic id", start=0, length=4))
    signals.append(can.Signal(name="group id", start=4, length=4))
    id = 0
    while id < 3:
        signals.append(
            can.Signal(
                name="thermistor id " + id,
                start=8 + (16 * id),
                length=16,
                conversion=temp_scale_conv,
                is_signed=True,
            )
        )
        id += 1
    return signals


def get_bms_detailed_voltages_signals():
    signals = []
    conv = conversion.LinearConversion(scale=(1 / 10000), offset=0, is_float=False)
    signals.append(can.Signal(name="ic id", start=4, length=4))
    signals.append(can.Signal(name="group id", start=0, length=4))
    i = 0
    num_of_voltages = 3
    # repeated signals for multiple voltages
    while i < num_of_voltages:
        signals.append(
            can.Signal(
                name="voltage " + i, start=8 + (i * 16), length=16, conversion=conv
            )
        )
    return signals


def get_bms_onboard_detailed_temperatures_signals():
    signals = []
    conv = conversion.LinearConversion(scale=(1 / 100), offset=0, is_float=False)
    signals.append(can.Signal(name="ic id", start=0, length=8))
    signals.append(
        can.signal(name="temp 0", start=8, length=16, conversion=conv, is_signed=True)
    )
    signals.append(
        can.signal(name="temp 1", start=24, length=16, conversion=conv, is_signed=True)
    )
    return signals


def get_bms_onboard_temperatures_signals():
    signals = []
    conv = conversion.LinearConversion(scale=(1 / 100), offset=0, is_float=False)
    signals.append(
        can.signal(
            name="average temp", start=0, length=16, conversion=conv, is_signed=True
        )
    )
    signals.append(
        can.signal(
            name="low temp", start=16, length=16, conversion=conv, is_signed=True
        )
    )
    signals.append(
        can.signal(
            name="high temp", start=32, length=16, conversion=conv, is_signed=True
        )
    )
    return signals


def get_bms_status_signals():
    signals = []
    signals.append(can.signal(name="state", start=0, length=8))
    signals.append(can.signal(name="overvoltage error", start=8, length=1))
    signals.append(can.signal(name="undervoltage error", start=9, length=1))
    signals.append(can.signal(name="total voltage high error", start=10, length=1))
    signals.append(can.signal(name="discharge overcurrent error", start=10, length=1))
    signals.append(can.signal(name="charge overcurrent error", start=11, length=1))
    signals.append(can.signal(name="discharge overtemp error", start=12, length=1))
    signals.append(can.signal(name="charge overtemp error", start=13, length=1))
    signals.append(can.signal(name="undertemp error", start=14, length=1))
    signals.append(can.signal(name="overtemp error", start=15, length=1))
    conv = conversion.LinearConversion(scale=(1 / 100), offset=0, is_float=False)
    signals.append(
        can.signal(name="current", start=24, length=16, is_signed=True, conversion=conv)
    )
    signals.append(
        can.signal(name="shutdown g above threshold error", start=40, length=1)
    )
    signals.append(
        can.signal(name="shutdown h above threshold error", start=41, length=1)
    )
    return signals


def get_bms_voltage_signals():
    signals = []
    conv = conversion.LinearConversion(scale=(1 / 10000), offset=0, is_float=False)
    conv_100 = conversion.LinearConversion(scale=(1 / 100), offset=0, is_float=False)
    signals.append(
        can.signal(name="average voltage", start=0, length=16, conversion=conv)
    )
    signals.append(can.signal(name="low voltage", start=16, length=16, conversion=conv))
    signals.append(
        can.signal(name="high voltage", start=32, length=16, conversion=conv)
    )
    signals.append(
        can.signal(name="total voltage", start=48, length=16, conversion=conv_100)
    )
    return signals


couloum_count_sigs = get_bms_coulomb_count_signals()
for msg in listofmsgs:
    print(msg.can_id_name, msg.sender_name)
