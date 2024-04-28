import React from 'react';

export function EditModeToggle({editMode, setEditMode}) {

    return (
        <div className={"flex flex-row items-center w-80"}>
            <div className={"grow w-max"}/>
            <article className={"prose pr-2"}>
                <p> Edit Mode </p>
            </article>
            <input type={"checkbox"} value={editMode} className={"toggle toggle-primary"} onChange={e => setEditMode(e.target.checked)}/>
        </div>
    )

}