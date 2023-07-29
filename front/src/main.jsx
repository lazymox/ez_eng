import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import {createBrowserRouter, RouterProvider} from "react-router-dom";
import Users from "./pages/Users.jsx";
import Payments from "./pages/Payments.jsx";
import Completed from "./pages/Completed.jsx";
import Feedback from "./pages/Feedback.jsx";

const router = createBrowserRouter([
    {
        path: '/',
        element: <App/>,
        children: [
            {path:'/',
            element:<Users/>},
            {
                path: '/payments',
                element: <Payments/>
            },
            {
                path: '/completed',
                element: <Completed/>
            },
            {
                path: '/feedback',
                element: <Feedback/>
            },
        ]
    },


])
ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <RouterProvider router={router}/>
    </React.StrictMode>,
)
