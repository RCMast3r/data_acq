from cantools.database import *

# multiple different CAN msgs can have the same array of signals, these functions create the individual arrays of signals.
# TODO put in units
# TODO verify
# TODO make this more automated and maybe define the signals using a file format
# TODO make this more automated by associating each ID with sets of signals in the file format

# TODO fix this? may wanna re-work this CAN message to make it more easily into a msg
def get_bms_balancing_status_signals():
    signals = []
    length = 8 # in bytes
    signals.append(can.signal.Signal(name="group_id", start=0, length=4))
    # for now this is how we doin this
    number_of_cells_per_even_ic = 12
    number_of_cells_per_odd_ic = 9
    # number_of_ics_per_group = 2
    i=0
    number_of_cell_bits = 60
    while i<number_of_cell_bits:
        signals.append(can.signal.Signal(name="cell_"+str(i+1)+"_balancing_status", start=i+4, length=1))
        i+=1
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
    signals.append(can.signal.Signal(name="ic id", start=4, length=4))
    signals.append(can.signal.Signal(name="group id", start=0, length=4))
    i = 0
    num_of_voltages = 3
    # repeated signals for multiple voltages
    while i < num_of_voltages:
        start_bit = 8 + (i * 16)
        signals.append(
            can.signal.Signal(
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
    signals.append(can.signal.Signal(name="ic id", start=0, length=4))
    signals.append(can.signal.Signal(name="group id", start=4, length=4))
    id = 0
    while id < 3:
        signals.append(
            can.signal.Signal(
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
    signals.append(can.signal.Signal(name="ic id", start=0, length=8))
    signals.append(
        can.signal.Signal(
            name="temp 0", start=8, length=16, conversion=conv, is_signed=True
        )
    )
    signals.append(
        can.signal.Signal(
            name="temp 1", start=24, length=16, conversion=conv, is_signed=True
        )
    )
    return signals, length

def get_bms_onboard_temperatures_signals():
    signals = []
    length = 6
    conv = conversion.LinearConversion(scale=(1 / 100), offset=0, is_float=False)
    signals.append(
        can.signal.Signal(
            name="average temp", start=0, length=16, conversion=conv, is_signed=True
        )
    )
    signals.append(
        can.signal.Signal(
            name="low temp", start=16, length=16, conversion=conv, is_signed=True
        )
    )
    signals.append(
        can.signal.Signal(
            name="high temp", start=32, length=16, conversion=conv, is_signed=True
        )
    )
    return signals, length

def get_bms_status_signals():
    signals = []
    length = 6
    signals.append(can.signal.Signal(name="state", start=0, length=8))
    signals.append(can.signal.Signal(name="overvoltage error", start=8, length=1))
    signals.append(can.signal.Signal(name="undervoltage error", start=9, length=1))
    signals.append(
        can.signal.Signal(name="total voltage high error", start=10, length=1)
    )
    signals.append(
        can.signal.Signal(name="discharge overcurrent error", start=11, length=1)
    )
    signals.append(
        can.signal.Signal(name="charge overcurrent error", start=12, length=1)
    )
    signals.append(
        can.signal.Signal(name="discharge overtemp error", start=13, length=1)
    )
    signals.append(can.signal.Signal(name="charge overtemp error", start=14, length=1))
    signals.append(can.signal.Signal(name="undertemp error", start=15, length=1))
    signals.append(can.signal.Signal(name="overtemp error", start=16, length=1))
    conv = conversion.LinearConversion(scale=(1 / 100), offset=0, is_float=False)
    signals.append(
        can.signal.Signal(
            name="current", start=24, length=16, is_signed=True, conversion=conv
        )
    )
    signals.append(
        can.signal.Signal(name="shutdown g above threshold error", start=40, length=1)
    )
    signals.append(
        can.signal.Signal(name="shutdown h above threshold error", start=41, length=1)
    )
    return signals, length

def get_bms_voltage_signals():
    
    signals = []
    length = 8
    conv = conversion.LinearConversion(scale=(1 / 10000), offset=0, is_float=False)
    conv_100 = conversion.LinearConversion(scale=(1 / 100), offset=0, is_float=False)
    signals.append(
        can.signal.Signal(name="average voltage", start=0, length=16, conversion=conv)
    )
    signals.append(
        can.signal.Signal(name="low voltage", start=16, length=16, conversion=conv)
    )
    signals.append(
        can.signal.Signal(name="high voltage", start=32, length=16, conversion=conv)
    )
    signals.append(
        can.signal.Signal(
            name="total voltage", start=48, length=16, conversion=conv_100
        )
    )
    return signals, length

def get_ccu_status_signals():
    signals = []
    length = 1
    signals.append(can.signal.Signal(name="charger enabled", start=0, length=1))
    return signals, length

def get_charger_configure_signals():
    signals = []
    length = 5
    signals.append(
        can.signal.Signal(name="max charging voltage high", start=0, length=8)
    )
    signals.append(
        can.signal.Signal(name="max charging voltage low", start=8, length=8)
    )
    signals.append(
        can.signal.Signal(name="max charging current high", start=16, length=8)
    )
    signals.append(
        can.signal.Signal(name="max charging current low", start=24, length=8)
    )
    signals.append(can.signal.Signal(name="control", start=32, length=8))
    return signals, length

def get_charger_data_signals():
    signals = []
    length = 7
    signals.append(can.signal.Signal(name="output dc voltage high", start=0, length=8))
    signals.append(can.signal.Signal(name="output dc voltage low", start=8, length=8))
    signals.append(can.signal.Signal(name="output current high", start=16, length=8))
    signals.append(can.signal.Signal(name="output current low", start=24, length=8))
    signals.append(can.signal.Signal(name="flags", start=32, length=8))
    signals.append(can.signal.Signal(name="input ac voltage high", start=40, length=8))
    signals.append(can.signal.Signal(name="input ac voltage low", start=48, length=8))
    return signals, length

def get_dashboard_status_signals():
    signals = []
    length = 7
    signals.append(can.signal.Signal(name="start button", start=0, length=1))
    signals.append(can.signal.Signal(name="buzzer active", start=1, length=1))
    signals.append(can.signal.Signal(name="ssok above threshold", start=2, length=1))
    # why is this a dash signal?
    signals.append(
        can.signal.Signal(name="shutdown h above threshold", start=3, length=1)
    )

    signals.append(can.signal.Signal(name="mark button", start=8, length=1))
    signals.append(can.signal.Signal(name="mode button", start=9, length=1))
    signals.append(
        can.signal.Signal(name="motor controller cycle button", start=10, length=1)
    )
    signals.append(can.signal.Signal(name="launch ctrl button ", start=11, length=1))
    signals.append(can.signal.Signal(name="torque mode button", start=12, length=1))
    signals.append(can.signal.Signal(name="led dimmer button", start=13, length=1))

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
        can.signal.Signal(name="dial state", start=16, length=8, conversion=choice_conv)
    )

    signals.append(
        can.signal.Signal(name="ams led", start=24, length=2, conversion=led_choices)
    )
    signals.append(
        can.signal.Signal(name="imd led", start=26, length=2, conversion=led_choices)
    )
    signals.append(
        can.signal.Signal(name="mode led", start=28, length=2, conversion=led_choices)
    )
    signals.append(
        can.signal.Signal(
            name="motor controller error led",
            start=30,
            length=2,
            conversion=led_choices,
        )
    )
    signals.append(
        can.signal.Signal(
            name="start status led", start=32, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(
            name="inertia status led", start=34, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(
            name="mechanical brake led", start=36, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(
            name="gen purp led", start=38, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(name="bots led", start=40, length=2, conversion=led_choices)
    )
    signals.append(
        can.signal.Signal(
            name="cockpit brb led", start=42, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(
            name="crit charge led", start=44, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(name="glv led", start=46, length=2, conversion=led_choices)
    )
    signals.append(
        can.signal.Signal(
            name="launch control led", start=48, length=2, conversion=led_choices
        )
    )
    return signals, length

def get_mc_energy_signals():
    signals = []
    length = 8
    signals.append(
        can.signal.Signal(name="dc bus voltage", start=0, length=16)
    )
    signals.append(
        can.signal.Signal(name="motor power", start=16, length=32)
    )
    signals.append(
        can.signal.Signal(name="feedback torque", start=48, length=16, is_signed=True)
    )
    return signals, length

# TODO conversions for units
def get_mc_setpoints_commands_signals():
    signals = []
    length = 8
    signals.append(
        can.signal.Signal(name="inverter enable", start=8, length=1)
    )
    signals.append(
        can.signal.Signal(name="hv enable", start=9, length=1)
    )
    signals.append(
        can.signal.Signal(name="driver enable", start=10, length=1)
    )
    signals.append(
        can.signal.Signal(name="remove error", start=11, length=1)
    )
    signals.append(
        can.signal.Signal(name="speed setpoint rpm", start=16, length=16, is_signed=True)
    )
    signals.append(
        can.signal.Signal(name="positive torque limit", start=32, length=16, is_signed=True)
    )
    signals.append(
        can.signal.Signal(name="negative torque limit", start=48, length=16, is_signed=True)
    )
    return signals, length

# TODO verify this one, idk if its signed or not. it should be signed since you can command negative torque
def get_mc_torque_command_signals():
    signals = []
    length = 2
    signals.append(
        can.signal.Signal(name="torque command", start=0, length=16, is_signed=True)
    )
    return signals, length
def get_mc_status_signals():
    signals = []
    length = 8
    signals.append(
        can.signal.Signal(name="system ready", start=8, length=1)
    )
    signals.append(
        can.signal.Signal(name="error", start=9, length=1)
    )
    signals.append(
        can.signal.Signal(name="warning", start=10, length=1)
    )
    signals.append(
        can.signal.Signal(name="quit dc on", start=11, length=1)
    )
    signals.append(
        can.signal.Signal(name="dc on", start=12, length=1)
    )
    signals.append(
        can.signal.Signal(name="quit inverter on", start=13, length=1)
    )
    signals.append(
        can.signal.Signal(name="inverter on", start=14, length=1)
    )
    signals.append(
        can.signal.Signal(name="derating on", start=15, length=1)
    )
    signals.append(
        can.signal.Signal(name="speed rpm", start=16, length=16, is_signed=True)
    )
    signals.append(
        can.signal.Signal(name="torque current", start=32, length=16, is_signed=True)
    )
    signals.append(
        can.signal.Signal(name="magnetizing current", start=48, length=16, is_signed=True)
    )
    return signals, length

def get_mc_temp_signals():
    signals = []
    conv_10 = conversion.LinearConversion(scale=(1 / 10), offset=0, is_float=False)
    length = 8
    signals.append(
        can.signal.Signal(name="motor temp", start=0, length=16, is_signed=True, conversion=conv_10)
    )
    signals.append(
        can.signal.Signal(name="inverter temp", start=16, length=16, is_signed=True, conversion=conv_10)
    )
    signals.append(
        can.signal.Signal(name="diagnostic number", start=32, length=16)
    )
    signals.append(
        can.signal.Signal(name="igbt temp", start=48, length=16, is_signed=True, conversion=conv_10)
    )
    
    return signals, length
# TODO make this big endian, the cantools lib seems to be not handling big endian packets correctly
def get_energy_meter_measurement_signals():
    signals = []
    conv = conversion.LinearConversion(scale=(1 / 65536), offset=0, is_float=False)
    length = 8
    signals.append(
        can.signal.Signal(name="voltage", start=0, length=32, conversion=conv)
    )
    signals.append(
        can.signal.Signal(name="current", start=32, length=32, conversion=conv)
    )
    
    return signals, length

# TODO use these gain signals in the conversion?
def get_energy_meter_status_signals():
    signals = []
    conv = conversion.LinearConversion(scale=(1 / 65536), offset=0, is_float=False)
    length = 8
    signals.append(
        can.signal.Signal(name="voltage gain", start=0, length=4)
    )
    signals.append(
        can.signal.Signal(name="current gain", start=4, length=4)
    )
    signals.append(
        can.signal.Signal(name="overvoltage error", start=8, length=1)
    )
    signals.append(
        can.signal.Signal(name="overpower error", start=9, length=1)
    )
    signals.append(
        can.signal.Signal(name="logging", start=10, length=1)
    )
    return signals, length

# TODO units and conversions
def get_mcu_analog_signals():
    signals = []
    length = 8
    signals.append(
        can.signal.Signal(name="steering_1", start=0, length=16, is_signed=True)
    )
    signals.append(
        can.signal.Signal(name="steering_2", start=16, length=16)
    )
    signals.append(
        can.signal.Signal(name="hall effect current", start=32, length=16, is_signed=True)
    )
    signals.append(
        can.signal.Signal(name="glv battery voltage", start=48, length=16)
    )
    return signals, length

def get_mcu_front_potentiometer_signals():
    signals = []
    length = 6
    signals.append(
        can.signal.Signal(name="pot_1", start=0, length=16)
    )
    signals.append(
        can.signal.Signal(name="pot_2", start=16, length=16)
    )
    signals.append(
        can.signal.Signal(name="pot_3", start=32, length=16)
    )
    
    return signals, length

def get_mcu_rear_potentiometer_signals():
    signals = []
    length = 6
    signals.append(
        can.signal.Signal(name="pot_4", start=0, length=16)
    )
    signals.append(
        can.signal.Signal(name="pot_5", start=16, length=16)
    )
    signals.append(
        can.signal.Signal(name="pot_6", start=32, length=16)
    )
    return signals, length

def get_mcu_load_cell_signals():
    signals = []
    length = 8
    signals.append(
        can.signal.Signal(name="front left load cell lbs", start=0, length=16)
    )
    signals.append(
        can.signal.Signal(name="front right load cell lbs", start=16, length=16)
    )
    signals.append(
        can.signal.Signal(name="rear left load cell lbs", start=32, length=16)
    )
    signals.append(
        can.signal.Signal(name="rear right load cell lbs", start=48, length=16)
    )
    return signals, length

def get_mcu_pedals_signals():
    signals = []
    length = 8
    signals.append(
        can.signal.Signal(name="accel pedal 1", start=0, length=16)
    )
    signals.append(
        can.signal.Signal(name="accel pedal 2", start=16, length=16)
    )
    signals.append(
        can.signal.Signal(name="brake pedal 1", start=32, length=16)
    )
    signals.append(
        can.signal.Signal(name="brake pedal 2", start=48, length=16)
    )
    return signals, length

def get_mcu_status_signals():
    signals = []
    length = 8
    ecu_states = conversion.NamedSignalConversion(
        scale=1,
        offset=0,
        choices={
            0: "STARTUP",
            1: "TRACTIVE_SYSTEM_NOT_ACTIVE",
            2: "TRACTIVE_SYSTEM_ACTIVE",
            3: "ENABLING_INVERTER",
            4: "WAITING_READY_TO_DRIVE_SOUND",
            5: "READY_TO_DRIVE",
        },
        is_float=False,
    )
    
    signals.append(
        can.signal.Signal(name="imd ok high", start=0, length=1)
    )
    signals.append(
        can.signal.Signal(name="shutdown b above threshold", start=1, length=1)
    )
    signals.append(
        can.signal.Signal(name="bms ok high", start=2, length=1)
    )
    signals.append(
        can.signal.Signal(name="shutdown c above threshold", start=3, length=1)
    )
    signals.append(
        can.signal.Signal(name="bspd ok high", start=4, length=1)
    )
    signals.append(
        can.signal.Signal(name="shutdown d above threshold", start=5, length=1)
    )
    signals.append(
        can.signal.Signal(name="shoftware ok high", start=6, length=1)
    )
    signals.append(
        can.signal.Signal(name="shutdown e above threshold", start=7, length=1)
    )
    

    signals.append(
        can.signal.Signal(name="mechanical brake active", start=8, length=1)
    )
    signals.append(
        can.signal.Signal(name="no accel implausability", start=9, length=1)
    )
    signals.append(
        can.signal.Signal(name="no brake implausability", start=10, length=1)
    )
    signals.append(
        can.signal.Signal(name="brake pedal active", start=11, length=1)
    )
    signals.append(
        can.signal.Signal(name="bspd current high", start=12, length=1)
    )
    signals.append(
        can.signal.Signal(name="bspd brake high", start=13, length=1)
    )
    signals.append(
        can.signal.Signal(name="no accel or brake implausability", start=14, length=1)
    )

    signals.append(
        can.signal.Signal(name="ecu state", start=16, length=3, conversion=ecu_states)
    )
    signals.append(
        can.signal.Signal(name="inverter error", start=19, length=1)
    )
    signals.append(
        can.signal.Signal(name="energy meter present", start=20, length=1)
    )
    signals.append(
        can.signal.Signal(name="activate buzzer", start=21, length=1)
    )
    signals.append(
        can.signal.Signal(name="software ok", start=22, length=1)
    )
    signals.append(
        can.signal.Signal(name="launch control active", start=23, length=1)
    )
    signals.append(
        can.signal.Signal(name="pack charge critical", start=24, length=2)
    )
    signals.append(
        can.signal.Signal(name="max torque", start=32, length=8)
    )
    # TODO make enum
    signals.append(
        can.signal.Signal(name="torque mode", start=40, length=8)
    )
    conv_100 = conversion.LinearConversion(scale=(1 / 100), offset=0, is_float=False)
    signals.append(
        can.signal.Signal(name="distance traveled m", start=48, length=16, conversion=conv_100)
    )
    return signals, length


def get_sab_front_readings_signals():
    signals = []
    length = 4
    conv_1000 = conversion.LinearConversion(scale=(1 / 1000), offset=0, is_float=False)
    signals.append(
        can.signal.Signal(name="front left linear suspension mm", start=0, length=16, conversion=conv_1000)
    )
    signals.append(
        can.signal.Signal(name="front right linear suspension mm", start=16, length=16, conversion=conv_1000)
    )
    
    return signals, length

def get_sab_rear_readings_signals():
    signals = []
    length = 8
    conv_1000 = conversion.LinearConversion(scale=(1 / 1000), offset=0, is_float=False)
    signals.append(
        can.signal.Signal(name="cooling loop fluid temp C", start=0, length=16, conversion=conv_1000)
    )
    signals.append(
        can.signal.Signal(name="ambient air tem", start=16, length=16, conversion=conv_1000)
    )
    signals.append(
        can.signal.Signal(name="ambient air tem", start=32, length=16, conversion=conv_1000)
    )
    signals.append(
        can.signal.Signal(name="back left linear suspension mm", start=48, length=16, conversion=conv_1000)
    )
    signals.append(
        can.signal.Signal(name="back right linear suspension mm", start=64, length=16, conversion=conv_1000)
    )
    return signals, length