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
            name="total_charge", start=0, length=32, conversion=ch_disch_conv, byte_order="little_endian"
        )
    )
    signals.append(
        can.signal.Signal(
            name="total_discharge",
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
    signals.append(can.signal.Signal(name="ic_id", start=4, length=4))
    signals.append(can.signal.Signal(name="group_id", start=0, length=4))
    i = 0
    num_of_voltages = 3
    # repeated signals for multiple voltages
    while i < num_of_voltages:
        start_bit = 8 + (i * 16)
        signals.append(
            can.signal.Signal(
                name="voltage_" + str(i), start=start_bit, length=16, conversion=conv
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
    signals.append(can.signal.Signal(name="ic_id", start=0, length=4))
    signals.append(can.signal.Signal(name="group_id", start=4, length=4))
    id = 0
    while id < 3:
        signals.append(
            can.signal.Signal(
                name="thermistor_id_" + str(id),
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
    signals.append(can.signal.Signal(name="ic_id", start=0, length=8))
    signals.append(
        can.signal.Signal(
            name="temp_0", start=8, length=16, conversion=conv, is_signed=True
        )
    )
    signals.append(
        can.signal.Signal(
            name="temp_1", start=24, length=16, conversion=conv, is_signed=True
        )
    )
    return signals, length

def get_bms_onboard_temperatures_signals():
    signals = []
    length = 6
    conv = conversion.LinearConversion(scale=(1 / 100), offset=0, is_float=False)
    signals.append(
        can.signal.Signal(
            name="average_temp", start=0, length=16, conversion=conv, is_signed=True
        )
    )
    signals.append(
        can.signal.Signal(
            name="low_temp", start=16, length=16, conversion=conv, is_signed=True
        )
    )
    signals.append(
        can.signal.Signal(
            name="high_temp", start=32, length=16, conversion=conv, is_signed=True
        )
    )
    return signals, length

def get_bms_status_signals():
    signals = []
    length = 6
    signals.append(can.signal.Signal(name="state", start=0, length=8))
    signals.append(can.signal.Signal(name="overvoltage_error", start=8, length=1))
    signals.append(can.signal.Signal(name="undervoltage_error", start=9, length=1))
    signals.append(
        can.signal.Signal(name="total voltage_high_error", start=10, length=1)
    )
    signals.append(
        can.signal.Signal(name="discharge_overcurrent_error", start=11, length=1)
    )
    signals.append(
        can.signal.Signal(name="charge_overcurrent_error", start=12, length=1)
    )
    signals.append(
        can.signal.Signal(name="discharge_overtemp_error", start=13, length=1)
    )
    signals.append(can.signal.Signal(name="charge_overtemp_error", start=14, length=1))
    signals.append(can.signal.Signal(name="undertemp_error", start=15, length=1))
    signals.append(can.signal.Signal(name="overtemp_error", start=16, length=1))
    conv = conversion.LinearConversion(scale=(1 / 100), offset=0, is_float=False)
    signals.append(
        can.signal.Signal(
            name="current", start=24, length=16, is_signed=True, conversion=conv
        )
    )
    signals.append(
        can.signal.Signal(name="shutdown g above_threshold_error", start=40, length=1)
    )
    signals.append(
        can.signal.Signal(name="shutdown h above_threshold_error", start=41, length=1)
    )
    return signals, length

def get_bms_voltage_signals():
    
    signals = []
    length = 8
    conv = conversion.LinearConversion(scale=(1 / 10000), offset=0, is_float=False)
    conv_100 = conversion.LinearConversion(scale=(1 / 100), offset=0, is_float=False)
    signals.append(
        can.signal.Signal(name="average_voltage", start=0, length=16, conversion=conv)
    )
    signals.append(
        can.signal.Signal(name="low_voltage", start=16, length=16, conversion=conv)
    )
    signals.append(
        can.signal.Signal(name="high_voltage", start=32, length=16, conversion=conv)
    )
    signals.append(
        can.signal.Signal(
            name="total_voltage", start=48, length=16, conversion=conv_100
        )
    )
    return signals, length

def get_ccu_status_signals():
    signals = []
    length = 1
    signals.append(can.signal.Signal(name="charger_enabled", start=0, length=1))
    return signals, length

def get_charger_configure_signals():
    signals = []
    length = 5
    signals.append(
        can.signal.Signal(name="max charging_voltage_high", start=0, length=8)
    )
    signals.append(
        can.signal.Signal(name="max charging_voltage_low", start=8, length=8)
    )
    signals.append(
        can.signal.Signal(name="max charging_current_high", start=16, length=8)
    )
    signals.append(
        can.signal.Signal(name="max charging_current_low", start=24, length=8)
    )
    signals.append(can.signal.Signal(name="control", start=32, length=8))
    return signals, length

def get_charger_data_signals():
    signals = []
    length = 7
    signals.append(can.signal.Signal(name="output dc_voltage_high", start=0, length=8))
    signals.append(can.signal.Signal(name="output dc_voltage_low", start=8, length=8))
    signals.append(can.signal.Signal(name="output_current_high", start=16, length=8))
    signals.append(can.signal.Signal(name="output_current_low", start=24, length=8))
    signals.append(can.signal.Signal(name="flags", start=32, length=8))
    signals.append(can.signal.Signal(name="input ac_voltage_high", start=40, length=8))
    signals.append(can.signal.Signal(name="input ac_voltage_low", start=48, length=8))
    return signals, length

def get_dashboard_status_signals():
    signals = []
    length = 7
    signals.append(can.signal.Signal(name="start_button", start=0, length=1))
    signals.append(can.signal.Signal(name="buzzer_active", start=1, length=1))
    signals.append(can.signal.Signal(name="ssok_above_threshold", start=2, length=1))
    # why is this a dash signal?
    signals.append(
        can.signal.Signal(name="shutdown h_above_threshold", start=3, length=1)
    )

    signals.append(can.signal.Signal(name="mark_button", start=8, length=1))
    signals.append(can.signal.Signal(name="mode_button", start=9, length=1))
    signals.append(
        can.signal.Signal(name="motor controller_cycle_button", start=10, length=1)
    )
    signals.append(can.signal.Signal(name="launch ctrl_button_", start=11, length=1))
    signals.append(can.signal.Signal(name="torque_mode_button", start=12, length=1))
    signals.append(can.signal.Signal(name="led_dimmer_button", start=13, length=1))

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
        can.signal.Signal(name="dial_state", start=16, length=8, conversion=choice_conv)
    )

    signals.append(
        can.signal.Signal(name="ams_led", start=24, length=2, conversion=led_choices)
    )
    signals.append(
        can.signal.Signal(name="imd_led", start=26, length=2, conversion=led_choices)
    )
    signals.append(
        can.signal.Signal(name="mode_led", start=28, length=2, conversion=led_choices)
    )
    signals.append(
        can.signal.Signal(
            name="motor controller_error_led",
            start=30,
            length=2,
            conversion=led_choices,
        )
    )
    signals.append(
        can.signal.Signal(
            name="start_status_led", start=32, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(
            name="inertia_status_led", start=34, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(
            name="mechanical_brake_led", start=36, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(
            name="gen_purp_led", start=38, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(name="bots_led", start=40, length=2, conversion=led_choices)
    )
    signals.append(
        can.signal.Signal(
            name="cockpit_brb_led", start=42, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(
            name="crit_charge_led", start=44, length=2, conversion=led_choices
        )
    )
    signals.append(
        can.signal.Signal(name="glv_led", start=46, length=2, conversion=led_choices)
    )
    signals.append(
        can.signal.Signal(
            name="launch_control_led", start=48, length=2, conversion=led_choices
        )
    )
    return signals, length

def get_mc_energy_signals():
    signals = []
    length = 8
    signals.append(
        can.signal.Signal(name="dc_bus_voltage", start=0, length=16)
    )
    signals.append(
        can.signal.Signal(name="motor_power", start=16, length=32)
    )
    signals.append(
        can.signal.Signal(name="feedback_torque", start=48, length=16, is_signed=True)
    )
    return signals, length

# TODO conversions for units
def get_mc_setpoints_commands_signals():
    signals = []
    length = 8
    signals.append(
        can.signal.Signal(name="inverter_enable", start=8, length=1)
    )
    signals.append(
        can.signal.Signal(name="hv_enable", start=9, length=1)
    )
    signals.append(
        can.signal.Signal(name="driver_enable", start=10, length=1)
    )
    signals.append(
        can.signal.Signal(name="remove_error", start=11, length=1)
    )
    signals.append(
        can.signal.Signal(name="speed_setpoint_rpm", start=16, length=16, is_signed=True)
    )
    signals.append(
        can.signal.Signal(name="positive_torque_limit", start=32, length=16, is_signed=True)
    )
    signals.append(
        can.signal.Signal(name="negative_torque_limit", start=48, length=16, is_signed=True)
    )
    return signals, length

# TODO verify this one, idk if its signed or not. it should be signed since you can command negative torque
def get_mc_torque_command_signals():
    signals = []
    length = 2
    signals.append(
        can.signal.Signal(name="torque_command", start=0, length=16, is_signed=True)
    )
    return signals, length
def get_mc_status_signals():
    signals = []
    length = 8
    signals.append(
        can.signal.Signal(name="system_ready", start=8, length=1)
    )
    signals.append(
        can.signal.Signal(name="error", start=9, length=1)
    )
    signals.append(
        can.signal.Signal(name="warning", start=10, length=1)
    )
    signals.append(
        can.signal.Signal(name="quit_dc_on", start=11, length=1)
    )
    signals.append(
        can.signal.Signal(name="dc_on", start=12, length=1)
    )
    signals.append(
        can.signal.Signal(name="quit_inverter_on", start=13, length=1)
    )
    signals.append(
        can.signal.Signal(name="inverter_on", start=14, length=1)
    )
    signals.append(
        can.signal.Signal(name="derating_on", start=15, length=1)
    )
    signals.append(
        can.signal.Signal(name="speed_rpm", start=16, length=16, is_signed=True)
    )
    signals.append(
        can.signal.Signal(name="torque_current", start=32, length=16, is_signed=True)
    )
    signals.append(
        can.signal.Signal(name="magnetizing_current", start=48, length=16, is_signed=True)
    )
    return signals, length

def get_mc_temp_signals():
    signals = []
    conv_10 = conversion.LinearConversion(scale=(1 / 10), offset=0, is_float=False)
    length = 8
    signals.append(
        can.signal.Signal(name="motor_temp", start=0, length=16, is_signed=True, conversion=conv_10)
    )
    signals.append(
        can.signal.Signal(name="inverter_temp", start=16, length=16, is_signed=True, conversion=conv_10)
    )
    signals.append(
        can.signal.Signal(name="diagnostic_number", start=32, length=16)
    )
    signals.append(
        can.signal.Signal(name="igbt_temp", start=48, length=16, is_signed=True, conversion=conv_10)
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
        can.signal.Signal(name="voltage_gain", start=0, length=4)
    )
    signals.append(
        can.signal.Signal(name="current_gain", start=4, length=4)
    )
    signals.append(
        can.signal.Signal(name="overvoltage_error", start=8, length=1)
    )
    signals.append(
        can.signal.Signal(name="overpower_error", start=9, length=1)
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
        can.signal.Signal(name="hall_effect_current", start=32, length=16, is_signed=True)
    )
    signals.append(
        can.signal.Signal(name="glv_battery_voltage", start=48, length=16)
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
        can.signal.Signal(name="front left load_cell_lbs", start=0, length=16)
    )
    signals.append(
        can.signal.Signal(name="front right load_cell_lbs", start=16, length=16)
    )
    signals.append(
        can.signal.Signal(name="rear left load_cell_lbs", start=32, length=16)
    )
    signals.append(
        can.signal.Signal(name="rear right load_cell_lbs", start=48, length=16)
    )
    return signals, length

def get_mcu_pedals_signals():
    signals = []
    length = 8
    signals.append(
        can.signal.Signal(name="accel_pedal_1", start=0, length=16)
    )
    signals.append(
        can.signal.Signal(name="accel_pedal_2", start=16, length=16)
    )
    signals.append(
        can.signal.Signal(name="brake_pedal_1", start=32, length=16)
    )
    signals.append(
        can.signal.Signal(name="brake_pedal_2", start=48, length=16)
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
        can.signal.Signal(name="imd_ok_high", start=0, length=1)
    )
    signals.append(
        can.signal.Signal(name="shutdown b_above_threshold", start=1, length=1)
    )
    signals.append(
        can.signal.Signal(name="bms_ok_high", start=2, length=1)
    )
    signals.append(
        can.signal.Signal(name="shutdown c_above_threshold", start=3, length=1)
    )
    signals.append(
        can.signal.Signal(name="bspd_ok_high", start=4, length=1)
    )
    signals.append(
        can.signal.Signal(name="shutdown d_above_threshold", start=5, length=1)
    )
    signals.append(
        can.signal.Signal(name="shoftware_ok_high", start=6, length=1)
    )
    signals.append(
        can.signal.Signal(name="shutdown e_above_threshold", start=7, length=1)
    )
    

    signals.append(
        can.signal.Signal(name="mechanical_brake_active", start=8, length=1)
    )
    signals.append(
        can.signal.Signal(name="no_accel_implausability", start=9, length=1)
    )
    signals.append(
        can.signal.Signal(name="no_brake_implausability", start=10, length=1)
    )
    signals.append(
        can.signal.Signal(name="brake_pedal_active", start=11, length=1)
    )
    signals.append(
        can.signal.Signal(name="bspd_current_high", start=12, length=1)
    )
    signals.append(
        can.signal.Signal(name="bspd_brake_high", start=13, length=1)
    )
    signals.append(
        can.signal.Signal(name="no accel or_brake_implausability", start=14, length=1)
    )

    signals.append(
        can.signal.Signal(name="ecu_state", start=16, length=3, conversion=ecu_states)
    )
    signals.append(
        can.signal.Signal(name="inverter_error", start=19, length=1)
    )
    signals.append(
        can.signal.Signal(name="energy_meter_present", start=20, length=1)
    )
    signals.append(
        can.signal.Signal(name="activate_buzzer", start=21, length=1)
    )
    signals.append(
        can.signal.Signal(name="software_ok", start=22, length=1)
    )
    signals.append(
        can.signal.Signal(name="launch_control_active", start=23, length=1)
    )
    signals.append(
        can.signal.Signal(name="pack_charge_critical", start=24, length=2)
    )
    signals.append(
        can.signal.Signal(name="max_torque", start=32, length=8)
    )
    # TODO make enum
    signals.append(
        can.signal.Signal(name="torque_mode", start=40, length=8)
    )
    conv_100 = conversion.LinearConversion(scale=(1 / 100), offset=0, is_float=False)
    signals.append(
        can.signal.Signal(name="distance_traveled_m", start=48, length=16, conversion=conv_100)
    )
    return signals, length


def get_sab_front_readings_signals():
    signals = []
    length = 4
    conv_1000 = conversion.LinearConversion(scale=(1 / 1000), offset=0, is_float=False)
    signals.append(
        can.signal.Signal(name="front left linear_suspension_mm", start=0, length=16, conversion=conv_1000)
    )
    signals.append(
        can.signal.Signal(name="front right linear_suspension_mm", start=16, length=16, conversion=conv_1000)
    )
    
    return signals, length

def get_sab_rear_readings_signals():
    signals = []
    length = 8
    conv_1000 = conversion.LinearConversion(scale=(1 / 1000), offset=0, is_float=False)
    signals.append(
        can.signal.Signal(name="cooling loop fluid_temp_C", start=0, length=16, conversion=conv_1000)
    )
    signals.append(
        can.signal.Signal(name="ambient_air_tem", start=16, length=16, conversion=conv_1000)
    )
    signals.append(
        can.signal.Signal(name="ambient_air_tem", start=32, length=16, conversion=conv_1000)
    )
    signals.append(
        can.signal.Signal(name="back left linear_suspension_mm", start=48, length=16, conversion=conv_1000)
    )
    signals.append(
        can.signal.Signal(name="back right linear_suspension_mm", start=64, length=16, conversion=conv_1000)
    )
    return signals, length