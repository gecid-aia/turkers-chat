import React from 'react';
import PropTypes from 'prop-types';
import Draggable from 'react-draggable';

import Messages from './Messages';
import MessageInput from './MessageInput';

export default class ChatBox extends React.Component {
  static propTypes = {
    chatId: PropTypes.number.isRequired,
    messagesUrl: PropTypes.string.isRequired,
    chatTitle: PropTypes.string.isRequired,
    chatIsCollective: PropTypes.bool.isRequired,
  }

  state = { showChat: true }

  _toggleChat = () => this.setState({ showChat: !this.state.showChat });

  render(){
    const { showChat } = this.state;
    const { messagesUrl, chatId, chatTitle, chatIsCollective } = this.props;

    return (
      <Draggable
        handle=".header"
        bounds="parent"
        defaultPosition={{
          x: chatIsCollective ? 0 : window.innerWidth / 2 * Math.random(),
          y: chatIsCollective ? 0 : window.innerHeight / 2 * Math.random()
      }}
      >
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
              <Messages messagesUrl={messagesUrl} chatId={chatId} />
              <div className="separator"></div>

              <MessageInput messagesUrl={messagesUrl} />
            </React.Fragment>
          ) : null}
        </div>
      </Draggable>
    );
  };
}
