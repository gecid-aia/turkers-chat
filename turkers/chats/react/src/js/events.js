import { HTTPEvent } from "rel-events";

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
