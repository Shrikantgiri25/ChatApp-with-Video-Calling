import React, { useEffect, useState } from "react";
import { Layout, Menu, Tooltip } from "antd";
import { useLocation, useNavigate } from "react-router-dom";
import {
  MessageOutlined,
  PhoneOutlined,
  ExperimentOutlined,
  ContactsOutlined,
  UserAddOutlined,
  LogoutOutlined,
} from "@ant-design/icons";
import { useSelector } from "react-redux";
import { UserProfileDetails } from "../../store/selectors/authselectors";
import ChatContentPane from "../ContentPane/ChatContentPane";
import UserListContentPane from "../ContentPane/UserListContentPane";
import Dashboard from "../Dashboard/Dashboard";
import "./MainLayout.scss";
import ChatListHeader from "../MiddlePane/ChatListPane/ChatListHeader";
import UserListHeader from "../MiddlePane/UserListPane/UserListHeader";
import ProfilePane from "../MiddlePane/PorfilePane/ProfilePane";

const { Sider, Content } = Layout;

const MainLayout = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const userProfileData = useSelector(UserProfileDetails);

  const hiddenSidebarRoutes = ["/login", "/register", "/user/", "/verify/"];
  const shouldShowSidebar = !hiddenSidebarRoutes.some((path) =>
    location.pathname.startsWith(path)
  );

  const [selectedTab, setSelectedTab] = useState("chats");
  const [selectedChatId, setSelectedChatId] = useState(null);
  const [selectedUserId, setSelectedUserId] = useState(null);

  // Highlight sidebar tab based on pathname
  useEffect(() => {
    if (location.pathname.startsWith("/chats")) setSelectedTab("chats");
    else if (location.pathname.startsWith("/users")) setSelectedTab("users");
    // Ensure 'profile' is set as the selected tab if on the profile page
    else if (location.pathname.startsWith("/profile")) setSelectedTab("profile");
  }, [location.pathname]);

  const handleMenuClick = ({ key }) => {
    setSelectedChatId(null);
    setSelectedUserId(null);
    // Note: The logout key should ideally NOT be handled here if it clears state,
    // but we'll include it for navigation to the profile page.
    if (key === "logout") {
      // Direct logout action
      localStorage.clear();
      navigate("/login");
      return;
    }
    
    setSelectedTab(key);
    navigate(`/${key}`);
  };

  const userProfilePicture = userProfileData?.profile?.profile_picture ? (
    <img
      src={`${import.meta.env.VITE_API_BASE_URL}${userProfileData.profile.profile_picture}`}
      alt="Profile"
      className="profile-img"
    />
  ) : (
    <UserAddOutlined
      className={`profile-icon ${selectedTab === "profile" ? "selected" : ""}`}
    />
  );

  return (
    <Layout className="main-layout">
      {shouldShowSidebar && (
        <Sider width={80} className="sidebar">
          {/* Top Main Navigation Menu */}
          <Menu
            mode="inline"
            selectedKeys={[selectedTab]}
            className="menu-main"
            onClick={handleMenuClick}
          >
            <Menu.Item
              key="chats"
              icon={
                <Tooltip title="Chats" placement="right">
                  <MessageOutlined />
                </Tooltip>
              }
            />
            <Menu.Item
              key="users"
              icon={
                <Tooltip title="Users" placement="right">
                  <ContactsOutlined />
                </Tooltip>
              }
            />
            <Menu.Item
              key="calls"
              disabled
              icon={
                <Tooltip title="Calls" placement="right">
                  <PhoneOutlined style={{ color: "rgba(229,29,247,0.2)" }} />
                </Tooltip>
              }
            />
            <Menu.Item
              key="chatbot"
              disabled
              icon={
                <Tooltip title="Chatbot" placement="right">
                  <ExperimentOutlined style={{ color: "rgba(229,29,247,0.2)" }} />
                </Tooltip>
              }
            />
          </Menu>

          {/* Bottom Profile and Logout Menu */}
          <Menu 
            selectedKeys={[selectedTab]}
            onClick={handleMenuClick} 
            mode="inline" 
            className="menu-profile"
          >
            <Menu.Item
              key="profile"
              // The click is handled by the main handler, which navigates to /profile
              icon={<Tooltip title="Profile">{userProfilePicture}</Tooltip>}
            />
            <Menu.Item
              key="logout"
              className="logout-item" // Targeted class for the Menu.Item container
              // The click is handled by the main handler and performs logout
              icon={
                <Tooltip title="Logout">
                  {/* The icon itself, with a unique class for styling the circle */}
                  <LogoutOutlined className="logout-icon-styled" />
                </Tooltip>
              }
            />
          </Menu>
        </Sider>
      )}

      <Layout>
        {/* Middle Pane */}
        <Sider width={420} className="middle-pane">
          {selectedTab === "chats" && (
            <ChatListHeader setSelectedChatId={setSelectedChatId} />
          )}
          {selectedTab === "users" && (
            <UserListHeader setSelectedUserId={setSelectedUserId} />
          )}
          {selectedTab === "profile" && (
            <ProfilePane selectedUserId={selectedUserId} setSelectedUserId={setSelectedUserId} />
          )}
        </Sider>

        {/* Content Pane */}
        <Content className="content-pane">
          {selectedChatId ? (
            <ChatContentPane chatId={selectedChatId} />
          ) : selectedUserId ? (
            <UserListContentPane userId={selectedUserId} />
          ) : (
            <Dashboard />
          )}
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;