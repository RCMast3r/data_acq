import React, {useEffect, useState} from 'react';
import './App.css';
import {StartStopButton} from "./Components/StartStopButton";
import {PageTitle} from "./Components/PageTitle";
import {TextForm} from "./Components/FieldComponents/TextForm";
import {OffloadButton} from "./OffloadButton";
import {Field} from "./Components/Field";
import {AddrToggle} from "./Components/AddrToggle";

function App() {

    async function updateFields() {
         const fetchResponse = await fetch(serverAddr + '/fields', {
             method: 'GET',
             headers: {
                 Accept: 'application/json',
                 'Content-Type': 'application/json'
             }
         })
         const json = await fetchResponse.text()
        //const json = '[{"id":0,"name":"driver","displayName":"Driver","type":"string","required":true,"dropdown":false,"automatic":false},{"id":1,"name":"testingGoal","displayName":"Testing Goal","type":"string","required":false,"dropdown":false,"automatic":false},{"id":2,"name":"eventType","displayName":"Event Type","type":"string","required":false,"dropdown":true,"automatic":false},{"id":3,"name":"notes","displayName":"Notes","type":"string","required":false,"dropdown":false,"automatic":false},{"id":4,"name":"startTime","displayName":"Start Time/Date","type":"string","required":false,"dropdown":false,"automatic":false},{"id":5,"name":"endTime","displayName":"End Time/Date","type":"string","required":false,"dropdown":false,"automatic":false},{"id":6,"name":"location","displayName":"Location","type":"string","required":false,"dropdown":false,"automatic":false},{"id":7,"name":"conditions","displayName":"Conditions (ie dry, night time)","type":"string","required":false,"dropdown":false,"automatic":false},{"id":8,"name":"temperature","displayName":"Temperature (C)","type":"string","required":false,"dropdown":false,"automatic":false},{"id":9,"name":"aeroType","displayName":"Aero Type","type":"string","required":false,"dropdown":false,"automatic":false},{"id":10,"name":"MCUversion","displayName":"MCU Version","type":"string","required":false,"dropdown":false,"automatic":false},{"id":11,"name":"errors","displayName":"Errors","type":"string","required":false,"dropdown":false,"automatic":false},{"id":12,"name":"yawPIDValues","displayName":"Yaw Pid Values","type":"string","required":false,"dropdown":false,"automatic":false},{"id":13,"name":"TCSPIDValues","displayName":"TCS PID Values","type":"string","required":false,"dropdown":false,"automatic":false},{"id":14,"name":"TCSEnable","displayName":"TCS Enabled","type":"string","required":false,"dropdown":false,"automatic":false},{"id":15,"name":"yawPIDENable","displayName":"Yaw PID Enabled","type":"string","required":false,"dropdown":false,"automatic":false},{"id":16,"name":"launchEnable","displayName":"Launch Enabled","type":"string","required":false,"dropdown":false,"automatic":false},{"id":17,"name":"normForceEnable","displayName":"Norm Force Enabled","type":"string","required":false,"dropdown":false,"automatic":false},{"id":18,"name":"mechPowerLimEnable","displayName":"Mech Power Lim. Enabled","type":"string","required":false,"dropdown":false,"automatic":false},{"id":19,"name":"pidPowerLimEnable","displayName":"Pid Power Lim. Enabled","type":"string","required":false,"dropdown":false,"automatic":false}]'

        setFields(JSON.parse(json))
        setData(new Array(JSON.parse(json).length).fill(''))

        return JSON.parse(json)
    }

    const [serverAddr, setServerAddr] = useState("http://192.168.203.1:6969")


    const [fields, setFields] = useState([])
    const [data, setData] = useState([]);
    const [recording, setRecording] = useState(false)

    useEffect(() => {
        updateFields().then(fields => setFields(fields))
    }, [])

    useEffect(() => {
        updateFields().then(fields => setFields(fields))
    }, [serverAddr])

    return (
        <div className={"flex flex-col gap-4 items-center justify-center pt-6"}>
            <AddrToggle serverAddr={serverAddr} setServerAddr={setServerAddr}/>
            <div className={"flex"}>
                <PageTitle/>
            </div>

            <div className={"flex flex-col gap-4 items-center justify-center"}>
                {fields.map((field, index) => <Field key={field.id} fields={fields} data={data} setData={setData} index={index} recording={recording} serverAddr={serverAddr}/>)}
                {/*<StartStopButton recording={recording} setRecording={setRecording} driverInput={driverInput} trackNameInput={trackNameInput} eventTypeInput={eventTypeInput} drivetrainTypeInput={drivetrainTypeInput} massInput={massInput} wheelbaseInput={wheelbaseInput} firmwareRevInput={firmwareRevInput}/>*/}
            </div>

            <StartStopButton fields={fields} data={data} recording={recording} setRecording={setRecording} serverAddr={serverAddr}/>
            <OffloadButton/>
        </div>
    );
}

export default App;
