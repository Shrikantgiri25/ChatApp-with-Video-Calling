import React, { useState } from "react";
import { Button, Input, message } from "antd";
import { ArrowLeftOutlined, CheckOutlined, UserAddOutlined } from "@ant-design/icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPen, faTrash } from "@fortawesome/free-solid-svg-icons";
import "./ProfilePane.scss";
import { useDispatch, useSelector } from "react-redux";
import { UserProfileDetails } from "../../../store/selectors/authselectors";
import { Formik, Form, Field } from "formik";
import { userProfileService } from "../../../services/userProfileService";
import { LOGIN_SUCCESS } from "../../../store/actiontypes/constants";

const ProfilePane = ({ selectedUserId="", setSelectedUserId = () => {} }) => {
  const dispatch = useDispatch();
  const userProfileData = useSelector(UserProfileDetails);

  const [isEditingName, setIsEditingName] = useState(false);
  const [isEditingBio, setIsEditingBio] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const initialValues = {
    full_name: userProfileData?.full_name || "",
    bio: userProfileData?.profile?.bio || "",
    profile_picture:
      userProfileData?.profile?.profile_picture
        ? `${import.meta.env.VITE_API_BASE_URL}${userProfileData.profile.profile_picture}`
        : null,
  };

  // Handles submitting Formik values to backend
  const handleSubmitForm = async (values) => {
    if (isSubmitting) return;
    
    setIsSubmitting(true);
    const formData = new FormData();
    
    // Always send full_name
    formData.append("full_name", values.full_name || "");
    
    // Always send bio
    formData.append("bio", values.bio || "");
    
    // Handle profile_picture
    if (values.profile_picture instanceof File) {
      // New file uploaded
      formData.append("profile_picture", values.profile_picture);
    } else if (values.profile_picture === null) {
      // User deleted the picture - send empty string
      formData.append("profile_picture", "");
    }
    // If it's a string URL, don't send it (no change)

    try {
      const response = await userProfileService.patchUserDetails(formData);
      
      if (response?.data?.data) {
        // Update Redux store with new data
        dispatch({ type: LOGIN_SUCCESS, payload: response.data.data });
        message.success("Profile updated successfully!");
      }
    } catch (err) {
      console.error("Failed to update profile", err);
      message.error("Failed to update profile");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="profile-form-container">
      <div className="profile-form">
        {/* Header */}
        <div className="form-header">
          <h2>{selectedUserId ? "User" : "My"} Profile</h2>
        </div>

        <Formik
          initialValues={initialValues}
          enableReinitialize
          onSubmit={handleSubmitForm}
        >
          {({ values, setFieldValue, handleSubmit }) => (
            <Form>
              {/* Profile Picture */}
              <div className="profile-upload-container">
                <input
                  type="file"
                  accept="image/*"
                  id="profile_avatar_input"
                  style={{ display: "none" }}
                  onChange={(e) => {
                    if (e.target.files[0]) {
                      setFieldValue("profile_picture", e.target.files[0]);
                      // Submit after setting the value
                      setTimeout(() => handleSubmit(), 100);
                    }
                  }}
                />
                <div
                  className="profile-picture-wrapper"
                  onClick={() =>
                    document.getElementById("profile_avatar_input").click()
                  }
                >
                  <div className="profile-picture-preview">
                    {values.profile_picture ? (
                      <img
                        src={
                          typeof values.profile_picture === "string"
                            ? values.profile_picture
                            : URL.createObjectURL(values.profile_picture)
                        }
                        alt="avatar"
                      />
                    ) : (
                      <UserAddOutlined className="profile-icon" />
                    )}
                  </div>

                  {values.profile_picture && (
                    <FontAwesomeIcon
                      icon={faTrash}
                      className="trash-icon"
                      onClick={(e) => {
                        e.stopPropagation();
                        setFieldValue("profile_picture", null);
                        document.getElementById("profile_avatar_input").value = null;
                        // Submit after setting the value
                        setTimeout(() => handleSubmit(), 100);
                      }}
                    />
                  )}
                </div>
              </div>

              {/* Full Name */}
              <div className="editable-field">
                <label>Full Name</label>
                <div className="field-row">
                  <Field name="full_name">
                    {({ field }) => (
                      <Input
                        {...field}
                        placeholder="Enter your full name"
                        readOnly={!isEditingName}
                        className={!isEditingName ? "readonly-input" : ""}
                        onBlur={() => {
                          if (isEditingName) {
                            setIsEditingName(false);
                            handleSubmit();
                          }
                        }}
                        onPressEnter={() => {
                          setIsEditingName(false);
                          handleSubmit();
                        }}
                      />
                    )}
                  </Field>
                  {isEditingName ? (
                    <CheckOutlined
                      className="edit-icon"
                      onClick={() => {
                        setIsEditingName(false);
                        handleSubmit();
                      }}
                    />
                  ) : (
                    <FontAwesomeIcon
                      icon={faPen}
                      className="edit-icon"
                      onClick={() => setIsEditingName(true)}
                    />
                  )}
                </div>
              </div>

              {/* Bio */}
              <div className="editable-field">
                <label>Bio</label>
                <div className="field-row">
                  <Field name="bio">
                    {({ field }) => (
                      <Input.TextArea
                        {...field}
                        rows={3}
                        maxLength={150}
                        placeholder="Write something about yourself..."
                        readOnly={!isEditingBio}
                        className={!isEditingBio ? "readonly-input" : ""}
                        showCount={isEditingBio}
                        onBlur={() => {
                          if (isEditingBio) {
                            setIsEditingBio(false);
                            handleSubmit();
                          }
                        }}
                      />
                    )}
                  </Field>
                  {isEditingBio ? (
                    <CheckOutlined
                      className="edit-icon"
                      onClick={() => {
                        setIsEditingBio(false);
                        handleSubmit();
                      }}
                    />
                  ) : (
                    <FontAwesomeIcon
                      icon={faPen}
                      className="edit-icon"
                      onClick={() => setIsEditingBio(true)}
                    />
                  )}
                </div>
              </div>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
};

export default ProfilePane;