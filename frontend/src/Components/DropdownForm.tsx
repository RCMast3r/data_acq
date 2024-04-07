import React, {useEffect, useState} from "react";

export function DropdownForm({title, type, data, setData, recording}:
                                 {
                                     title: string,
                                     type: string,
                                     data: string,
                                     setData: React.Dispatch<React.SetStateAction<string>>,
                                     recording: boolean
                                 }) {

    const [options, setOptions] = useState([] as string[])
    const [showAdd, setShowAdd] = useState(false)

    const webserverURL: string = 'http://192.168.203.1:6969'

    async function updateOptions() {
        const fetchResponse = await fetch(webserverURL + '/read/' + type, {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            }
        })
        setOptions(await fetchResponse.json())
    }

    useEffect(() => {
        updateOptions().then()
    }, [])

    function getAddForm() {
        if (!showAdd) return (<></>)
        return (
            <div className={"flex flex-row items-center w-96"}>
                <input className={"input input-bordered w-64"}/>
                <button className={"btn"}>
                    Add
                </button>
            </div>
        )
    }

    return (
        <>
            <div className={"flex flex-row items-center w-96"}>
                <article className={"prose"}>
                    <h4>{title + ':'}</h4>
                </article>
                <div className={"grow w-max"}/>
                <select value={data} className={"select select-bordered w-64"} onChange={e => setData(e.target.value)}
                        disabled={recording}>
                    {options.map((option) => <option value={option}>{option}</option>)}
                </select>
                <button className={"btn"} onClick={() => setShowAdd(!showAdd)}>
                    +
                </button>
            </div>
            {getAddForm()}
        </>
    )
}
