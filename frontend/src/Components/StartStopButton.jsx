import React from "react";
import { useState } from "react";
import {getURL} from "../Util/ServerAddrUtil";
import {getFormattedDate} from "../Util/DateUtil";
import {getMetadata} from "../Util/DataUtil";
import {wait} from "@testing-library/user-event/dist/utils";

export function StartStopButton({fields, data, recording, setRecording, useLocalhost}) {

    const [time, setTime] = useState("");
    const [waitingForResponse, setWaitingForResponse] = useState(false);

    function getButtonStyle() {
        return recording ? "btn btn-error" : "btn btn-success"
    }

    function getButtonText() {
        return recording ? "Stop Recording" : "Start Recording"
    }

    async function stopRecording() {
        if(waitingForResponse) {
            return false
        }
        setWaitingForResponse(true);
        const fetchResponse = await fetch(getURL('stop', useLocalhost), {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            }
        })
        setWaitingForResponse(false);
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
        setWaitingForResponse(true);

        // Creating the formatted date string
        const formattedDate = getFormattedDate()
        setTime(formattedDate)

        let body = getMetadata(fields, data)

        const fetchResponse = await fetch(getURL('start', useLocalhost), {
            method: 'POST',
            body: body,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            }
        })

        setWaitingForResponse(false);
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
        <div className="centered-container">
            {recording && (
                <article className={"prose"}>
                    <p>
                        Recording: {time}.mcap
                    </p>
                </article>
            )}
            <button className={getButtonStyle()} onClick={toggleRecording} disabled={waitingForResponse}>
                {getButtonText()}
            </button>
        </div>
    )

}
