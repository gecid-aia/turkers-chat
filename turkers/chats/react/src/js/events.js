import { HTTPEvent, Event } from "rel-events";

import {
  GetChatMessagesEventManager,
  SendMessageEventManager,
  GetChatsEventManager,
} from "./eventManagers";

export const GetChatMessagesEvent = new HTTPEvent({
  name: "getChatMessages",
  manager: new GetChatMessagesEventManager()
});

export const GetChatsEvent = new HTTPEvent({
  name: "getChats",
  manager: new GetChatsEventManager()
});

export const SendMessageEvent = new HTTPEvent({
  name: "sendMessage",
  manager: new SendMessageEventManager()
});

export const SetReplyingMessageEvent = new Event({
  name: "setReplyingMessage",
  manager: {
    initialState: { replyTo: {} },
    onDispatch: (state, event) => {
      if (!event.replyTo) {
        return { replyTo: {} };
      }

      return {
        replyTo: {
          ...state.replyTo,
          [event.chatId]: event.replyTo
        }
      };
    }
  }
});
