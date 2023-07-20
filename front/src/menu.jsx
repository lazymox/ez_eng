import {Link} from "react-router-dom";
import {useEffect} from "react";

// eslint-disable-next-line react/prop-types
export default function Menu({sections}) {
    function swich() {
        sections.forEach(({link}) => {

            if (link === window.location.pathname) {
                document.querySelector(`a[href='${link}']`).classList.add('bg-green-100')
            }else {
                  document.querySelector(`a[href='${link}']`).classList.remove('bg-green-100')
            }
        })
    }
    useEffect(()=>{
        swich()
    },[sections])
    return (<>
        <ul className='  flex flex-col my-40  '>
            {sections.map(({title, icon, link}, index) => (
                    <li key={index} onClick={swich}>
                        <Link
                            href=""
                            className="flex items-center gap-2  border-transparent px-6 py-3 text-gray-500 hover:border-gray-100 hover:bg-gray-50 hover:text-gray-700"
                            to={link}>
                            <img className="h-5 w-5 opacity-30" src={icon} alt=''/>

                            <span className="text-xl font-light"> {title} </span>
                        </Link>
                    </li>
                )
            )}
        </ul>

    </>)
}
