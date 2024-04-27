import React from "react";

export function StartStopButton({fields, data, recording, setRecording}) {

    var waitingForResponse = false

    function getButtonStyle() {
        return recording ? "btn btn-error" : "btn btn-success"
    }

    function getButtonText() {
        return recording ? "Stop Recording" : "Start Recording"
    }

    function isDisabled() {
        if (waitingForResponse) {
            return true
        }
        let ret = false
        for (let i = 0; i < data.length; i++) {
            if(data[i] === undefined || data[i] === null) {
                ret = true
                break
            }
        }
        return ret
    }

    const webserverURL = 'http://192.168.203.1:6969'
    //const webserverURL = 'http://0.0.0.0:6969'

    async function stopRecording() {
        if(waitingForResponse) {
            return false
        }
        waitingForResponse = true
        const fetchResponse = await fetch(webserverURL + '/stop', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            }
        })
        waitingForResponse = false
        const status = fetchResponse.status
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
        body += '"time":"' + (new Date()).toString()+'"'
        body += " }"
        console.log(body)
        const fetchResponse = await fetch(webserverURL + '/start', {
            method: 'POST',
            body: body,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            }
        })

        waitingForResponse = false
        const status = fetchResponse.status
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
        <button className={getButtonStyle()} onClick={toggleRecording} disabled={isDisabled()}>
            {getButtonText()}
        </button>
    )

}
