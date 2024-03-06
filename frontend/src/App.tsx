import React, {useState} from 'react';
import './App.css';
import {StartStopButton} from "./Components/StartStopButton";
import {PageTitle} from "./Components/PageTitle";
import {TextForm} from "./Components/TextForm";
import {DropdownForm} from "./Components/DropdownForm";

const drivers = ["Driver 1", "Driver 2", "Driver 3"]
const tracks = ["Track 1", "Track 2", "Track 3"]
const events = ["Event 1", "Event 2", "Event 3"]

function App() {
    //form data
    const [driverInput, setDriverInput] = useState(drivers[0])
    const [trackNameInput, setTrackNameInput] = useState(tracks[0])
    const [eventTypeInput, setEventTypeInput] = useState(events[0])
    const [carSetupIdInput, setCarSetupIdInput] = useState("")
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

            <DropdownForm title={"Driver"} options={drivers} data={driverInput} setData={setDriverInput} recording={recording}/>
            <DropdownForm title={"Track Name"} options={tracks} data={trackNameInput} setData={setTrackNameInput} recording={recording}/>
            <DropdownForm title={"Event Type"} options={events} data={eventTypeInput} setData={setEventTypeInput} recording={recording}/>
            <TextForm title={"Car Setup"} isNum={false} data={carSetupIdInput} setData={setCarSetupIdInput} recording={recording}/>
            <TextForm title={"Drivetrain"} isNum={false} data={drivetrainTypeInput} setData={setDrivetrainTypeInput} recording={recording}/>
            <TextForm title={"Mass"} isNum={true} data={massInput} setData={setMassInput} recording={recording}/>
            <TextForm title={"Wheelbase"} isNum={true} data={wheelbaseInput} setData={setWheelbaseInput} recording={recording}/>
            <TextForm title={"Firmware Rev"} isNum={false} data={firmwareRevInput} setData={setFirmwareRevInput} recording={recording}/>

            <div className={"flex"}>
                <StartStopButton recording={recording} setRecording={setRecording} driverInput={driverInput} trackNameInput={trackNameInput} eventTypeInput={eventTypeInput} carSetupIdInput={carSetupIdInput} drivetrainTypeInput={drivetrainTypeInput} massInput={massInput} wheelbaseInput={wheelbaseInput} firmwareRevInput={firmwareRevInput}/>
            </div>
        </div>
    );
}

export default App;
