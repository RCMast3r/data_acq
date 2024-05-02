
import React from 'react'

export function OffloadButton() {

    const webserverURL = 'http://192.168.203.1:6969'

    async function offload() {
        const fetchResponse = await fetch(webserverURL + '/offload', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            }
        })
        const status = fetchResponse.status
        return status === 200
    }

    return (

        <button className={"btn"} onClick={() => alert("New Alert")} disabled={false}>
            Offload
        </button>
    )
}
