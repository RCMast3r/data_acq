import {useState} from "react";

export function StartStopButton() {

    const [started, setStarted] = useState(false)

    function getButtonStyle() : string {
        return started ? "btn btn-error" : "btn btn-success"
    }

    function getButtonText() : string{
        return started? "Stop Recording" : "Start Recording"
    }

    function toggleRecording() {
        //TODO: POST request
        setStarted(!started)
    }

    return (
        <button className={getButtonStyle()} onClick={toggleRecording}>
            {getButtonText()}
        </button>
    )
}