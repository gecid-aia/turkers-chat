import React from 'react';

import ChatBox from './ChatBox';
import { GetChatsEvent } from '../../events';

class ChatsPage extends React.Component {
  componentDidMount(){ this.props.getChats(); }

  render(){
    return this.props.chats.map((chat) => (
      <ChatBox
        messagesUrl={chat.messages_url}
        chatTitle={chat.title}
        chatId={chat.id}
        chatIsCollective={chat.is_collective}
      />
    ));
  }
}

export default GetChatsEvent.register({
  Component: ChatsPage,
  props: ['chats']
});
