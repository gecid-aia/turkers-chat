import React from 'react';
import PropTypes from 'prop-types';
import Draggable from 'react-draggable';

import Messages from './Messages';
import MessageInput from './MessageInput';
import ChatInfoOverlay from './ChatInfoOverlay';

export default class ChatBox extends React.Component {
  static propTypes = {
    chat: PropTypes.shape({
      id: PropTypes.number.isRequired,
      messages_url: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      is_collective: PropTypes.bool.isRequired,
      open_for_messages: PropTypes.bool.isRequired,
    })
  }

  constructor(props){
    super(props);
    this.state = {
      showChat: props.chat.is_collective,
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
    const { messages_url, id, info, title, is_collective, open_for_messages } = this.props.chat;

    return (
      <Draggable
        handle=".header"
        bounds="parent"
        defaultPosition={{
          x: is_collective ? 0 : window.innerWidth / 2 * Math.random(),
          y: is_collective ? 0 : window.innerHeight / 2 * Math.random()
      }}
      >
        <div
          id={is_collective ? "collective-chat" : ''}
          className={
            `chat-box
            ${showChat ? '' : ' collapsed'}
            ${showInfo ? ' inverted' : ''}
            ${open_for_messages ? '' : ' closed-for-messages'}
          `}
        >

          <div className="header">
            <strong>{title.toUpperCase()}</strong>


            <div className="chat-controls">
              {info && info.length ? <span onClick={this._toggleInfo}>?</span> : null}
              <span onClick={this._toggleChat}>{showChat ? '—' : '|'}</span>
            </div>
          </div>

          {showChat ? (
            <React.Fragment>

              <div className="separator"></div>
              {showInfo
                ? (
                  <React.Fragment>
                    <ChatInfoOverlay text={info} />
                    <a className="return-to-chat-link" href="#" onClick={this._toggleInfo}>Return to chat</a>
                  </React.Fragment>
                )
                : (
                  <React.Fragment>
                    <Messages messagesUrl={messages_url} chatId={id} />
                    {open_for_messages ? (
                      <React.Fragment>
                        <div className="separator"></div>
                        <MessageInput messagesUrl={messages_url} />
                      </React.Fragment>
                    ) : null}
                  </React.Fragment>
                )}

            </React.Fragment>
          ) : null}
        </div>
      </Draggable>
    );
  };
}
