import React from "react";

export function TextForm({title, isNum, data, setData, recording}:
                             {
                                 title: string,
                                 isNum: boolean,
                                 data: string,
                                 setData: React.Dispatch<React.SetStateAction<string>>,
                                 recording: boolean
                             }) {

    function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
        if (isNum) {
            let newStr: string = ""
            for (let i = 0; i < e.target.value.length; i++) {
                if (e.target.value[i] === '.' || (e.target.value[i] >= '0' && e.target.value[i] <= '9')) {
                    newStr += e.target.value[i]
                }
            }
            setData(newStr)
        } else {
            setData(e.target.value)
        }
    }

    return (
        <div className={"flex flex-row items-center w-96"}>
            <article className={"prose"}>
                <h4>{title + ':'}</h4>
            </article>
            <div className={"grow w-max"}/>
            <input value={data} onChange={handleChange} className={"input input-bordered w-64"}
                   disabled={recording}/>
        </div>
    )
}