import React from "react";

export function StartStopButton({ recording, setRecording, driverInput, trackNameInput, eventTypeInput,
    drivetrainTypeInput, massInput, wheelbaseInput, firmwareRevInput }: {
        recording: boolean,
        setRecording: React.Dispatch<React.SetStateAction<boolean>>,
        driverInput: string,
        trackNameInput: string,
        eventTypeInput: string,
        drivetrainTypeInput: string,
        massInput: string,
        wheelbaseInput: string,
        firmwareRevInput: string
    }) {

    var waitingForResponse: Boolean = false

    function getButtonStyle(): string {
        return recording ? "btn btn-error" : "btn btn-success"
    }

    function getButtonText(): string {
        return recording ? "Stop Recording" : "Start Recording"
    }

    function isDisabled(): boolean {
        if (waitingForResponse) return true
        if (driverInput.length === 0) return true
        if (trackNameInput.length === 0) return true
        if (eventTypeInput.length === 0) return true
        if (drivetrainTypeInput.length === 0) return true
        if (massInput.length === 0) return true
        if (wheelbaseInput.length === 0) return true
        if (firmwareRevInput.length === 0) return true
        return false
    }

    const webserverURL: string = 'http://192.168.203.1:6969'

    async function stopRecording(): Promise<boolean> {
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

    async function startRecording(): Promise<boolean> {
        console.log("Start Recording function started")
        console.log(webserverURL + '/start')
        waitingForResponse = true
        try {
            const fetchResponse = await fetch(webserverURL + '/start', {
            method: 'POST',
            body: JSON.stringify({
                driver: driverInput,
                trackName: trackNameInput,
                eventType: eventTypeInput,
                drivetrainType: drivetrainTypeInput,
                mass: massInput,
                wheelbase: wheelbaseInput,
                firmwareRev: firmwareRevInput
            }),
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            }
            })

            waitingForResponse = false
            const status = fetchResponse.status
            return status === 200
        } catch (error) {
            console.log(error)
        }

        return false

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
