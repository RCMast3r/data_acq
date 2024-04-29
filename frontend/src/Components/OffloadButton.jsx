import React from "react";

export function OffloadButton({serverAddr}) {

    async function offload() {
        const fetchResponse = await fetch(serverAddr + '/offload', {
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
        <button className={"btn"} onClick={offload} disabled={false}>
            Offload
        </button>
    )
}
