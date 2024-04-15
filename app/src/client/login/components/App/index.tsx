import React from 'react';
// import logo from '/logo.svg';

function App({ data }: { data?: Record<string, unknown> | null }) {
    console.log('login - App', { data });
    return (
        <div className="App">
            <header className="App-header">{`💸 🤑 💸 Login 💸 🤑 💸`}</header>
            <div>{`BIG OL' FORM`}</div>
        </div>
    );
}

export default App;
