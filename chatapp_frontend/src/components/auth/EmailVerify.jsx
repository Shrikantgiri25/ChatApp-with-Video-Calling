import React, { useEffect, useState, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";

import "./EmailVerify.scss";
import { AuthService } from "../../services/authService";
import LoadingScreen from "../Spinner/Spinner";

const EmailVerifyPage = () => {
  const { token } = useParams();
  const navigate = useNavigate();

  const [status, setStatus] = useState("verifying"); // "verifying" | "success" | "error"
  const [message, setMessage] = useState("");
  const called = useRef(false);

  useEffect(() => {
    if (called.current) return;
    called.current = true;

    const verifyEmail = async () => {
      const response = await AuthService.verify(token);

      if (response?.success) {
        setStatus("success");
        setMessage("Email Verified Successfully. Redirecting...");

        // Get token_id from response
        const tokenId = response.data.token_id;

        // Redirect to set-password page after 3 seconds
        setTimeout(() => navigate(`/user/${tokenId}/set-password`), 3000);
      } else {
        setStatus("error");
        setMessage("Invalid or Expired Verification Link");
      }
    };

    verifyEmail();
  }, [token, navigate]);

  return (
    <div className="auth-page">
      <div className="auth-form email-verify-form">
        {status === "verifying" && (
          <div className="spinner-container">
            <LoadingScreen/>
            <h2>Verifying your email...</h2>
          </div>
        )}

        {(status === "success" || status === "error") && (
          <div className="message-container">
            <h2 className={status === "error" ? "error-message" : "success-message"}>
              {message}
            </h2>

            {status === "error" && (
              <button type="button" onClick={() => navigate("/login")} className="back-login-btn">
                Back to Login
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default EmailVerifyPage;
