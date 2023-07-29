import Menu from "./menu.jsx";
import {Outlet} from "react-router-dom";
import users from './assets/users.svg'
import payments from './assets/paymens.svg'
import completed from './assets/complited.svg'
import feedback from './assets/feedback.svg'
export default function App() {
    let sections = [{title: 'Пользователи', icon: users, link: '/'}, {
        title: 'Платежи',
        icon: payments,
        link: '/payments'
    }, {title: 'Завершившие', icon: completed, link: '/completed'},
        {title: 'отзывы',icon: feedback,link: '/feedback'}]
    return (
        <div className='flex flex-row  mt-3 gap-x-96'>
            <Menu sections={sections}/>
            <Outlet/>
        </div>
    )
}


