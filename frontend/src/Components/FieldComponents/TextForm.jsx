import React from "react";

export function TextForm({fields, data, setData, index, recording}) {

    function handleChange(e) {
        // TODO: validate input
        const newData = [...data];
        newData[index] = e.target.value;
        setData(newData)
        //setData(data.map((v, i) => i === index ? e.target.value : v))
    }

    return (
        <input value={data[index]} onChange={handleChange} className={"input input-bordered w-80 -mt-3"} disabled={recording}/>
    )
}
