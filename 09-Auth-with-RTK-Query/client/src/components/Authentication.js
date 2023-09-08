import React, {useState} from 'react'
import {useHistory} from 'react-router-dom'
import styled from "styled-components";
import { useFormik } from "formik"
import * as yup from "yup"
import { useCreateUserMutation, useLoginUserMutation } from '../app/services/userApi'


function Authentication() {
  const [signUp, setSignUp] = useState(false)
  // const [error, setError] = useState(null)
  
  const history = useHistory()

  const [createUser, {isLoading: loadingSignup, error: signupError}] = useCreateUserMutation()
  const [loginUser, {isLoading: loadingLogin, error: loginError}] = useLoginUserMutation()

  const handleClick = () => setSignUp((signUp) => !signUp)
  const formSchema = yup.object().shape({
    name: yup.string().required("Please enter a user name"),
    email: yup.string().email(),
    password: yup.string().required("Please enter a secure password")
  })


  const formik = useFormik({
    initialValues: {
      name:'',
      email:'',
      password:''
    },
    validationSchema: formSchema,
    onSubmit: (values) => {
        signUp ? createUser(values) : loginUser(values)
        // fetch(signUp?'/signup':'/login',{
        //   method: "POST",
        //   headers: {
        //     "Content-Type": "application/json",
        //   },
        //   body: JSON.stringify(values),
        // })
        // .then(res => {
        //   if(res.ok){
        //     res.json().then(user => {
        //       console.log(user)
        //       history.push('/')
        //     })
        //   } else {

        //     // res.json().then(error => setError(error.message))
        //   }
        // })
       
    },
  })

    return (
        <> 
        {signupError && <h2 style={{color:'red'}}> {signupError.data.message} </h2>}
        {loginError && <h2 style={{color:'red'}}> {loginError.data.message} </h2>}
        <h2>Please Log in or Sign up!</h2>
        <h2>{signUp?'Already a member?':'Not a member?'}</h2>
        <button onClick={handleClick}>{signUp?'Log In!':'Register now!'}</button>
        <Form onSubmit={formik.handleSubmit}>
        <label>
          Username
          </label>
        <input type='text' name='name' value={formik.values.name} onChange={formik.handleChange} />
        <label>
           Password
           </label>
           <input type='password' name='password' value={formik.values.password} onChange={formik.handleChange} />
        {signUp&&(
          <>
          <label>
          Email
          </label>
          <input type='text' name='email' value={formik.values.email} onChange={formik.handleChange} />
           
           </>
        )}
        <input type='submit' value={signUp?'Sign Up!':'Log In!'} />
      </Form>
        </>
    )
}

export default Authentication

export const Form = styled.form`
display:flex;
flex-direction:column;
width: 400px;
margin:auto;
font-family:Arial;
font-size:30px;
input[type=submit]{
  background-color:#42ddf5;
  color: white;
  height:40px;
  font-family:Arial;
  font-size:30px;
  margin-top:10px;
  margin-bottom:10px;
}
`