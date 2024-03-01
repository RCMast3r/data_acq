import React from "react";

export function DropdownForm({title, options, data, setData, recording}:
                                 {
                                     title: string,
                                     options: string[],
                                     data: string,
                                     setData: React.Dispatch<React.SetStateAction<string>>,
                                     recording: boolean
                                 }) {

    return (
        <div className={"flex flex-row items-center w-96"}>
            <article className={"prose"}>
                <h4>{title + ':'}</h4>
            </article>
            <div className={"grow w-max"}/>
            `
            <select value={data} className={"select select-bordered w-64"} onChange={e => setData(e.target.value)} disabled={recording}>
                {options.map((option) => <option value={option}>{option}</option>)}
            </select>
        </div>

    )
}