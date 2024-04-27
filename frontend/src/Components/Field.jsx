import React from 'react';
import {TextForm} from "./FieldComponents/TextForm";
import {FieldTitle} from "./FieldComponents/FieldTitle";
import {DropdownForm} from "./FieldComponents/DropdownForm";

export function Field({fields, data, setData, index, recording, serverAddr}) {
    
    function getField() {
        //console.log(JSON.stringify(fields[index]))
        if (fields[index] === undefined) {
            return (<></>)
        } else if (fields[index].automatic) {
            return (<></>)
        } else if(fields[index].dropdown) {
            return (<DropdownForm fields={fields} data={data} setData={setData} index={index} recording={recording} serverAddr={serverAddr}/>)
        } else {
            return (<TextForm fields={fields} data={data} setData={setData} index={index} recording={recording}/>)
        }
    }

    return (
        <>
            <FieldTitle fields={fields} index={index}/>
            {getField()}
        </>
    )
}