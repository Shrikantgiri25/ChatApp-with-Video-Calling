import React from 'react';
import ChatListPane from './ChatListPane';
import "./ChatListPane.scss";
import { useDispatch, useSelector } from 'react-redux';
import { selectConversationSearch } from '../../../store/selectors/searchSelector';
import { CONVERSATIONLIST_SEARCH } from '../../../store/actiontypes/constants';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEllipsisVertical } from "@fortawesome/free-solid-svg-icons";
import { Dropdown, Tooltip } from 'antd';

const ChatListHeader = () => {
  const conversationSearch = useSelector(selectConversationSearch);
  const dispatch = useDispatch();

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <div className="header-wrapper">
        <h2 className="chatapp-title">Chat Application</h2>

        {/* Search input and kebab menu in one line */}
        <div className="search-wrapper">
          <input
            className="searchText"
            value={conversationSearch}
            type="text"
            placeholder="Search..."
            onChange={(e) =>
              dispatch({ type: CONVERSATIONLIST_SEARCH, payload: e.target.value })
            }
          />
          <Dropdown overlay={[]} trigger={['click']} placement="bottomRight">
            <Tooltip title="More Options">
              <FontAwesomeIcon className="kebab-icon" icon={faEllipsisVertical} />
            </Tooltip>
          </Dropdown>
        </div>
      </div>

      {/* Chat List Pane */}
      <ChatListPane search={conversationSearch} />
    </div>
  );
};

export default ChatListHeader;
