import { toast } from 'react-toastify';
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

      const method = response.config.method?.toUpperCase();

      if ([200, 201].includes(response.status) && method !== "GET") {
        const successMessage =
          response.data?.message ||
          (response.status === 201 ? "Created successfully!" : "Successfull");

        toast.success(successMessage, {
          position: "top-right",
          autoClose: 2000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
        });
      }
    } catch (error) {
      console.error("Create group failed:", error);
    } finally {
      setSubmitting(false);
    }
  }
};
