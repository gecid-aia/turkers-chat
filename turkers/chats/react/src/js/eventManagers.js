import { fetchFromApi } from "rel-events";
import {
  cloneDeep as _cloneDeep,
  isEqual as _isEqual,
  unionBy as _unionBy,
  sortBy as _orderBy,
} from 'lodash';
import { getCurrentStateFromEvent } from "rel-events/dist/helpers";

export class GetChatMessagesEventManager {
  initialState = { chats: {} };

  call = ({ messagesUrl }) => () => fetchFromApi(messagesUrl);

  onDispatch = state => state;
  onFailure = state => state;
  onSuccess = (state, event) => {
    const newState = _cloneDeep(state);

    if (!state.chats[event.extraData.chatId]) {
      state.chats[event.extraData.chatId] = { results: [] }
    }

    const newResults = _unionBy(
      event.response.data.results,
      state.chats[event.extraData.chatId].results,
      'id'
    );

    newState.chats[event.extraData.chatId] = {
      nextPage: event.response.data.next,
      results: _orderBy(newResults, ['id'], ['asc'])
    }

    if (_isEqual(
      state.chats[event.extraData.chatId].results,
      newState.chats[event.extraData.chatId].results
    )) {
      return state;
    }

    return newState;
  };
}

export class GetChatsEventManager {
  initialState = { chats: [] };

  call = () => () => fetchFromApi('/api/chats/');

  onDispatch = state => state;
  onFailure = state => state;
  onSuccess = (state, event) => ({...state, chats: event.response.data.results});
}

export class SendMessageEventManager {
  initialState = { isLoading: false };

  shouldDispatch = (appState, event) => {
    const currentState = getCurrentStateFromEvent({ event: SendMessageEvent, appState });
    return !currentState.isLoading;
  }

    const requestData = {
      method: 'POST',
      body: JSON.stringify({
        content: message,
      })
    };

    return () => fetchFromApi(messagesUrl, requestData);
  };

  onDispatch = state => state;
  onFailure = state => state;
  onSuccess = state => state;
}
