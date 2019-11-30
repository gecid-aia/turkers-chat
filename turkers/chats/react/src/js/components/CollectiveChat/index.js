import React from 'react';
import Draggable from 'react-draggable';

import Messages from '../Chat/Messages';
import MessageInput from '../Chat/MessageInput';

export default class CollectiveChat extends React.Component {
  state = { showChat: true }

  _toggleChat = () => this.setState({ showChat: !this.state.showChat });

  render(){
    const { showChat } = this.state;

    return (
      <Draggable handle=".header" bounds="parent">
        <div id="collective-chat" className={"chat-box" + (showChat ? '' : ' collapsed')}>

          <div className="header">
            <strong>CONVERSA COLETIVA</strong>
            <div className="hide-chat" onClick={this._toggleChat}>
              {showChat ? '—' : '|'}
            </div>
          </div>

          {showChat ? (
            <React.Fragment>

              <div className="separator"></div>
              <Messages />
              <div className="separator"></div>

              <MessageInput />
            </React.Fragment>
          ) : null}
        </div>
      </Draggable>
    );
  };
}
