import React, {useEffect, useState} from "react";

export function DropdownForm({fields, data, setData, index}) {

    function handleChange(e) {
        const newData = [...data];
        newData[index] = e.target.value;
        setData(newData);
    }

    return (
        <select value={data[index]} className={"select select-bordered w-80"} onChange={handleChange}>
            {fields[index].options.map((option) => <option value={option}>{option}</option>)}
        </select>
    )

}

