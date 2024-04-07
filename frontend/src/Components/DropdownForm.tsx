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
    const [newOption, setNewOption] = useState("")

    // const webserverURL: string = 'http://192.168.203.1:6969'
    const webserverURL: string = 'http://192.168.172.129:6969'

    async function updateOptions() {
        const fetchResponse = await fetch(webserverURL + '/read/' + type, {
            method: 'GET',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            }
        })
        console.log(await fetchResponse.json())
        setOptions(await fetchResponse.json())
    }

    async function addOption() {
        const fetchResponse = await fetch(webserverURL + '/write/' + type, {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                value: newOption
            })
        })
        await fetchResponse.json()
        await updateOptions()
        setShowAdd(false)
        setNewOption("")
    }

    useEffect(() => {
        updateOptions().then()
    }, [])

    function getAddForm() {
        if (!showAdd) return (<></>)
        return (
            <div className={"flex flex-row items-center w-96"}>
                <input value={newOption} className={"input input-bordered w-64"}/>
                <button className={"btn"} onClick={() => addOption()}>
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
