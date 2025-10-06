// ChatListHeader.jsx

import React from 'react';
import UserListPane from "./UserListPane";
import "../ChatListPane/ChatListPane.scss"
import { USERLIST_SEARCH } from '../../../store/actiontypes/constants';
import { selectUserListSearch } from '../../../store/selectors/searchSelector';
import { useDispatch, useSelector } from 'react-redux';
const UserListHeader = () => {
  const userSearch = useSelector(selectUserListSearch);
  const dispatch = useDispatch();
  return (
    // APPLY FULL HEIGHT AND FLEX DIRECTION HERE
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}> 
      <div className="header-wrapper">
        <h2 className="chatapp-title">Users</h2>
        <input className="searchText" value={userSearch} type="text" placeholder="Search..." onChange={(e) =>
                    dispatch({ type: USERLIST_SEARCH, payload: e.target.value })
                  }/>
      </div>
      
      {/* This is the main fix: Make the ChatListPane take all remaining vertical space 
        and handle its own scrolling.
      */}
      <UserListPane search={userSearch}/> 
    </div>
  )
}

export default UserListHeader