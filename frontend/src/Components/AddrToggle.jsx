import React from 'react';

export function AddrToggle({serverAddr, setServerAddr}) {

    function handleChange(e) {
        if(e.target.checked) {
            setServerAddr("http://localhost:6969")
        } else {
            setServerAddr("http://192.168.203.1:6969")
        }
    }

    return (
        <div className={"flex flex-row items-center w-80"}>
            <div className={"grow w-max"}/>
            <article className={"prose pr-2"}>
                <p> DO NOT TOUCH -&gt;</p>
            </article>
            <input type={"checkbox"} className={"toggle toggle-primary"} onChange={handleChange}/>
        </div>
    )

}