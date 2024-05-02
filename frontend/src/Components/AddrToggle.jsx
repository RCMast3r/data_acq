import React from 'react';

export function AddrToggle({useLocalhost, setUseLocalhost}) {

    return (
        <div className={"flex flex-row items-center w-80"}>
            <div className={"grow w-max"}/>
            <article className={"prose pr-2"}>
                <p> DO NOT TOUCH -&gt;</p>
            </article>
            <input value={useLocalhost} type={"checkbox"} className={"toggle toggle-error"} onChange={e => setUseLocalhost(e.target.checked)}/>
        </div>
    )

}