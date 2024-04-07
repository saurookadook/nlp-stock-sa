import React from 'react';
// import logo from '/logo.svg';

function App({ data }: { data?: any | null }) {
    return (
        <div className="home">
            <header className="home-header">{`💸 🤑 💸 Welcome to NLP SSA 💸 🤑 💸`}</header>
            <div>
                <p>
                    <em>{`a.k.a.`}</em>
                </p>
                <p>
                    <b>{`💸 🤑 💸 THE MONEY MAKERRRRR 💸 🤑 💸 `}</b>
                </p>
            </div>
        </div>
    );
}

export default App;
