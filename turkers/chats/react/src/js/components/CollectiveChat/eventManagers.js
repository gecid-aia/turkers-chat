import { fetchFromApi } from "rel-events"

export class GetCollectiveChatMessagesEventManager {
  initialState = { results: [] };

  call = () => () => fetchFromApi('/api/chat/1/messages/');

  onDispatch = state => state;
  onFailure = state => state;
  onSuccess = (state, { response: { data: { results } } }) => ({ ...state, results });
}

export class SendMessageEventManager {
  initialState = {}
  call = ({ chatId, message }) => {
    const requestData = {
      method: 'POST',
      body: JSON.stringify({
        content: message,
      })
    };

    return () => fetchFromApi(`/api/chat/${chatId}/messages/`, requestData);
  };

  onDispatch = state => state;
  onFailure = state => state;
  onSuccess = state => state;
}
