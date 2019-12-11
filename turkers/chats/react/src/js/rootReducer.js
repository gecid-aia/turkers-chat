import { combineReducers } from "redux";
import { combineEventReducers } from "rel-events";

import {
  GetChatMessagesEvent,
  SendMessageEvent,
  GetChatsEvent
} from "./events";

export default combineReducers({
  ...combineEventReducers([
    GetChatMessagesEvent,
    SendMessageEvent,
    GetChatsEvent
  ])
});
