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

  // Function to handle moving back to the chat list
  const handleGoBack = () => {
    setCreateGroup(false);
    // You might also want to clear the user search here
    dispatch({ type: USERLIST_SEARCH, payload: "" });
  }

  // Simplified handleMenuClick: only handles 'New Group' now
  const handleMenuClick = ({ key }) => {
    if (key === "new_group") setCreateGroup(true);
  };
  
  // Simplified optionsMenu: only shows "New Group"
  const optionsMenu = (
    <Menu
      onClick={handleMenuClick}
      items={[
        { key: "new_group", label: "New Group", icon: <UsergroupAddOutlined /> }
      ]}
    />
  );
  
  // Logic for rendering the appropriate header content
  const renderHeaderContent = () => {
    // State 1: In Group Creation (Add Group Members)
    if (createGroup) {
      return (
        // New structure for back button and title
        <div className="group-creation-header">
          {/* Back Button */}
          <Tooltip title="Back to Chats">
            <ArrowLeftOutlined 
              className="back-icon" 
              onClick={handleGoBack} 
            />
          </Tooltip>
          {/* Title for the current view */}
          <h2 className="chatapp-title">{showGroupForm ? "Create Group" : "Add Group Members"}</h2>
        </div>
      );
    } 
    
    // State 2: Normal Chat List (Title, Search, Kebab)
    return (
      <>
        <h2 className="chatapp-title">{"Chat Application"}</h2>
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
          <Dropdown overlay={optionsMenu} trigger={['click']} placement="bottomRight">
            <Tooltip title="More Options" placement='topLeft'>
              <FontAwesomeIcon className="kebab-icon" icon={faEllipsisVertical} />
            </Tooltip>
          </Dropdown>
        </div>
      </>
    );
  };
  
  // The original structure for the User List Pane's search bar still needs to be handled
  const renderGroupSearch = () => {
      // If we are in the User List/Group Creation view, show the search bar
      if (createGroup) {
          return (
             <div className="search-wrapper group-search-only">
               <input
                 className="searchText"
                 value={userSearch}
                 type="text"
                 placeholder="Search Users..."
                 onChange={(e) =>
                   dispatch({ type: USERLIST_SEARCH, payload: e.target.value })
                 }
               />
             </div>
          );
      }
      return null;
  }
  
  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <div className="header-wrapper">
        {/* Render the appropriate header content */}
        {renderHeaderContent()}

        {/* Render search input ONLY when adding group members (or showGroupForm is false) */}
        { !showGroupForm && createGroup && renderGroupSearch() }
      </div>

      {/* Chat List Pane */}
      {
        createGroup 
          ? <UserListPane 
              search={userSearch} 
              isGroupCreation={createGroup} 
              showGroupForm={showGroupForm} 
              setShowGroupForm={setShowGroupForm} 
              setCreateGroup={setCreateGroup}
            /> 
          : <ChatListPane search={conversationSearch} />
      }
    </div>
  );
};

export default ChatListHeader;  