import React from "react";
import { useState } from "react";
import {getURL} from "../Util/ServerAddrUtil";
import {getFormattedDate} from "../Util/DateUtil";

export function StartStopButton({fields, data, recording, setRecording, useLocalhost}) {

    const [time, setTime] = useState("");
    let waitingForResponse = false;

    function getButtonStyle() {
        return recording ? "btn btn-error" : "btn btn-success"
    }

    function getButtonText() {
        return recording ? "Stop Recording" : "Start Recording"
    }

    function isDisabled() {
        return waitingForResponse
    }


    async function stopRecording() {
        if(waitingForResponse) {
            return false
        }
        waitingForResponse = true
        const fetchResponse = await fetch(getURL('stop', useLocalhost), {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            }
        })
        waitingForResponse = false
        const status = fetchResponse.status
        if (status === 200) {
            alert("Stopped writing to " + time + ".mcap");
        }
        return status === 200
    }

    async function startRecording() {
        if(waitingForResponse) {
            return false
        }

        let body = "{ "
        
        for(let i = 0; i < data.length; i++) {
            body += '"' + fields[i].name + '":' + JSON.stringify(data[i])
            body += ', '
        }

        // Creating the formatted date string
        const formattedDate = getFormattedDate()
        setTime(formattedDate)
        body += '"time":"' + formattedDate+'"'
        body += " }"
        console.log(body)
        const fetchResponse = await fetch(await fetch(getURL('start', useLocalhost)), {
            method: 'POST',
            body: body,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            }
        })

        waitingForResponse = false
        const status = fetchResponse.status
        if (status === 200) {
            setTime(formattedDate)
        }
        return status === 200
    }

    async function toggleRecording() {
        if (recording) {
            const stoppedRecording = await stopRecording()
            if (stoppedRecording) {
                setRecording(false)
            }
        } else {
            const startedRecording = await startRecording()
            if (startedRecording) {
                setRecording(true)
            }
        }
    }

    return (
        <div>
            {recording && (
                <article className={"prose"}>
                    <p>
                        Recording: {time}.mcap
                    </p>
                </article>
            )}
            <button className={getButtonStyle()} onClick={toggleRecording} disabled={false}>
                {getButtonText()}
            </button>
        </div>
    )

}
