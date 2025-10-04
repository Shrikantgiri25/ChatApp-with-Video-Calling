import React, { useEffect, useState } from "react";
import { Layout, Menu, Tooltip } from "antd";
import { useLocation, useNavigate } from "react-router-dom";
import {
  MessageOutlined,
  PhoneOutlined,
  ExperimentOutlined,
  ContactsOutlined,
  UserAddOutlined,
} from "@ant-design/icons";
import { useSelector } from "react-redux";
import { UserProfileDetails } from "../../store/selectors/authselectors";
import ChatListPane from "../MiddlePane/ChatListPane/ChatListPane";
import UserListPane from "../MiddlePane/UserListPane/UserListPane";
import ChatContentPane from "../ContentPane/ChatContentPane";
import UserListContentPane from "../ContentPane/UserListContentPane";
import Dashboard from "../Dashboard/Dashboard";
import "./MainLayout.scss";

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
  }, [location.pathname]);

  const handleMenuClick = ({ key }) => {
    setSelectedChatId(null);
    setSelectedUserId(null);
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

          <Menu mode="inline" className="menu-profile">
            <Menu.Item
              key="profile"
              icon={<Tooltip title="Profile">{userProfilePicture}</Tooltip>}
            />
          </Menu>
        </Sider>
      )}

      <Layout>
        {/* Middle Pane */}
        <Sider width={420} className="middle-pane">
          {selectedTab === "chats" && (
            <ChatListPane setSelectedChatId={setSelectedChatId} />
          )}
          {selectedTab === "users" && (
            <UserListPane setSelectedUserId={setSelectedUserId} />
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
