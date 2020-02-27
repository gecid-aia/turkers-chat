import React from 'react';
import PropTypes from 'prop-types';

import { SendMessageEvent, SetReplyingMessageEvent } from '../../events';
import MessageReply from './MessageReply';

let MessageInput = class extends React.Component {
  static propTypes = {
    messagesUrl: PropTypes.string.isRequired,
  }

  state = { message: '' }

  _handleMessageTyping = e => {
    this.setState({ message: e.target.value });
  }

  _handleKeyPress = e => {
    if (e.key === 'Enter') {
      const { message }= this.state;
      const { messagesUrl, replyTo } = this.props;
      this.setState({ message: '' }, () => {
        if (replyTo) {
          this.props.setReplyingMessage();
          this.props.sendMessage({ messagesUrl, message, replyTo })
        };
        this.props.sendMessage({ messagesUrl, message });
      })
    }
  }

  render(){
    const { replyTo } = this.props;

    return (
      <React.Fragment>
        {replyTo ?(
          <MessageReply message={replyTo} />
        ) : null}
        <input
          type="text"
          value={this.state.message}
          onChange={this._handleMessageTyping}
          onKeyPress={this._handleKeyPress}
        />
      </React.Fragment>
    );
  }
}

MessageInput = SendMessageEvent.register({
  Component: MessageInput,
});

MessageInput = SetReplyingMessageEvent.register({
  Component: MessageInput,
  props: ['replyTo']
})

export default MessageInput;
