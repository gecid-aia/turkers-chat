import React from 'react';
import PropTypes from 'prop-types';
import { isEqual as _isEqual } from 'lodash';

import { GetChatMessagesEvent, SetReplyingMessageEvent } from '../../events';
import ReplyIcon from './static/ReplyIcon';
import MessageReply from './MessageReply';

let Messages = class extends React.Component {
  static propTypes = {
    chatId: PropTypes.number.isRequired,
    chats: PropTypes.object.isRequired,
    filterTurkersMessages: PropTypes.bool.isRequired,
  }

  constructor(props){
    super(props)
    this.state = { scheduler: null }
    this.messagesBox = React.createRef();
  }

  componentDidMount() {
    const { messagesUrl, chatId } = this.props;
    this.props.getChatMessages({ messagesUrl, chatId });
    this.setState({
      scheduler: setInterval(() => this.props.getChatMessages({ messagesUrl, chatId }), 1000 * 60)
    });
  }

  componentDidUpdate(prevProps) {
    const { chatId } = this.props;
    const isFirstMeaningfulRender = prevProps.chats[chatId] && !prevProps.chats[chatId].results.length && this.props.chats[chatId].results.length;
    const boxSize = this.messagesBox.current.clientHeight
    const scrollDifference = this.messagesBox.current.scrollHeight - (boxSize + this.messagesBox.current.scrollTop);

    if (isFirstMeaningfulRender || scrollDifference <= boxSize){
      this.messagesBox.current.scrollTop = this.messagesBox.current.scrollHeight;
    }
  }

  componentWillUnmount() {
    this.setState({ scheduler: null });
  }

  _getNextPage = () => {
    this.props.getChatMessages({
      messagesUrl: this.props.chats[this.props.chatId].nextPage,
      chatId: this.props.chatId,
    });
  }

  _setReplyingMessage = (chatId, replyTo) => {
    if (replyTo.accept_reply) {
      this.props.setReplyingMessage({ chatId, replyTo });
    }
  };

  render(){
    const { chats, chatId, filterTurkersMessages } = this.props;
    let results = chats[chatId] && chats[chatId].results && chats[chatId].results;

    if (results && filterTurkersMessages) {
      results = results.filter(message => message.sender_is_turker)
    }

    return (
      <div className="messages" ref={this.messagesBox}>
        {chats[chatId] && chats[chatId].nextPage ? (
          <div className="next-page-section" onClick={this._getNextPage}>
            <p>Ver mensagens antigas</p>
          </div>
        ) : null}
        {results && results.map((message, i) => (
          <div
            key={i}
            onClick={() => this._setReplyingMessage(chatId, message)}
            className={
              `message
              ${message.sender_is_turker ? ' turker-message' : ''}
              ${message.accept_reply ? ' can-be-replied' : ''}`
            }
          >
            {message.reply_to ? <MessageReply message={message.reply_to} /> : null}
            <p className="sender">
              <span>
                {message.sender_username}:
                <ReplyIcon />
              </span>
            </p>
            <p className="content">{message.content}</p>
          </div>
        ))}
      </div>
    );
  }
}

Messages = GetChatMessagesEvent.register({
  Component: Messages,
  props: ['chats']
});

Messages = SetReplyingMessageEvent.register({ Component: Messages });

export default Messages;
