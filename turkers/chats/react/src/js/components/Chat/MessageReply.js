import React from 'react';
import { truncate as _truncate } from 'lodash';

import ReplyIcon from './static/ReplyIcon';

export default function MessageReply({ message }) {
  return (
    <div className="message-reply">
      <span><ReplyIcon /></span>
      <p className="title">Reply to</p>
      <p className="sender">{message.sender_username}</p>
      <p>{_truncate(message.content)}</p>
    </div>
  );
}
