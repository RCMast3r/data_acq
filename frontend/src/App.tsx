import React, {useState} from 'react';
import './App.css';
import {StartStopButton} from "./Components/StartStopButton";
import {PageTitle} from "./Components/PageTitle";
import {TextForm} from "./Components/TextForm";
import {DropdownForm} from "./Components/DropdownForm";
import {OffloadButton} from "./OffloadButton";

const drivers = ["Driver 1", "Driver 2", "Driver 3"]
const tracks = ["Track 1", "Track 2", "Track 3"]
const events = ["Event 1", "Event 2", "Event 3"]

/**
 * NOTE: Check cloud webserver whenever editing this file
 */

function App() {
    const [driverInput, setDriverInput] = useState(drivers[0])
    const [trackNameInput, setTrackNameInput] = useState(tracks[0])
    const [eventTypeInput, setEventTypeInput] = useState(events[0])
    const [drivetrainTypeInput, setDrivetrainTypeInput] = useState("")
    const [massInput, setMassInput] = useState("")
    const [wheelbaseInput, setWheelbaseInput] = useState("")
    const [firmwareRevInput, setFirmwareRevInput] = useState("")

    const [recording, setRecording] = useState(false)

    return (
        <div className={"flex flex-col gap-4 items-center justify-center"}>
            <div className={"flex"}>
                <PageTitle/>
            </div>

            {/*<DropdownForm title={"Driver"} type={"driver"} data={driverInput} setData={setDriverInput} recording={recording}/>*/}
            <TextForm title={"Driver"} isNum={false} data={driverInput} setData={setDriverInput} recording={recording}/>
            <TextForm title={"Track Name"} isNum={false} data={trackNameInput} setData={setTrackNameInput} recording={recording}/>
            <TextForm title={"Event Type"} isNum={false} data={eventTypeInput} setData={setEventTypeInput} recording={recording}/>
            <TextForm title={"Drivetrain"} isNum={false} data={drivetrainTypeInput} setData={setDrivetrainTypeInput} recording={recording}/>
            <TextForm title={"Mass"} isNum={true} data={massInput} setData={setMassInput} recording={recording}/>
            <TextForm title={"Wheelbase"} isNum={true} data={wheelbaseInput} setData={setWheelbaseInput} recording={recording}/>
            <TextForm title={"Firmware Rev"} isNum={false} data={firmwareRevInput} setData={setFirmwareRevInput} recording={recording}/>

            <div className={"flex"}>
                <StartStopButton recording={recording} setRecording={setRecording} driverInput={driverInput} trackNameInput={trackNameInput} eventTypeInput={eventTypeInput} drivetrainTypeInput={drivetrainTypeInput} massInput={massInput} wheelbaseInput={wheelbaseInput} firmwareRevInput={firmwareRevInput}/>
            </div>

            <OffloadButton/>
        </div>
    );
}

export default App;
