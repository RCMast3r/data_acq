import React from "react";

export function TextForm({data, setData, index}) {

    function handleChange(e) {
        const newData = [...data];
        newData[index] = e.target.value;
        setData(newData)
    }

    return (
        <input value={data[index]} onChange={handleChange} className={"input input-bordered w-80"}/>
    )
}
