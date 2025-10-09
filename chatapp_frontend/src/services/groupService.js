import api from '../api/api';

export const groupService = {
  createGroup: async (values, setSubmitting = () => {}) => {
    try {
      const formData = new FormData();

      formData.append("group_name", values.group_name);
      formData.append("description", values.description || "");
      if (values.group_avatar) {
        formData.append("group_avatar", values.group_avatar);
      }

      // Append members (multiple IDs)
      values.members.forEach(memberId => {
        formData.append("members", memberId);
      });

      const response = await api.post("/group/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.status === 201) {
        console.log("Group created successfully!");
      }
    } catch (error) {
      console.error("Create group failed:", error);
    } finally {
      setSubmitting(false);
    }
  }
};
