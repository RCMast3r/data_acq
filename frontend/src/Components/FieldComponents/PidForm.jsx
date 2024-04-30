import React from 'react';

export function PidForm({data, setData, index}) {

    function handleChangeP(e) {
        const newData = [...data]
        newData[index].p = e.target.value
        setData(newData)
    }
    
    function handleChangeI(e) {
        const newData = [...data]
        newData[index].p = e.target.value
        setData(newData)
    }
    
    function handleChangeD(e) {
        const newData = [...data]
        newData[index].p = e.target.value
        setData(newData)
    }
    
    return (
        <div className={"flex flex-row items-center w-80 -mb-3"}>
            <article className={"prose pr-2"}>
                <p>P:</p>
            </article>
            <input value={data[index].p} onChange={handleChangeP} className={"input input-bordered w-20"}/>
            
            <div className={"grow w-max"}/>
            
            <article className={"prose pr-2"}>
                <p>I:</p>
            </article>
            <input value={data[index].p} onChange={handleChangeI} className={"input input-bordered w-20"}/>
            
            <div className={"grow w-max"}/>
            
            <article className={"prose pr-2"}>
                <p>D:</p>
            </article>
            <input value={data[index].p} onChange={handleChangeD} className={"input input-bordered w-20"}/>
        </div>
    )

}