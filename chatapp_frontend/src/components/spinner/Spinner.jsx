import { Spin } from "antd";
import { LoadingOutlined } from "@ant-design/icons";

const LoadingScreen = () => (
  <div className="spinner-container">
    <Spin
      indicator={
        <LoadingOutlined style={{ fontSize: 64, color: "#861df7" }} spin />
      }
      size="large"
    />
  </div>
);

export default LoadingScreen;
