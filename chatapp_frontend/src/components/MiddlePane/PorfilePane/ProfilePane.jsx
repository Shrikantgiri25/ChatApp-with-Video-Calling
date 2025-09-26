import { Card, Avatar, Form, Input, Button } from "antd";

const ProfilePane = () => {
  return (
    <Card>
      <Avatar size={64} src="https://via.placeholder.com/150" />
      <Form layout="vertical" style={{ marginTop: 16 }}>
        <Form.Item label="Full Name">
          <Input defaultValue="John Doe" />
        </Form.Item>
        <Form.Item label="Bio">
          <Input.TextArea defaultValue="Hey, I am using ChitChat!" />
        </Form.Item>
        <Button type="primary" block>
          Save Changes
        </Button>
      </Form>
    </Card>
  );
};

export default ProfilePane;
