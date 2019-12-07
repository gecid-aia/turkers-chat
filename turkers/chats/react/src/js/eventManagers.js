import { fetchFromApi } from "rel-events";
import { cloneDeep as _cloneDeep } from 'lodash';

export class GetChatMessagesEventManager {
  initialState = { results: {} };

  call = ({ messagesUrl }) => () => fetchFromApi(messagesUrl);

  onDispatch = state => state;
  onFailure = state => state;
  onSuccess = (state, event) => {
    const newState = _cloneDeep(state);
    newState.results[event.extraData.messagesUrl] = event.response.data.results;
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
  initialState = {}
  call = ({ messagesUrl, message }) => {
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
