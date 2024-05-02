import React from 'react';

export function FileInfo({fileData, index, useLocalhost}) {

    function edit() {
        alert("This feature has not been implemented yet")
    }
    
    function offloadFile() {
        alert("This feature has not been implemented yet")
    }
    
    function getOffloadStatus() {
        if(fileData[index].offloaded) {
            return (
                <article className={"article pt-3"}>
                    <p className={"text-success"}>
                        Offloaded
                    </p>
                </article>
            )
        } else {
            return (
                <button className={"btn btn-success"}>
                    Offload
                </button>
            )
        }
    }
    
    return (
        <div className={"bg-base-300 p-6 rounded-lg"}>
            <article className={"article"}>
                <p>{fileData[index].name}</p>
            </article>
            <div className={"flex flex-row gap-10 w-80 bg-base-300 pt-4"}>
                <div className={"grow w-max"}/>
                {getOffloadStatus()}
                <button className={"btn"} onClick={edit}>
                    Edit Metadata
                </button>
            </div>
        </div>
    )

}