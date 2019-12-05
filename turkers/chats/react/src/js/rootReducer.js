import { combineReducers } from "redux";
import { combineEventReducers } from "rel-events";

import {
  GetCollectiveChatMessagesEvent,
  SendMessageEvent
} from "./components/CollectiveChat/events";

export default combineReducers({
  ...combineEventReducers([GetCollectiveChatMessagesEvent, SendMessageEvent])
});
