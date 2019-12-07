import React from 'react';
import PropTypes from 'prop-types';
import { isEqual as _isEqual } from 'lodash';

import { GetChatMessagesEvent } from '../../events';

class Messages extends React.Component {
  static propTypes = {
    messagesUrl: PropTypes.string.isRequired,
    results: PropTypes.object.isRequired,
  }

  constructor(props){
    super(props)
    this.state = { scheduler: null }
    this.messagesBox = React.createRef();
  }

  componentDidMount() {
    const { messagesUrl } = this.props;
    this.props.getChatMessages({ messagesUrl });
    this.setState({
      scheduler: setInterval(() => this.props.getChatMessages({ messagesUrl }), 2000)
    });
  }

  componentDidUpdate({ results }) {
    if (!_isEqual(results[this.props.messagesUrl], this.props.results[this.props.messagesUrl])){
      this.messagesBox.current.scrollTop = this.messagesBox.current.scrollHeight;
    }
  }

  componentWillUnmount() {
    this.setState({ scheduler: null });
  }

  render(){
    const { results, messagesUrl } = this.props;
    return (
      <div className="messages" ref={this.messagesBox}>
        {results[messagesUrl] && results[messagesUrl].map((message, i) => (
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
  props: ['results']
});
