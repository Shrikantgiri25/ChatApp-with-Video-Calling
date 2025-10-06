// ChatListHeader.jsx

import React from 'react'
import ChatListPane from './ChatListPane'
import "./ChatListPane.scss"
import { useDispatch, useSelector } from 'react-redux'
import { selectConversationSearch } from '../../../store/selectors/searchSelector'
import { CONVERSATIONLIST_SEARCH } from '../../../store/actiontypes/constants'

const ChatListHeader = () => {
  const conversationSearch = useSelector(selectConversationSearch);
  const dispatch = useDispatch();

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <div className="header-wrapper">
        <h2 className="chatapp-title">Chat Application</h2>
        <input
          className="searchText"
          value={conversationSearch}
          type="text"
          placeholder="Search..."
          onChange={(e) =>
            dispatch({ type: CONVERSATIONLIST_SEARCH, payload: e.target.value })
          }
        />
      </div>

      <ChatListPane search={conversationSearch} />
    </div>
  );
};


export default ChatListHeader