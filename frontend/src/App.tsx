import React from 'react';
import './App.css';
import {StartStopButton} from "./Components/StartStopButton";
import {PageTitle} from "./Components/PageTitle";

function App() {
    return (
        <div className={"flex-col"}>
            <div className={"flex justify-center"}>
                <PageTitle></PageTitle>
            </div>
            <div className={"flex justify-center"}>
                <StartStopButton></StartStopButton>
            </div>
        </div>
    );
}

export default App;
