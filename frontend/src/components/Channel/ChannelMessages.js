import React from 'react';
import axios from 'axios';

import { List, ListSubheader, Button } from '@material-ui/core';
import { pollingInterval, getIsPolling, subscribeToStep, unsubscribeToStep } from '../../utils/update';
import Message from '../Message';
import AuthContext from '../../AuthContext';
import { toast } from 'react-toastify';
import { CHANNEL_ERROR_TEXT } from '../../utils/text';
import AddMessage from '../Message/AddMessage';
import { useInterval } from '../../utils';

function ChannelMessages({ channel_id = '' }) {
  const [messages, setMessages] = React.useState([]);
  const [currentStart, setCurrentStart] = React.useState(0);
  const token = React.useContext(AuthContext);
  
  const fetchChannelMessages = () => axios
  .get('/channel/messages', {
    params: {
      token,
      channel_id,
      start: currentStart,
    },
  })
  .then(({ data }) => {
    const { messages: newMessages, start, end } = data;
    setCurrentStart(end); // TODO: add/remove problems
    setMessages(messages.concat(newMessages));
  })
  .catch((err) => {
    console.error(err);
    toast.error(CHANNEL_ERROR_TEXT);
  });

  const resetChannelMessages = () => axios
  .get('/channel/messages', {
    params: {
      token,
      channel_id,
      start: 0,
    },
  })
  .then(({ data }) => {
    const { messages: newMessages, start, end } = data;
    setCurrentStart(end); // TODO: add/remove problems
    setMessages(newMessages);
  })
  .catch((err) => {
    console.error(err);
    toast.error(CHANNEL_ERROR_TEXT);
  });

  React.useEffect(() => {
    fetchChannelMessages();
    subscribeToStep(fetchChannelMessages);
    return () => unsubscribeToStep(fetchChannelMessages);
  }, [channel_id])

  return (
    <>
      <hr />
      {
        (currentStart != -1 && 
          <Button
            variant="outlined"
            color="secondary"
            onClick={() => fetchChannelMessages()}
          >
            Previous messages
          </Button>
        )
      }
      <List
        subheader={<ListSubheader>Messages</ListSubheader>}
        style={{ width: '100%' }}
      >
        {messages.slice().reverse().map((message) => (
          <Message {...message} />
        ))}
      </List>
      <AddMessage onAdd={resetChannelMessages} channel_id={channel_id} />
    </>
  );
}

export default ChannelMessages;
