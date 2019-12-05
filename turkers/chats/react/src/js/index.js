import React from "react";
import ReactDOM from "react-dom";
import thunk from "redux-thunk";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import { eventsMiddleware } from "rel-events";

import rootReducer from "./rootReducer";
import CollectiveChat from "./components/CollectiveChat";

import "whatwg-fetch";
import "../scss/index.scss";

const store = createStore(
  rootReducer,
  applyMiddleware(thunk, eventsMiddleware)
);

class App extends React.Component {
  render() {
    return <Provider store={store}><CollectiveChat /></Provider>;
  }
}

ReactDOM.render(<App />, document.getElementById("chat-react"));
