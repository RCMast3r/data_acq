import React from 'react'

export function DeleteButton(serverAddr) {


    async function deleteMCAPs() {
        const fetchResponse = await fetch(serverAddr + '/delete', {
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
        <button className={"btn btn-error"} onClick={deleteMCAPs} disabled={false}>
            Delete
        </button>
    )
}
