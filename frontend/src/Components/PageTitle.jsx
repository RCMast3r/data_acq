import React from 'react'

export function PageTitle({text}) {
    return (
        <article className={"prose"}>
            <h1>
                {text}
            </h1>
        </article>
    )
}
