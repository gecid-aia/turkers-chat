import React from 'react';
import { isEqual as _isEqual } from 'lodash';

import { GetCollectiveChatMessagesEvent } from '../CollectiveChat/events';

class Messages extends React.Component {
  constructor(props){
    super(props)
    this.state = { scheduler: null }
    this.messagesBox = React.createRef();
  }

  componentDidMount() {
    this.props.getCollectiveChatMessages();
    this.setState({
      scheduler: setInterval(() => this.props.getCollectiveChatMessages(), 1000)
    });
  }

  componentDidUpdate({ results }) {
    if (!_isEqual(results, this.props.results)){
      this.messagesBox.current.scrollTop = this.messagesBox.current.scrollHeight;
    }
  }

  componentWillUnmount() {
    this.setState({ scheduler: null });
  }

  render(){
    const { results } = this.props;
    return (
      <div className="messages" ref={this.messagesBox}>
        {results.map((message, i) => (
          <div className="message" key={i}>
            <p className="sender">{message.sender_username}: </p>
            <p className="content">{message.content}</p>
          </div>
        ))}
      </div>
    );
  }
}

export default GetCollectiveChatMessagesEvent.register({
  Component: Messages,
  props: ['results']
});
