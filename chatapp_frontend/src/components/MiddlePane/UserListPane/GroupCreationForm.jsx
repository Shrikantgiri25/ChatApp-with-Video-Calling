import React from 'react';
import { Formik, Form, Field, ErrorMessage } from "formik";
import { Button } from "antd";
import { UserAddOutlined, ArrowLeftOutlined } from '@ant-design/icons';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash } from "@fortawesome/free-solid-svg-icons";
import { GroupCreationSchema } from '../../../validation/GroupCreationValidation';
import "./GroupCreationForm.scss";


const GroupCreationForm = ({ onBack, selectedUserIds, onSubmit }) => {
  const INITIAL_VALUES = {
    group_name: "",
    description: "",
    group_avatar: null
  };
  
  const handleSubmit = async (values, { setSubmitting }) => {
    // Combine form values with selected user IDs
    const groupData = {
      ...values,
      members: Array.from(selectedUserIds)
    };
    
    await onSubmit(groupData, setSubmitting);
    setSubmitting(false);
  };

  return (
    <div className='group-form-container'>
      <Formik
        initialValues={INITIAL_VALUES}
        validationSchema={GroupCreationSchema}
        validateOnMount
        enableReinitialize
        onSubmit={handleSubmit}
      >
        {({ setFieldValue, values, isSubmitting, isValid, dirty }) => (
          <Form className="group-creation-form">
            <div className="form-header">
              <Button
                type="text"
                icon={<ArrowLeftOutlined />}
                onClick={onBack}
                className="back-button"
              />
              <h2>Create Group</h2>
              <div style={{ width: '32px' }} /> {/* Spacer for alignment */}
            </div>
            
            {/* Group Avatar */}
            <label>Group Avatar </label>
            <div className="profile-upload-container">
              <input
                type="file"
                accept="image/*"
                id="group_avatar_input"
                style={{ display: "none" }}
                onChange={(event) => setFieldValue("group_avatar", event.currentTarget.files[0])}
              />

              <div className="profile-picture-wrapper">
                <div
                  className="profile-picture-preview"
                  onClick={() => document.getElementById("group_avatar_input").click()}
                >
                  {values.group_avatar ? (
                    <img src={URL.createObjectURL(values.group_avatar)} alt="preview" />
                  ) : (
                    <UserAddOutlined className="profile-icon" />
                  )}
                </div>

                {values.group_avatar && (
                  <FontAwesomeIcon
                    icon={faTrash}
                    className="trash-icon"
                    onClick={(e) => {
                      e.stopPropagation();
                      setFieldValue("group_avatar", null);
                      document.getElementById("group_avatar_input").value = null;
                    }}
                  />
                )}
              </div>
            </div>

            {/* Group Name */}
            <label>Group Name *</label>
            <Field
              name="group_name"
              placeholder="Enter group name"
              className="input-field"
            />
            <ErrorMessage name="group_name" component="div" className="error" />

            {/* Description */}
            <label>Description (optional)</label>
            <Field
              as="textarea"
              name="description"
              placeholder="Enter group description (max 100 characters)"
              maxLength={100}
              className="textarea-field"
            />
            <ErrorMessage name="description" component="div" className="error" />

            {/* Selected Members Count */}
            <div className="selected-members-info">
              <span>{selectedUserIds.size} member(s) selected</span>
            </div>

            {/* Submit button */}
            <Button
              type="primary"
              htmlType="submit"
              className="submit-button"
              loading={isSubmitting}
              disabled={!isValid || isSubmitting}
              block
            >
              Create Group
            </Button>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default GroupCreationForm;