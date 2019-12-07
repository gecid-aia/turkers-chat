import React from "react";
import ReactDOM from "react-dom";
import thunk from "redux-thunk";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import { eventsMiddleware } from "rel-events";

import rootReducer from "./rootReducer";
import ChatsPage from "./components/Chat/";

import "whatwg-fetch";
import "../scss/index.scss";

const store = createStore(
  rootReducer,
  applyMiddleware(thunk, eventsMiddleware)
);

class App extends React.Component {
  render() {
    return <Provider store={store}><ChatsPage /></Provider>;
  }
}

ReactDOM.render(<App />, document.getElementById("chat-react"));
