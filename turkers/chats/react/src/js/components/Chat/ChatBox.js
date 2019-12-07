import React from 'react';
import PropTypes from 'prop-types';
import Draggable from 'react-draggable';

import Messages from './Messages';
import MessageInput from './MessageInput';

export default class ChatBox extends React.Component {
  static propTypes = {
    messagesUrl: PropTypes.string.isRequired,
    chatTitle: PropTypes.string.isRequired,
    chatIsCollective: PropTypes.bool.isRequired,
  }

  state = { showChat: true }

  _toggleChat = () => this.setState({ showChat: !this.state.showChat });

  render(){
    const { showChat } = this.state;
    const { messagesUrl, chatTitle, chatIsCollective } = this.props;

    return (
      <Draggable handle=".header" bounds="parent">
        <div id={chatIsCollective ? "collective-chat" : ''} className={"chat-box" + (showChat ? '' : ' collapsed')}>

          <div className="header">
            <strong>{chatTitle.toUpperCase()}</strong>
            <div className="hide-chat" onClick={this._toggleChat}>
              {showChat ? '—' : '|'}
            </div>
          </div>

          {showChat ? (
            <React.Fragment>

              <div className="separator"></div>
              <Messages messagesUrl={messagesUrl} />
              <div className="separator"></div>

              <MessageInput messagesUrl={messagesUrl} />
            </React.Fragment>
          ) : null}
        </div>
      </Draggable>
    );
  };
}
