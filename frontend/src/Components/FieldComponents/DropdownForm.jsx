import React, {useEffect, useState} from "react";

export function DropdownForm({fields, data, setData, index, recording, serverAddr}) {

    const [options, setOptions] = useState([])
    const [showAdd, setShowAdd] = useState(false)
    const [addInput, setAddInput] = useState('')

    async function updateOptions() {
        console.log(fields[index].name)
         const fetchResponse = await fetch(serverAddr + '/read/' + fields[index].name, {
             method: 'POST',
             headers: {
                 'Accept': 'application/json',
                 'Content-Type': 'application/json'
             }
        })
         const resultArray = await fetchResponse.json()
         //console.log(resultArray)
        //const json = '["","True","False"]'
        setOptions(resultArray)
    }

    useEffect(() => {
        updateOptions().then()
    }, [])

    useEffect(() => {
        updateOptions().then()
    }, [serverAddr])

    async function addOption() {
        const fetchResponse = await fetch(serverAddr + '/add/' + fields[index].name, {
            method: 'POST',
            body: JSON.stringify(addInput),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
        fetchResponse.then(setShowAdd(false));
    }

    function handleChange(e) {
        const newData = [...data];
        newData[index] = e.target.value;
        setData(newData);
    }

    function getNoAdd() {
        return (
            <select value={data[index]} className={"select select-bordered w-80"} onChange={handleChange}
                    disabled={recording}>
                {options.map((option) => <option value={option}>{option}</option>)}
            </select>
        )
    }

    function getAddForm() {
        return (
            <div className={"flex flex-row items-center w-80 -mt-3"}>
                <input value={addInput} onChange={e => setAddInput(e.target.value)} className={"input input-bordered w-64"} disabled={recording}/>
                <div className={"grow w-max"}/>
                <button className={"btn"} onClick={() => addOption} disabled={addInput === ''}>
                    Ok
                </button>
            </div>
        )
    }

    function getAdd() {
        return (
            <div className={"flex flex-row items-center w-80"}>
                <select value={data[index]} className={"select select-bordered w-64"} onChange={handleChange} disabled={recording}>
                    {options.map((option) => <option value={option}>{option}</option>)}
                </select>
                <div className={"grow w-max"}/>
                <button className={"btn btn-square"} onClick={()=>setShowAdd(!showAdd)}>
                    {showAdd ? "-" : "+"}
                </button>
            </div>
        )
    }

    return (
        <>
            {fields[index].type === "boolean" ? getNoAdd() : getAdd()}
            {showAdd ? getAddForm() : null}
        </>
    )

}