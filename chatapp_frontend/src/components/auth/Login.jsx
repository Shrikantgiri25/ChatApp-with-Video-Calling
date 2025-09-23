import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import { Button } from "antd";
import { LoginSchema } from "../../validation/loginValidation";
import { RegisterSchema } from "../../validation/registerValidation"; // <-- new schema for register
import { AuthService } from "../../services/authService";
import "./Login.scss";

const AuthPage = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // Decide page based on route
  const isLogin = location.pathname === "/login";

  useEffect(() => {
    // Clear tokens on visiting auth pages
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  }, []);

  const INITIAL_VALUES = isLogin
    ? { email: "", password: "" }
    : { email: "", fullName: "" };

  return (
    <div className="auth-page">
      {/* Header */}
      <div className="dashboard-header">
        <div className="chatapp-logo">
          <span className="chatapp-text">Chat </span>
          <span className="x-text">Application</span>
        </div>
        <h1 className="main-title">Connect Seamlessly</h1>
      </div>

      <Formik
        initialValues={INITIAL_VALUES}
        validationSchema={isLogin ? LoginSchema : RegisterSchema}
        validateOnMount
        onSubmit={async (values, { setSubmitting, setStatus, resetForm }) => {
          try {
            if (isLogin) {
              // Login API
              const response = await AuthService.login(values);
              const accessToken = response?.access;
              const refreshToken = response?.refresh;

              if (accessToken) localStorage.setItem("access_token", accessToken);
              if (refreshToken)
                localStorage.setItem("refresh_token", refreshToken);

              navigate("/"); // redirect after login
            } else {
              // Register API
              await AuthService.register(values);
              setStatus("Verification link has been sent to your email!");
              resetForm();
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
            <h2>{isLogin ? "Login" : "Register"}</h2>

            {/* Email field (common) */}
            <label>Email</label>
            <Field type="email" name="email" placeholder="Enter your email" />
            <ErrorMessage
              name="email"
              component="div"
              className="error-message"
            />

            {/* Show password only on login */}
            {isLogin && (
              <>
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
              </>
            )}

            {/* Show full name only on register */}
            {!isLogin && (
              <>
                <label>Full Name</label>
                <Field
                  type="text"
                  name="fullName"
                  placeholder="Enter your full name"
                />
                <ErrorMessage
                  name="fullName"
                  component="div"
                  className="error-message"
                />
              </>
            )}

            {status && <p className="status-message">{status}</p>}

            <Button
              type="primary"
              htmlType="submit"
              className="submit-button"
              loading={isSubmitting}
              disabled={!isValid || isSubmitting}
              block
            >
              {isLogin ? "Login" : "Register"}
            </Button>

            <p className="toggle-text">
              {isLogin ? "Don’t have an account? " : "Already have an account? "}
              <span
                className="toggle-link"
                onClick={() => navigate(isLogin ? "/register" : "/login")}
              >
                {isLogin ? "Register" : "Login"}
              </span>
            </p>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default AuthPage;
