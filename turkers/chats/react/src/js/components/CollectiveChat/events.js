import { HTTPEvent } from "rel-events";

import {
  GetCollectiveChatMessagesEventManager,
  SendMessageEventManager,
} from "./eventManagers";

export const GetCollectiveChatMessagesEvent = new HTTPEvent({
  name: "getCollectiveChatMessages",
  manager: new GetCollectiveChatMessagesEventManager()
});

export const SendMessageEvent = new HTTPEvent({
  name: "sendMessage",
  manager: new SendMessageEventManager()
});
