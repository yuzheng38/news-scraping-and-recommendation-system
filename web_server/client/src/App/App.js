import '../../node_modules/materialize-css/dist/css/materialize.min.css';
import '../../node_modules/materialize-css/dist/js/materialize.js';
import './App.css';

import logo from './logo.png';
import NewsPanel from '../NewsPanel/NewsPanel.js';
import React from 'react';

class App extends React.Component {
    render() {
        return (
            <div className='App'>
                <img className='logo' src={logo} alt='logo' />
                <div className='container'>
                    <NewsPanel />
                </div> 
            </div> 
        );
    }
}

export default App;