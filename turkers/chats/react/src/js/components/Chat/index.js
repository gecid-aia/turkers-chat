import React from 'react';

import ChatBox from './ChatBox';
import { GetChatsEvent, SetReplyingMessageEvent } from '../../events';

let ChatsPage = class extends React.Component {
  componentDidMount() { this.props.getChats(); }

  render() {
    const { replyTo, chats } = this.props;

    return chats.map((chat) => (
      <ChatBox
        key={chat.id}
        chat={chat}
        replyTo={replyTo}
      />
    ));
  }
}

ChatsPage = GetChatsEvent.register({
  Component: ChatsPage,
  props: ['chats']
});

ChatsPage = SetReplyingMessageEvent.register({
  Component: ChatsPage,
  props: ['replyTo']
});

export default ChatsPage;
