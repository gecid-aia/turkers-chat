import React from 'react';

import { SendMessageEvent } from '../CollectiveChat/events';

class MessageInput extends React.Component {
  state = { message: '' }

  _handleMessageTyping = e => {
    this.setState({ message: e.target.value });
  }

  _handleKeyDown = e => {
    if (e.key === 'Enter') {
      const { message }= this.state;
      this.setState({ message: '' }, () => {
        this.props.sendMessage({ chatId: 1, message });
      })
    }
  }

  render(){
    return (
      <input
        type="text"
        value={this.state.message}
        onChange={this._handleMessageTyping}
        onKeyDown={this._handleKeyDown}
      />
    );
  }
}

export default SendMessageEvent.register({
  Component: MessageInput,
});
