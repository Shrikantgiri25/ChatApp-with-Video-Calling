import React from 'react'
import { Formik, Form, Field, ErrorMessage } from "formik";
import { Button } from "antd";
import { LoginSchema } from '../../validation/loginValidation';
import { AuthService } from '../../services/authService';

export const Login = () => {
  const INITIAL_VALUES = {
    email: "", 
    password: ""
} 
  return (
    <Formik
    initialValues={INITIAL_VALUES}
    validationSchema={LoginSchema}
    onSubmit={async (values)=> {
        console.log(values);
        const response = await AuthService.login(values);
        const accessToken = response?.access;
        if (accessToken){
            localStorage.setItem("access_token", accessToken);
        }
        const refreshToken = response?.refresh;
        if (refreshToken){
            localStorage.setItem("refresh_token", refreshToken);
        }
    }}
    >
    {({isSubmitting, isValid}) => (
        <Form className='form-style'>
            <div>
                <label>Email</label>
                <Field type="email" name="email" placeholder="Enter your email"/>
                <ErrorMessage name='email' component="div" style={{color: "red"}}/>
            </div>
            <div>
                <label>Password</label>
                <Field type="password" name="password" placeholder="Enter your password"/>
                <ErrorMessage name='password' component="div" style={{color: "red"}}/>
            </div>
            <Button htmlType='submit' type='primary' disabled={isSubmitting || !isValid}>
                Login
            </Button>
        </Form>
    )}
    </Formik>
  )
}
