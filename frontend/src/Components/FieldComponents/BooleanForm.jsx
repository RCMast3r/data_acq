import React from 'react';

export function BooleanForm({data, setData, index}) {
    function handleChange(e) {
        const newData = [...data]
        newData[index] = e.target.value === "True"
        setData(newData)
    }

    return (
        <select value={data[index] ? "True" : "False"} className={"select select-bordered w-80"}
                onChange={handleChange}>
            <option value={"False"}>False</option>
            <option value={"True"}>True</option>
        </select>
    )
}