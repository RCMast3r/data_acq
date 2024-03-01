import React, {useState} from "react";

export function StartStopButton({recording, setRecording}: {recording: boolean, setRecording: React.Dispatch<React.SetStateAction<boolean>>}) {

    function getButtonStyle() : string {
        return recording ? "btn btn-error" : "btn btn-success"
    }

    function getButtonText() : string{
        return recording ? "Stop Recording" : "Start Recording"
    }

    function toggleRecording() {
        //TODO: POST request
        setRecording(!recording)
    }

    return (
        <button className={getButtonStyle()} onClick={toggleRecording}>
            {getButtonText()}
        </button>
    )
}