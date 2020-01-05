import React from 'react';
import PropTypes from 'prop-types';
import Draggable from 'react-draggable';

import Messages from './Messages';
import MessageInput from './MessageInput';
import ChatInfoOverlay from './ChatInfoOverlay';

export default class ChatBox extends React.Component {
  static propTypes = {
    chatId: PropTypes.number.isRequired,
    messagesUrl: PropTypes.string.isRequired,
    chatTitle: PropTypes.string.isRequired,
    chatIsCollective: PropTypes.bool.isRequired,
  }

  constructor(props){
    super(props);
    this.state = {
      showChat: props.chatIsCollective,
      showInfo: false,
    }
  }

  _toggleChatAndInfo = () => this.setState({ showChat: !this.state.showChat, showInfo: !this.state.showInfo })

  _toggleChat = () => {
    if (this.state.showInfo) {
      this._toggleChatAndInfo();
    }
    this.setState({ showChat: !this.state.showChat })
  };

  _toggleInfo = () => {
    if (!this.state.showChat) {
      this._toggleChatAndInfo();
    }
    this.setState({ showInfo: !this.state.showInfo })
  };

  render(){
    const { showChat, showInfo } = this.state;
    const { messagesUrl, chatId, chatInfo, chatTitle, chatIsCollective } = this.props;

    return (
      <Draggable
        handle=".header"
        bounds="parent"
        defaultPosition={{
          x: chatIsCollective ? 0 : window.innerWidth / 2 * Math.random(),
          y: chatIsCollective ? 0 : window.innerHeight / 2 * Math.random()
      }}
      >
        <div
          id={chatIsCollective ? "collective-chat" : ''}
          className={"chat-box" + (showChat ? '' : ' collapsed') + (showInfo ? ' inverted' : '')}
        >

          <div className="header">
            <strong>{chatTitle.toUpperCase()}</strong>


            <div className="chat-controls">
              {chatInfo && chatInfo.length ? <span onClick={this._toggleInfo}>?</span> : null}
              <span onClick={this._toggleChat}>{showChat ? '—' : '|'}</span>
            </div>
          </div>

          {showChat ? (
            <React.Fragment>

              <div className="separator"></div>
              {showInfo
                ? (
                  <React.Fragment>
                    <ChatInfoOverlay text={chatInfo} />
                    <a className="return-to-chat-link" href="#" onClick={this._toggleInfo}>Return to chat</a>
                  </React.Fragment>
                )
                : (
                  <React.Fragment>
                    <Messages messagesUrl={messagesUrl} chatId={chatId} />
                    <div className="separator"></div>
                    <MessageInput messagesUrl={messagesUrl} />
                  </React.Fragment>
                )}

            </React.Fragment>
          ) : null}
        </div>
      </Draggable>
    );
  };
}
