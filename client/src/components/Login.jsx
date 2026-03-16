import React, { useState } from 'react'
import { ENDPOINTS, instance } from './api'
import {useNavigate} from 'react-router-dom'

const Login = () => {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const navigate =useNavigate()

    const handleOnSubmit=async(e)=>{
        e.preventDefault()
        await instance.post(ENDPOINTS.LOGIN(),{username,password})
        .then(res=>{
            localStorage.setItem("token",res.data.token)
            navigate("/tasks")
        })

    }

    return (
        <>
            <div className='container'>
                <form onSubmit={handleOnSubmit} className='login-form'>
                    <h2>Login</h2>
                    <input type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder='Username'>
                        </input>
                    <input type="password"
                        value={password}
                        onChange={(e)=>setPassword(e.target.value)}
                        placeholder='Password'>
                       
                        </input>
                    <button>Login</button>
                </form>
            </div>
        </>
    )
}

export default Login