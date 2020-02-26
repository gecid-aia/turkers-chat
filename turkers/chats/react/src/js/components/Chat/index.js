import React from 'react';

import ChatBox from './ChatBox';
import { GetChatsEvent } from '../../events';

class ChatsPage extends React.Component {
  componentDidMount() { this.props.getChats(); }

  render() {
    return this.props.chats.map((chat) => (
      <ChatBox
        key={chat.id}
        chat={chat}
      />
    ));
  }
}

export default GetChatsEvent.register({
  Component: ChatsPage,
  props: ['chats']
});
