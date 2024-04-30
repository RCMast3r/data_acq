import React, {useEffect, useState} from 'react';
import {getDefaultData} from "../Util/DataUtil";
import {getURL} from "../Util/ServerAddrUtil";
import {EditModeToggle} from "../Components/EditModeToggle";
import {AddrToggle} from "../Components/AddrToggle";
import {PageTitle} from "../Components/PageTitle";
import {Field} from "../Components/Field";
import {StartStopButton} from "../Components/StartStopButton";
import {OffloadButton} from "../Components/OffloadButton";

export function MCAPRecorder({}) {

    const [useLocalhost, setUseLocalhost] = React.useState(false)
    const [fields, setFields] = useState([])
    const [data, setData] = useState([])
    const [recording, setRecording] = useState(false)

    useEffect(() => {
        updateFields().then(fields => {
            setFields(fields)
            setData(getDefaultData(fields))
        })
    }, [useLocalhost])

    async function updateFields() {
//        const fetchResponse = await fetch(getURL('fields', useLocalhost), {
//            method: 'GET',
//            headers: {
//                Accept: 'application/json',
//                'Content-Type': 'application/json'
//            }
//        })
//        const json = await fetchResponse.text()
        const json = '[{"name":"driver","displayName":"Driver","type":"string","automatic":false,"options":["Shayan","Ryan"]},{"name":"testingGoal","displayName":"Testing Goal","type":"string","automatic":false,"options":[]},{"name":"eventType","displayName":"Event Type","type":"string","automatic":false,"options":["Skidpad","Acceleration","Hairpin","SCC Autocross"]},{"name":"startTime","displayName":"Start Time & Date","type":"string","automatic":false,"options":[]},{"name":"endTime","displayName":"End Time & Date","type":"string","automatic":false,"options":[]},{"name":"location","displayName":"Location","type":"string","automatic":false,"options":[]},{"name":"conditions","displayName":"Conditions (ie dry, night time)","type":"string","automatic":false,"options":[]},{"name":"temperature","displayName":"Temperature (C)","type":"string","automatic":false,"options":[]},{"name":"aeroType","displayName":"Aero Type","type":"string","automatic":false,"options":[]},{"name":"MCUversion","displayName":"MCU Version","type":"string","automatic":false,"options":[]},{"name":"yawPIDValues","displayName":"Yaw PID Values","type":"pid","automatic":false,"options":[]},{"name":"TCSPIDValues","displayName":"TCS PID Values","type":"pid","automatic":false,"options":[]},{"name":"TCSEnable","displayName":"TCS Enabled","type":"boolean","automatic":false,"options":[]},{"name":"yawPIDEnable","displayName":"Yaw PID Enabled","type":"boolean","automatic":false,"options":[]},{"name":"launchEnable","displayName":"Launch Enabled","type":"boolean","automatic":false,"options":[]},{"name":"normForceEnable","displayName":"Norm Force Enabled","type":"boolean","automatic":false,"options":[]},{"name":"mechPowerLimEnable","displayName":"Mech Power Lim. Enabled","type":"boolean","automatic":false,"options":[]},{"name":"pidPowerLimEnable","displayName":"PID Power Lim. Enabled","type":"boolean","automatic":false,"options":[]},{"name":"notes","displayName":"Notes","type":"string","automatic":false,"options":[]},{"name":"errors","displayName":"Errors","type":"string","automatic":false,"options":[]}]'

        return JSON.parse(json)
    }

    return (
        <>
            <main>
                <div className={"flex flex-col gap-4 items-center justify-center pt-6"}>
                    <AddrToggle useLocalhost={useLocalhost} setUseLocalhost={setUseLocalhost}/>
                    <div className={"flex"}>
                        <PageTitle/>
                    </div>

                    <div className={"flex flex-col gap-4 items-center justify-center"}>
                        {fields.map((field, index) => <Field key={field.id} fields={fields} data={data}
                                                             setData={setData} index={index} recording={recording}
                                                             serverAddr={'http://192.168.203.1'}/>)}
                    </div>

                </div>
            </main>
            <footer className={"sticky bottom-0 bg-base-100"}>
                <div className={"flex flex-col gap-4 items-center justify-center pt-6"}>
                    <StartStopButton fields={fields} data={data} recording={recording} setRecording={setRecording}
                                     serverAddr={'http://192.168.203.1'}/>
                    <OffloadButton/>
                </div>
            </footer>

        </>
    )
}