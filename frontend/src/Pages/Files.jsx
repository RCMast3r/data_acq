import React, {useEffect, useState} from 'react';
import {FileInfo} from "../Components/FileInfo";
import {PageTitle} from "../Components/PageTitle";
import {AddrToggle} from "../Components/AddrToggle";

export function Files({}) {

    const [useLocalhost, setUseLocalhost] = useState(false)
    const [fileData, setFileData] = useState([])

    useEffect(() => {
        updateFiles().then(fileData => setFileData(fileData))
    }, [])

    async function updateFiles() {
        // TODO: HTTP Request
        let json = '[{"name": "2024-05-01-T00-00-00.mcap", "offloaded": false}, {"name": "2024-04-30-T00-00-00.mcap", "offloaded": true} ]'
        return JSON.parse(json)
    }

    return (
        <main>
            <div className={"flex flex-col gap-4 items-center justify-center pt-6"}>
                <AddrToggle useLocalhost={useLocalhost} setUseLocalhost={setUseLocalhost}/>
                
                <div className={"flex"}>
                    <PageTitle text={"MCAP Files on Car"}/>
                </div>

                {fileData.map((file, index) => <FileInfo key={file.name} fileData={fileData} index={index} useLocalhost={useLocalhost}/>)}
            </div>
        </main>
    )

}