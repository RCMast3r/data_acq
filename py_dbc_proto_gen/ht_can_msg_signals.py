from cantools.database import *

# multiple different CAN msgs can have the same array of signals, these functions create the individual arrays of signals
# TODO put in units
# TODO verify


# TODO energy meter
# TODO motor controller
# TODO MCU
# TODO SAB


# TODO
def get_bms_balancing_status_signals():
    signals = []
    length = 8 # in bytes
    signals.append(can.signal.Signal(name="group_id", start=0, length=4, byte_order="little_endian"))
    # for now this is how we doin this
    number_of_cells_per_even_ic = 12
    number_of_cells_per_odd_ic = 9
    # number_of_ics_per_group = 2
    # while i<number_of_cells_per_group:
    #     signals.append(can.signal.Signal(name="cell_"+(i+1)+"_balancing_status"), start=, length=1)
    #     i+=1
    return signals, length


def get_bms_coulomb_count_signals():
    signals = []
    length = 8
    ch_disch_conv = conversion.LinearConversion(
        scale=(1 / 10000), offset=0, is_float=False
    )
    signals.append(
        can.signal.Signal(
            name="total charge", start=0, length=32, conversion=ch_disch_conv, byte_order="little_endian"
        )
    )
    signals.append(
        can.signal.Signal(
            name="total discharge",
            start=32,
            length=32,
            unit="Coulombs",
            conversion=ch_disch_conv,
            byte_order="little_endian"
        )
    )
    return signals, length

def get_bms_detailed_voltages_signals():
    signals = []
    length = 7
    conv = conversion.LinearConversion(scale=(1 / 10000), offset=0, is_float=False)
    signals.append(can.signal.Signal(byte_order="little_endian", name="ic id", start=4, length=4))
    signals.append(can.signal.Signal(byte_order="little_endian", name="group id", start=0, length=4))
    i = 0
    num_of_voltages = 3
    # repeated signals for multiple voltages
    while i < num_of_voltages:
        start_bit = 8 + (i * 16)
        signals.append(
            can.signal.Signal(byte_order="little_endian", 
                name="voltage " + str(i), start=start_bit, length=16, conversion=conv
            )
        )
        i += 1
    return signals, length

def get_bms_detailed_temp_signals():
    signals = []
    length =7
    temp_scale_conv = conversion.LinearConversion(
        scale=(1 / 100), offset=0, is_float=False
    )
    signals.append(can.signal.Signal(byte_order="little_endian", name="ic id", start=0, length=4))
    signals.append(can.signal.Signal(byte_order="little_endian", name="group id", start=4, length=4))
    id = 0
    while id < 3:
        signals.append(
            can.signal.Signal(byte_order="little_endian", 
                name="thermistor id " + str(id),
                start=8 + (16 * id),
                length=16,
                conversion=temp_scale_conv,
                is_signed=True,
            )
        )
        id += 1
    return signals, length

def get_bms_onboard_detailed_temperatures_signals():
    signals = []
    length = 5
    conv = conversion.LinearConversion(scale=(1 / 100), offset=0, is_float=False)
    signals.append(can.signal.Signal(byte_order="little_endian", name="ic id", start=0, length=8))
    signals.append(
        can.signal.Signal(byte_order="little_endian", 
            name="temp 0", start=8, length=16, conversion=conv, is_signed=True
        )
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", 
            name="temp 1", start=24, length=16, conversion=conv, is_signed=True
        )
    )
    return signals, length

def get_bms_onboard_temperatures_signals():
    signals = []
    length = 6
    conv = conversion.LinearConversion(scale=(1 / 100), offset=0, is_float=False)
    signals.append(
        can.signal.Signal(byte_order="little_endian", 
            name="average temp", start=0, length=16, conversion=conv, is_signed=True
        )
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", 
            name="low temp", start=16, length=16, conversion=conv, is_signed=True
        )
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", 
            name="high temp", start=32, length=16, conversion=conv, is_signed=True
        )
    )
    return signals, length

def get_bms_status_signals():
    signals = []
    length = 6
    signals.append(can.signal.Signal(byte_order="little_endian", name="state", start=0, length=8))
    signals.append(can.signal.Signal(byte_order="little_endian", name="overvoltage error", start=8, length=1))
    signals.append(can.signal.Signal(byte_order="little_endian", name="undervoltage error", start=9, length=1))
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="total voltage high error", start=10, length=1)
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="discharge overcurrent error", start=11, length=1)
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="charge overcurrent error", start=12, length=1)
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="discharge overtemp error", start=13, length=1)
    )
    signals.append(can.signal.Signal(byte_order="little_endian", name="charge overtemp error", start=14, length=1))
    signals.append(can.signal.Signal(byte_order="little_endian", name="undertemp error", start=15, length=1))
    signals.append(can.signal.Signal(byte_order="little_endian", name="overtemp error", start=16, length=1))
    conv = conversion.LinearConversion(scale=(1 / 100), offset=0, is_float=False)
    signals.append(
        can.signal.Signal(byte_order="little_endian", 
            name="current", start=24, length=16, is_signed=True, conversion=conv
        )
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="shutdown g above threshold error", start=40, length=1)
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="shutdown h above threshold error", start=41, length=1)
    )
    return signals, length

