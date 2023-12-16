from cantools.database import *

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

def get_ccu_status_signals():
    signals = []
    signals.append(can.signal(name="charger enabled", start=0, length=1))
    return signals

def get_charger_configure_signals():
    signals = []
    signals.append(can.signal(name="max charging voltage high", start=0, length=8))
    signals.append(can.signal(name="max charging voltage low", start=8, length=8))
    signals.append(can.signal(name="max charging current high", start=16, length=8))
    signals.append(can.signal(name="max charging current low", start=24, length=8))
    signals.append(can.signal(name="control", start=32, length=8))
    return signals

def get_charger_data_signals():
    signals = []
    signals.append(can.signal(name="output dc voltage high", start=0, length=8))
    signals.append(can.signal(name="output dc voltage low", start=8, length=8))
    signals.append(can.signal(name="output current high", start=16, length=8))
    signals.append(can.signal(name="output current low", start=24, length=8))
    signals.append(can.signal(name="flags", start=32, length=8))
    signals.append(can.signal(name="input ac voltage high", start=40, length=8))
    signals.append(can.signal(name="input ac voltage low", start=48, length=8))
    return signals

def get_dashboard_status_signals():
    signals = []
    signals.append(can.signal(name="start button", start=0, length=1))
    signals.append(can.signal(name="buzzer active", start=1, length=1))
    signals.append(can.signal(name="ssok above threshold", start=2, length=1))
    # why is this a dash signal?
    signals.append(can.signal(name="shutdown h above threshold", start=3, length=1))

    signals.append(can.signal(name="mark button", start=8, length=1))
    signals.append(can.signal(name="mode button", start=9, length=1))
    signals.append(can.signal(name="motor controller cycle button", start=10, length=1))
    signals.append(can.signal(name="launch ctrl button ", start=11, length=1))
    signals.append(can.signal(name="torque mode button", start=12, length=1))
    signals.append(can.signal(name="led dimmer button", start=13, length=1))

    signals.append(
        can.signal(
            name="dial state",
            start=16,
            length=8,
            choices={
                0: "MODE_ONE",
                1: "MODE_TWO",
                2: "ACCELERATION_LAUNCH_CONTROL",
                3: "SKIDPAD",
                4: "AUTOCROSS",
                5: "ENDURANCE",
            },
        )
    )

    led_choices = {
        0: "OFF",
        1: "ON",
        2: "YELLOW",
        3: "RED",
    }
    signals.append(can.signal(name="ams led", start=24, length=2, choices=led_choices))
    signals.append(can.signal(name="imd led", start=26, length=2, choices=led_choices))
    signals.append(can.signal(name="mode led", start=28, length=2, choices=led_choices))
    signals.append(
        can.signal(
            name="motor controller error led", start=30, length=2, choices=led_choices
        )
    )
    signals.append(
        can.signal(name="start status led", start=32, length=2, choices=led_choices)
    )
    signals.append(
        can.signal(name="inertia status led", start=34, length=2, choices=led_choices)
    )
    signals.append(
        can.signal(name="mechanical brake led", start=36, length=2, choices=led_choices)
    )
    signals.append(
        can.signal(name="gen purp led", start=38, length=2, choices=led_choices)
    )
    signals.append(can.signal(name="bots led", start=40, length=2, choices=led_choices))
    signals.append(
        can.signal(name="cockpit brb led", start=42, length=2, choices=led_choices)
    )
    signals.append(
        can.signal(name="crit charge led", start=44, length=2, choices=led_choices)
    )
    signals.append(can.signal(name="glv led", start=46, length=2, choices=led_choices))
    signals.append(
        can.signal(name="launch control led", start=48, length=2, choices=led_choices)
    )
    return signals
