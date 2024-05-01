import React, {useEffect, useState} from 'react';
import {AddrToggle} from "../Components/AddrToggle";
import {PageTitle} from "../Components/PageTitle";
import {getURL} from "../Util/ServerAddrUtil";

export function EditSSOT({}) {

    const [useLocalhost, setUseLocalhost] = useState(false)
    const [metadata, setMetadata] = useState('')

    useEffect(() => {
        updateMetadata().then(metadata => setMetadata(metadata))
    }, [useLocalhost])

    async function updateMetadata() {
        let json;
        try {
            const fetchResponse = await fetch(getURL('fields', useLocalhost), {
                signal: AbortSignal.timeout(3000),
                method: 'GET',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json'
                }
            })
            json = await fetchResponse.text()
        } catch (e) {
            alert("WARNING: Using hardcoded fields")
            json = '[{"name":"driver","displayName":"Driver","type":"string","automatic":false,"options":["Shayan","Ryan"]},{"name":"testingGoal","displayName":"Testing Goal","type":"string","automatic":false,"options":[]},{"name":"eventType","displayName":"Event Type","type":"string","automatic":false,"options":["Skidpad","Acceleration","Hairpin","SCC Autocross"]},{"name":"startTime","displayName":"Start Time & Date","type":"string","automatic":false,"options":[]},{"name":"endTime","displayName":"End Time & Date","type":"string","automatic":false,"options":[]},{"name":"location","displayName":"Location","type":"string","automatic":false,"options":[]},{"name":"conditions","displayName":"Conditions (ie dry, night time)","type":"string","automatic":false,"options":[]},{"name":"temperature","displayName":"Temperature (C)","type":"string","automatic":false,"options":[]},{"name":"aeroType","displayName":"Aero Type","type":"string","automatic":false,"options":[]},{"name":"MCUversion","displayName":"MCU Version","type":"string","automatic":false,"options":[]},{"name":"yawPIDValues","displayName":"Yaw PID Values","type":"pid","automatic":false,"options":[]},{"name":"TCSPIDValues","displayName":"TCS PID Values","type":"pid","automatic":false,"options":[]},{"name":"TCSEnable","displayName":"TCS Enabled","type":"boolean","automatic":false,"options":[]},{"name":"yawPIDEnable","displayName":"Yaw PID Enabled","type":"boolean","automatic":false,"options":[]},{"name":"launchEnable","displayName":"Launch Enabled","type":"boolean","automatic":false,"options":[]},{"name":"normForceEnable","displayName":"Norm Force Enabled","type":"boolean","automatic":false,"options":[]},{"name":"mechPowerLimEnable","displayName":"Mech Power Lim. Enabled","type":"boolean","automatic":false,"options":[]},{"name":"pidPowerLimEnable","displayName":"PID Power Lim. Enabled","type":"boolean","automatic":false,"options":[]},{"name":"notes","displayName":"Notes","type":"string","automatic":false,"options":[]},{"name":"errors","displayName":"Errors","type":"string","automatic":false,"options":[]}]'
        }
        return JSON.stringify(JSON.parse(json), null, 4)
    }
    
    async function saveMetadata() {
        try {
            const fetchResponse = await fetch(getURL('saveFields', useLocalhost), {
                method: 'GET',
                headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json'
                }
            })
        } catch (e) {
            alert(e)
        }
        
        updateMetadata().then(metadata => setMetadata(metadata))
    }

    return (
        <>
            <main>
                <div className={"flex flex-col gap-4 items-center justify-center pt-6"}>
                    <AddrToggle useLocalhost={useLocalhost} setUseLocalhost={setUseLocalhost}/>
                    <div className={"flex"}>
                        <PageTitle text={"Metadata Editor"}/>
                    </div>
                </div>

                <div className={"flex flex-col gap-4 items-center justify-center pt-6"}>
                    <textarea className={"textarea textarea-bordered w-80 h-[70dvh] resize-none"} value={metadata}
                              onChange={e => setMetadata(e.target.value)} wrap={'off'}></textarea>
                </div>
            </main>
            <footer className={"sticky bottom-0 bg-base-100"}>
                <div className={"flex flex-row gap-4 pt-6"}>
                    <div className={"grow w-max"}/>
                    <button className={"btn"} onClick={() => updateMetadata().then(metadata => setMetadata(metadata))}>
                        Reset
                    </button>
                    <button className={"btn btn-success"} onClick={saveMetadata}>
                        Save
                    </button>
                    <div className={"grow w-max"}/>
                </div>
            </footer>
        </>
    )

}