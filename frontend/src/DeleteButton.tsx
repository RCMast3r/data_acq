import React from 'react'
import { exec } from "node:child_process";

export function DeleteButton() {

    const webserverURL: string = 'http://192.168.203.1:6969'

    async function deleteMCAPs() {
        const fetchResponse = await fetch(webserverURL + '/delete', {
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
        <button className={"btn"} onClick={deleteMCAPs} disabled={false}>
            Delete
        </button>
    )
}
