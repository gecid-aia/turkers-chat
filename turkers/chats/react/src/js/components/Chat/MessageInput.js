import React from 'react';
import PropTypes from 'prop-types';

import { SendMessageEvent } from '../../events';

class MessageInput extends React.Component {
  static propTypes = {
    messagesUrl: PropTypes.string.isRequired,
  }

  state = { message: '' }

  _handleMessageTyping = e => {
    this.setState({ message: e.target.value });
  }

  _handleKeyDown = e => {
    if (e.key === 'Enter') {
      const { message }= this.state;
      const { messagesUrl }= this.props;
      this.setState({ message: '' }, () => {
        this.props.sendMessage({ messagesUrl, message });
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
