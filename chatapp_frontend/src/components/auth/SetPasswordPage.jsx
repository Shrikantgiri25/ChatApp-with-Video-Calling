import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import { Button } from "antd";
import * as Yup from "yup";
import { AuthService } from "../../services/authService";
import "./Login.scss";

// Validation schema
const SetPasswordSchema = Yup.object().shape({
  password: Yup.string()
    .min(6, "Password must be at least 6 characters")
    .required("Password is required"),
  confirm_password: Yup.string()
    .oneOf([Yup.ref("password"), null], "Passwords must match")
    .required("Confirm Password is required"),
});

const SetPasswordPage = () => {
  const navigate = useNavigate();
  const { token } = useParams(); // token_id from URL

  const INITIAL_VALUES = {
    password: "",
    confirm_password: "",
  };
  
  return (
    <div className="auth-page">
      {/* Header */}
      <div className="dashboard-header">
        <div className="chatapp-logo">
          <span className="chatapp-text">Chat </span>
          <span className="x-text">Application</span>
        </div>
        <h1 className="main-title">Set Your Password</h1>
      </div>

      <Formik
        initialValues={INITIAL_VALUES}
        validationSchema={SetPasswordSchema}
        validateOnMount
        onSubmit={async (values, { setSubmitting, setStatus, resetForm }) => {
          try {
            const response = await AuthService.setPassword({
              token_id: token,
              password: values.password,
              confirm_password: values.confirm_password,
            });

            if (response?.success) {
              setStatus("Password set successfully! Redirecting to login...");
              resetForm();
              setTimeout(() => navigate("/login", {replace: true}), 2000);
            } else {
              setStatus(response?.message || "Something went wrong");
            }
          } catch (error) {
            setStatus(error?.response?.data?.message || "Something went wrong");
          } finally {
            setSubmitting(false);
          }
        }}
      >
        {({ isSubmitting, isValid, status }) => (
          <Form className="auth-form">
            <h2>Set Password</h2>

            <label>New Password</label>
            <Field
              type="password"
              name="password"
              placeholder="Enter new password"
            />
            <ErrorMessage
              name="password"
              component="div"
              className="error-message"
            />

            <label>Confirm Password</label>
            <Field
              type="password"
              name="confirm_password"
              placeholder="Confirm new password"
            />
            <ErrorMessage
              name="confirm_password"
              component="div"
              className="error-message"
            />

            {status && <p className="status-message">{status}</p>}

            <Button
              type="primary"
              htmlType="submit"
              className="submit-button"
              loading={isSubmitting}
              disabled={!isValid || isSubmitting}
              block
            >
              Set Password
            </Button>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default SetPasswordPage;
