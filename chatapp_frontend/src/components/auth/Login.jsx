import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import { Button } from "antd";
import { LoginSchema } from "../../validation/loginValidation";
import { AuthService } from "../../services/authService";
import "./Login.scss";

const Login = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Clear token when visiting login page
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  }, []);

  const INITIAL_VALUES = {
    email: "",
    password: "",
  };

  return (
    <div className="auth-page">
      {/* Header (same as code a) */}
      <div className="dashboard-header">
        <div className="chatapp-logo">
          <span className="chatapp-text">Chat{" "}</span>
          <span className="x-text">Application</span>
        </div>
        <h1 className="main-title">Connect Seamlessly</h1>
      </div>

      <Formik
        initialValues={INITIAL_VALUES}
        validationSchema={LoginSchema}
        validateOnMount
        onSubmit={async (values, { setSubmitting, setStatus }) => {
          try {
            const response = await AuthService.login(values);
            const accessToken = response?.access;
            const refreshToken = response?.refresh;

            if (accessToken) {
              localStorage.setItem("access_token", accessToken);
            }
            if (refreshToken) {
              localStorage.setItem("refresh_token", refreshToken);
            }

            navigate("/"); // redirect after login
          } catch (error) {
            setStatus(error?.response?.data?.message || "Login failed");
          } finally {
            setSubmitting(false);
          }
        }}
      >
        {({ isSubmitting, isValid, status }) => (
          <Form className="auth-form">
            <h2>Login</h2>

            <label>Email</label>
            <Field
              type="email"
              name="email"
              placeholder="Enter your email"
            />
            <ErrorMessage
              name="email"
              component="div"
              className="error-message"
            />

            <label>Password</label>
            <Field
              type="password"
              name="password"
              placeholder="Enter your password"
            />
            <ErrorMessage
              name="password"
              component="div"
              className="error-message"
            />

            {status && <p className="error-message">{status}</p>}

            <Button
              type="primary"
              htmlType="submit"
              className="submit-button"
              loading={isSubmitting}
              disabled={!isValid || isSubmitting}
              block
            >
              Login
            </Button>

            <p className="toggle-text">
              Don’t have an account?{" "}
              <span
                className="toggle-link"
                onClick={() => navigate("/register")}
              >
                Register
              </span>
            </p>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default Login;