def get_bms_voltage_signals():
    
    signals = []
    length = 8
    conv = conversion.LinearConversion(scale=(1 / 10000), offset=0, is_float=False)
    conv_100 = conversion.LinearConversion(scale=(1 / 100), offset=0, is_float=False)
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="average voltage", start=0, length=16, conversion=conv)
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="low voltage", start=16, length=16, conversion=conv)
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="high voltage", start=32, length=16, conversion=conv)
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", 
            name="total voltage", start=48, length=16, conversion=conv_100
        )
    )
    return signals, length

def get_ccu_status_signals():
    signals = []
    length = 1
    signals.append(can.signal.Signal(byte_order="little_endian", name="charger enabled", start=0, length=1))
    return signals, length

def get_charger_configure_signals():
    signals = []
    length = 5
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="max charging voltage high", start=0, length=8)
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="max charging voltage low", start=8, length=8)
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="max charging current high", start=16, length=8)
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="max charging current low", start=24, length=8)
    )
    signals.append(can.signal.Signal(byte_order="little_endian", name="control", start=32, length=8))
    return signals, length

def get_charger_data_signals():
    signals = []
    length = 7
    signals.append(can.signal.Signal(byte_order="little_endian", name="output dc voltage high", start=0, length=8))
    signals.append(can.signal.Signal(byte_order="little_endian", name="output dc voltage low", start=8, length=8))
    signals.append(can.signal.Signal(byte_order="little_endian", name="output current high", start=16, length=8))
    signals.append(can.signal.Signal(byte_order="little_endian", name="output current low", start=24, length=8))
    signals.append(can.signal.Signal(byte_order="little_endian", name="flags", start=32, length=8))
    signals.append(can.signal.Signal(byte_order="little_endian", name="input ac voltage high", start=40, length=8))
    signals.append(can.signal.Signal(byte_order="little_endian", name="input ac voltage low", start=48, length=8))
    return signals, length

def get_dashboard_status_signals():
    signals = []
    length = 7
    signals.append(can.signal.Signal(byte_order="little_endian", name="start button", start=0, length=1))
    signals.append(can.signal.Signal(byte_order="little_endian", name="buzzer active", start=1, length=1))
    signals.append(can.signal.Signal(byte_order="little_endian", name="ssok above threshold", start=2, length=1))
    # why is this a dash signal?
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="shutdown h above threshold", start=3, length=1)
    )

    signals.append(can.signal.Signal(byte_order="little_endian", name="mark button", start=8, length=1))
    signals.append(can.signal.Signal(byte_order="little_endian", name="mode button", start=9, length=1))
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="motor controller cycle button", start=10, length=1)
    )
    signals.append(can.signal.Signal(byte_order="little_endian", name="launch ctrl button ", start=11, length=1))
    signals.append(can.signal.Signal(byte_order="little_endian", name="torque mode button", start=12, length=1))
    signals.append(can.signal.Signal(byte_order="little_endian", name="led dimmer button", start=13, length=1))

    choice_conv = conversion.NamedSignalConversion(
        scale=1,
        offset=0,
        choices={
            0: "MODE_ONE",
            1: "MODE_TWO",
            2: "ACCELERATION_LAUNCH_CONTROL",
            3: "SKIDPAD",
            4: "AUTOCROSS",
            5: "ENDURANCE",
        },
        is_float=False,
    )
    led_choices = conversion.NamedSignalConversion(
        scale=1,
        offset=0,
        choices={
            0: "OFF",
            1: "ON",
            2: "YELLOW",
            3: "RED",
        },
        is_float=False,
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="dial state", start=16, length=8, conversion=choice_conv)
    )

    signals.append(
        can.signal.Signal(byte_order="little_endian", name="ams led", start=24, length=2, conversion=led_choices)
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="imd led", start=26, length=2, conversion=led_choices)
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="mode led", start=28, length=2, conversion=led_choices)
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", 
            name="motor controller error led",
            start=30,
            length=2,
            conversion=led_choices,
        )
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", 
            name="start status led", start=32, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", 
            name="inertia status led", start=34, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", 
            name="mechanical brake led", start=36, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", 
            name="gen purp led", start=38, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="bots led", start=40, length=2, conversion=led_choices)
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", 
            name="cockpit brb led", start=42, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", 
            name="crit charge led", start=44, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", name="glv led", start=46, length=2, conversion=led_choices)
    )
    signals.append(
        can.signal.Signal(byte_order="little_endian", 
            name="launch control led", start=48, length=2, conversion=led_choices
        )
    )
    return signals, length
