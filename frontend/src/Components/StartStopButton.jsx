import React from "react";
import { useState } from "react";

export function StartStopButton({fields, data, recording, setRecording, serverAddr}) {
    const [showAlert, setShowAlert] = useState(false);
    const [alertMessage, setAlertMessage] = useState("");
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


    async function stopRecording() {
        if(waitingForResponse) {
            return false
        }
        waitingForResponse = true
        const fetchResponse = await fetch(serverAddr + '/stop', {
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
        const date = new Date();
  
        // Extracting date components
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, '0'); // Adding 1 because months are zero-based
        const day = date.getDate().toString().padStart(2, '0');
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        const seconds = date.getSeconds().toString().padStart(2, '0');

        // Creating the formatted date string
        const formattedDate = `${year}-${month}-${day}-T${hours}-${minutes}-${seconds}`;
        body += '"time":"' + formattedDate+'"'
        body += " }"
        console.log(body)
        const fetchResponse = await fetch(serverAddr + '/start', {
            method: 'POST',
            body: body,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            }
        })

        waitingForResponse = false
        const status = fetchResponse.status
        if (status == 200) {
            setAlertMessage("Writing to " + formattedDate + ".mcap"); // Set the alert message
            setShowAlert(true); // Show alert if request was successful
            setTimeout(() => {
                setShowAlert(false);
              }, 5000);
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
            {showAlert && (
                <div class="toast">
                <div class="alert alert-info">
                  <span>{alertMessage}</span>
                </div>
              </div>
            )}
            <button className={getButtonStyle()} onClick={toggleRecording} disabled={false}>
                {getButtonText()}
            </button>
        </div>
    )

}
