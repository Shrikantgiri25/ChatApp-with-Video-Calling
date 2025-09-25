import React from 'react';
import { Formik, Form, Field, ErrorMessage } from "formik";
import { Button } from "antd";
import { UserAddOutlined } from '@ant-design/icons';
import { OnBoardingSchema } from '../../validation/OnboardingValidation';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash } from "@fortawesome/free-solid-svg-icons";
import { userProfileService } from '../../services/userProfileService';
import "./OnBoardingPage.scss";
import { useNavigate } from 'react-router-dom';

const OnBoardingPage = () => {
  const navigate = useNavigate();  
  const INITIAL_VALUES = {
    bio: "",
    profile_picture: null
  };
  
  const handleSubmit = async (values, { setSubmitting }) => {
    await userProfileService.patchUserDetails(values, setSubmitting, navigate);
    setSubmitting(false);
  };


  return (
    <div className='main-container'>
      <Formik
        initialValues={INITIAL_VALUES}
        validationSchema={OnBoardingSchema}
        validateOnMount
        enableReinitialize
        // eslint-disable-next-line no-unused-vars
        onSubmit={handleSubmit}
      >
        {({ setFieldValue, values, isSubmitting, isValid, dirty }) => (
          <Form className="onboarding-form">
              <div className="form-header">
                <h2>Complete Your Profile</h2>
                <button
                  type="button"
                  className="skip-button"
                  onClick={() => handleSubmit({bio: "", profile_picture: null}, {setSubmitting: ()=> {}})} // replace with navigate("/dashboard") or similar
                >
                  Skip
                </button>
              </div>
            
            {/* Profile Picture */}
            <label>Profile Picture (optional)</label>
            <div className="profile-upload-container">
              <input
                type="file"
                accept="image/*"
                capture="user"
                id="profile_picture_input"
                style={{ display: "none" }}
                onChange={(event) => setFieldValue("profile_picture", event.currentTarget.files[0])}
              />

              <div className="profile-picture-wrapper">
                <div
                  className="profile-picture-preview"
                  onClick={() => document.getElementById("profile_picture_input").click()}
                >
                  {values.profile_picture ? (
                    <img src={URL.createObjectURL(values.profile_picture)} alt="preview" />
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
                      document.getElementById("profile_picture_input").value = null;
                    }}
                  />
                )}
              </div>
            </div>


            {/* Bio */}
            <label>Bio (optional)</label>
            <Field
              as="textarea"
              name="bio"
              placeholder="Enter your bio (max 50 characters)"
              maxLength={50}
            />
            <ErrorMessage name="bio" component="div" className="error" />

            {/* Submit button */}
            <Button
              type="primary"
              htmlType="submit"
              className="submit-button"
              loading={isSubmitting}
              disabled={!dirty || !isValid || isSubmitting}
              block
            >
              Continue
            </Button>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default OnBoardingPage;
