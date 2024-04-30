import React from 'react';
import {TextForm} from "./FieldComponents/TextForm";
import {FieldTitle} from "./FieldComponents/FieldTitle";
import {DropdownForm} from "./FieldComponents/DropdownForm";
import {BooleanForm} from "./FieldComponents/BooleanForm";
import {PidForm} from "./FieldComponents/PidForm";

export function Field({fields, data, setData, index}) {
    
    function getField() {
        if (fields[index] === undefined) {
            return (<></>)
        } else if (fields[index].automatic) {
            return (<></>)
        } else if (fields[index].type === "boolean") {
            return (<BooleanForm data={data} setData={setData} index={index}/>)
        } else if (fields[index].type === "pid") {
            return (<PidForm data={data} setData={setData} index={index}/> )
        } else if(fields[index].options.length > 0) {
            return (<DropdownForm fields={fields} data={data} setData={setData} index={index}/>)
        } else {
            return (<TextForm data={data} setData={setData} index={index}/>)
        }
    }

    return (
        <>
            <FieldTitle fields={fields} index={index}/>
            {getField()}
        </>
    )
}