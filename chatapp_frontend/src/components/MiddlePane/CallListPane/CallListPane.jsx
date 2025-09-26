import { List } from "antd";
import { PhoneOutlined } from "@ant-design/icons";

const CallListPane = () => {
  const calls = [
    { id: 1, name: "Alice", type: "Incoming" },
    { id: 2, name: "Bob", type: "Missed" },
  ];

  return (
    <List
      dataSource={calls}
      renderItem={(call) => (
        <List.Item>
          <PhoneOutlined style={{ marginRight: 8 }} />
          {call.name} - {call.type}
        </List.Item>
      )}
    />
  );
};

export default CallListPane;
