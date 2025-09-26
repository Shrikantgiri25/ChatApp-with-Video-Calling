import React from 'react'
import { Layout, Menu, Tooltip} from "antd";
import { Outlet, useLocation } from "react-router-dom";
import { MessageOutlined, PhoneOutlined, ExperimentOutlined } from '@ant-design/icons';
import { useSelector } from "react-redux";
import { UserProfileDetails } from '../../store/selectors/authselectors';
import "./MainLayout.scss";

const { Sider, Content } = Layout;

const MainLayout = () => {
  const location = useLocation();
  const hiddenSidebarRoutes = ["/login", "/register", "user/:token/set-password/", "/verify/:token/email/"];
  const shouldShowSidebar = !hiddenSidebarRoutes.includes(location.pathname);
  const userProfileData = useSelector(UserProfileDetails);
  const userProfilePicture = userProfileData && `${import.meta.env.VITE_API_BASE_URL}${userProfileData?.profile?.profile_picture}` 

  return (
    <Layout className="main-layout">
      {shouldShowSidebar && (
        <Sider width={80} className="sidebar">
          <Menu mode="inline" defaultSelectedKeys={['messages']} className="menu-main">
            <Menu.Item key="messages" icon={
              <Tooltip title="Messages" placement="right">
                <MessageOutlined style={{ fontSize: '24px' }}/>
              </Tooltip>
            }/>
            <Menu.Item key="calls" icon={
              <Tooltip title="Calls" placement="right">
                <PhoneOutlined style={{ fontSize: '24px' }}/>
              </Tooltip>
              }/>

            <Menu.Item key="chatbot" icon={
              <Tooltip title="Chatbot" placement="right">
                <ExperimentOutlined style={{ fontSize: '24px' }}/>
              </Tooltip>
            }/>
          </Menu>

          <Menu mode="inline" className="menu-profile">
            <Menu.Item key="profile" icon={
              <Tooltip title="Profile" placement="right">
              <img 
                src={userProfilePicture || "https://via.placeholder.com/32"} 
                alt="Profile" 
                className="profile-img"
              />
              </Tooltip>
            } />
          </Menu>
        </Sider>
      )}
      <Layout>
        <Content className="content">
          <Outlet/>
        </Content>
      </Layout>
    </Layout>
  )
}

export default MainLayout;
