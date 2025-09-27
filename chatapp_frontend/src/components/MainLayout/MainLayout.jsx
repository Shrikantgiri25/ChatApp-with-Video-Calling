import React, { useState } from 'react';
import { Layout, Menu, Tooltip } from "antd";
import { Outlet, useLocation } from "react-router-dom";
import { MessageOutlined, PhoneOutlined, ExperimentOutlined, ContactsFilled } from '@ant-design/icons';
import { useSelector } from "react-redux";
import { UserProfileDetails } from '../../store/selectors/authselectors';
import ChatListPane from '../MiddlePane/ChatListPane/ChatListPane';
import CallListPane from '../MiddlePane/CallListPane/CallListPane';
import ProfilePane from '../MiddlePane/PorfilePane/ProfilePane';
import "./MainLayout.scss";
import { UserAddOutlined } from '@ant-design/icons';
const { Sider, Content } = Layout;

const MainLayout = () => {
  const location = useLocation();
  const hiddenSidebarRoutes = [
    "/login",
    "/register", 
    "user/:token/set-password/", 
    "/verify/:token/email/"
  ];
  const shouldShowSidebar = !hiddenSidebarRoutes.some(path =>
    location.pathname.startsWith(path)
  );

  const userProfileData = useSelector(UserProfileDetails);

  const [selectedTab, setSelectedTab] = useState("chats");
  const userProfilePicture = userProfileData?.profile?.profile_picture ? <img 
                      src={`${import.meta.env.VITE_API_BASE_URL}${userProfileData?.profile?.profile_picture}`} 
                      alt="Profile" 
                      className="profile-img"
                    /> : <UserAddOutlined className={`profile-icon ${selectedTab === 'profile' ? 'selected' : ''}`} />

  return (
    <Layout className="main-layout">
      {shouldShowSidebar && (
        <>
          {/* Sidebar */}
          <Sider width={80} className="sidebar">
            <Menu mode="inline" selectedKeys={[selectedTab]} className="menu-main">
              <Menu.Item 
                key="chats" 
                onClick={()=> setSelectedTab("chats")}
                icon={
                  <Tooltip title="Chats" placement="right">
                    <MessageOutlined />
                  </Tooltip>
                }
              />
              <Menu.Item 
                key="calls" 
                onClick={()=> setSelectedTab("calls")}
                icon={
                  <Tooltip title="Calls" placement="right">
                    <PhoneOutlined />
                  </Tooltip>
                }
              />
              <Menu.Item 
                key="contacts" 
                onClick={()=> setSelectedTab("contacts")}
                icon={
                  <Tooltip title="Contacts" placement="right">
                    <ContactsFilled />
                  </Tooltip>
                }
              />
              <Menu.Item 
                key="chatbot" 
                disabled
                icon={
                  <Tooltip title="Chatbot" placement="right">
                    <ExperimentOutlined style={{ color: "rgba(229, 29, 247, 0.2)" }}/>
                  </Tooltip>
                }
              />
            </Menu>

            <Menu mode="inline" className="menu-profile">
              <Menu.Item 
                key="profile" 
                onClick={()=> setSelectedTab("profile")}
                icon={
                  <Tooltip title="Profile" placement="right">
                    {userProfilePicture}
                  </Tooltip>
                }
              />
            </Menu>
          </Sider>

          {/* Middle Pane */}
          <div className="middle-pane">
            {selectedTab === "chats" && <ChatListPane />}
            {selectedTab === "calls" && <CallListPane />}
            {selectedTab === "contacts" && <ChatListPane />}
            {selectedTab === "profile" && <ProfilePane />}
          </div>
        </>
      )}

      {/* Main Content */}
      <Layout>
        <Content className="content">
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;
