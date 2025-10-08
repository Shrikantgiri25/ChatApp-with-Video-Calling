import React, { useState } from 'react';
import ChatListPane from './ChatListPane';
import "./ChatListPane.scss";
import { useDispatch, useSelector } from 'react-redux';
import { selectConversationSearch, selectUserListSearch } from '../../../store/selectors/searchSelector';
import { CONVERSATIONLIST_SEARCH, USERLIST_SEARCH } from '../../../store/actiontypes/constants';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEllipsisVertical } from "@fortawesome/free-solid-svg-icons";
import { Dropdown, Menu, Tooltip } from 'antd';
import { UsergroupAddOutlined, ArrowLeftOutlined } from "@ant-design/icons";
import UserListPane from '../UserListPane/UserListPane';



const ChatListHeader = () => {
  const conversationSearch = useSelector(selectConversationSearch);
  const userSearch = useSelector(selectUserListSearch);
  const dispatch = useDispatch();
  const [createGroup, setCreateGroup] = useState(false);
  const [showGroupForm, setShowGroupForm] = useState(false);
  const handleMenuClick = ({ key }) => {
  if (key === "new_group") setCreateGroup(true);
  else setCreateGroup(false)
  };
  const optionsMenu = (
    <Menu
    onClick={handleMenuClick}
      items={[
        !createGroup ? { key: "new_group", label: "New Group", icon:  <UsergroupAddOutlined />} : { key: "back", label: "Back", icon:  <ArrowLeftOutlined />}
      ]}
    />
  );
  
  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <div className="header-wrapper">
          <h2 className="chatapp-title">{showGroupForm ? "Create Group": createGroup ? "Add Group Members" : "Chat Application"}</h2>

          {/* Search input and kebab menu in one line */}
          { !showGroupForm && <div className="search-wrapper">
            <input
              className="searchText"
              value={createGroup ? userSearch: conversationSearch}
              type="text"
              placeholder="Search..."
              onChange={(e) =>
                dispatch(createGroup ? { type: USERLIST_SEARCH, payload: e.target.value } : { type: CONVERSATIONLIST_SEARCH, payload: e.target.value })
              }
            />
            {<Dropdown overlay={optionsMenu} trigger={['click']} placement="bottomRight">
              <Tooltip title="More Options" placement='topLeft'>
                <FontAwesomeIcon className="kebab-icon" icon={faEllipsisVertical} />
              </Tooltip>
            </Dropdown>}
          </div>}
      </div>

      {/* Chat List Pane */}
      {
        createGroup ? <UserListPane search={userSearch} isGroupCreation={createGroup} showGroupForm={showGroupForm} setShowGroupForm={setShowGroupForm}/> : <ChatListPane search={conversationSearch} />
      }
    </div>
  );
};

export default ChatListHeader;
