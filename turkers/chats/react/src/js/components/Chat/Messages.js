import React from 'react';
import PropTypes from 'prop-types';
import { isEqual as _isEqual } from 'lodash';

import { GetChatMessagesEvent } from '../../events';

class Messages extends React.Component {
  static propTypes = {
    chatId: PropTypes.number.isRequired,
    chats: PropTypes.object.isRequired,
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
      scheduler: setInterval(() => this.props.getChatMessages({ messagesUrl, chatId }), 2000)
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

  getNextPage = () => {
    this.props.getChatMessages({
      messagesUrl: this.props.chats[this.props.chatId].nextPage,
      chatId: this.props.chatId,
    });
  }

  render(){
    const { chats, chatId } = this.props;
    return (
      <div className="messages" ref={this.messagesBox}>
        {chats[chatId] && chats[chatId].nextPage ? (
          <div className="next-page-section" onClick={this.getNextPage}>
            <p>Ver mensagens antigas</p>
          </div>
        ) : null}
        {chats[chatId] && chats[chatId].results && chats[chatId].results.map((message, i) => (
          <div className="message" key={i}>
            <p className="sender">{message.sender_username}: </p>
            <p className="content">{message.content}</p>
          </div>
        ))}
      </div>
    );
  }
}

export default GetChatMessagesEvent.register({
  Component: Messages,
  props: ['chats']
});
