import {useEffect, useRef, useState} from "react"
import DatePicker, {registerLocale, setDefaultLocale} from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import ru from 'date-fns/locale/ru';


// eslint-disable-next-line react/prop-types
export default function Table({endPoint, tableTypes}) {
    registerLocale('ru', ru)
    setDefaultLocale('ru')
    let [items, setItems] = useState([])
    let [isEdit, setIsEdit] = useState(false)
    let deleteItems=useRef([])
    useEffect(() => {
        fetch(`${import.meta.env.VITE_API_PATH}${endPoint}`).then(r => r.json()).then(res => setItems(res))
    }, [endPoint])

    function checkColumType(type, content, name, user_id) {
        switch (type) {
            case 'text':
                return content
            case 'edit':
                return <input type={"text"} name={name} className='bg-inherit' value={content}
                              onChange={(e) => handleEdit(e, user_id)}/>
            case 'bool':
                return <input type={"checkbox"} name={name} className='bg-inherit cursor-pointer' checked={content}
                              onChange={(e) => handleEdit({
                                  target: {
                                      value: !!e.target.checked,
                                      name: e.target.name
                                  }
                              }, user_id)}/>
            case 'date':
                return <DatePicker name={name} className='bg-inherit cursor-pointer' dateFormat="yyyy/MM/dd" minDate={new Date()}
                                   selected={new Date(content)}
                                   onChange={(e) => handleEdit({target: {name: `${name}`, value: e}}, user_id)}/>
            default:
                return '-'
        }
    }

    function rowIter(obj, user_id) {
        return Object.entries(obj).map(([key, value], index) => (
             <td key={index} className="px-6 py-4 whitespace-nowrap">{checkColumType(Object.values(tableTypes[index])[0], value, key, user_id)}</td>
    ))

    }

    function handleEdit(e, id) {
        let {name, value} = e.target
        let editData = items.map((item) =>
            item.user_id === id && name ? {...item, [name]: value} : item
        )
        setItems(editData)
        setIsEdit(true)
    }
    function deleteRow(row) {
        let editData= items.filter( a=>{ a.user_id!==row && deleteItems.current.push(a.user_id)  ; return  a.user_id!==row})
        setItems(editData)
        setIsEdit(true)
    }

    function sendChanges(data) {
        if (deleteItems.current.length>0){
            deleteData(deleteItems.current)
            deleteItems.current=[]
        }
        fetch(`${import.meta.env.VITE_API_PATH}${endPoint}`, {
            method: 'post',
            headers: {'Content-Type': 'application/json;'},
            body: JSON.stringify(data)
        }).then(res => res.json())

        setIsEdit(false)
    }

    function deleteData(targets){
            fetch(`${import.meta.env.VITE_API_PATH}${endPoint}`, {
            method: 'delete',
            headers: {'Content-Type': 'application/json;'},
            body: JSON.stringify(targets)
        }).then(res => res.json())

    }
    return (
        <div className="max-w-screen-xl mx-auto">
            <div className="mt-12 shadow-sm border rounded-lg overflow-x-auto">
                <table className="w-full table-auto text-sm text-left">
                    <thead className="text-gray-600 font-medium border-b">
                    <tr className>
                        {tableTypes.map(item => <th key={Object.keys(item)} className='py-3 px-6'>{Object.keys(item)}</th>)}
                    </tr>
                    </thead>
                    <tbody className="text-gray-600 divide-y">

                    {items.map((item) => (
                        <tr key={item.user_id} className="odd:bg-gray-50 even:bg-white">
                            {rowIter(item, item.user_id)}
                            <td className="text-right px-6 whitespace-nowrap">
                                <button
                                    onClick={()=> deleteRow(item.user_id)}
                                    className="py-2 leading-none px-3 font-medium text-red-600 hover:text-red-700 duration-150 hover:bg-gray-50 rounded-lg">
                                    удалить
                                </button>
                            </td>
                        </tr>
                    ))}

                    </tbody>
                </table>

            </div>
            <span
                className='text-red-700 text-sm m-4'>{isEdit && '* после из мнений не забудьте отправить на сервер'}</span>
            <button
                onClick={() => sendChanges(items)}
                disabled={!isEdit}
                className=" block  mx-auto  mt-5 rounded cursor-pointer border disabled:cursor-not-allowed border-green-600 bg-green-600 px-12 py-3 text-sm font-medium text-white hover:bg-transparent hover:text-green-600 focus:outline-none focus:ring active:text-green-500 disabled:opacity-25 ">
                отправить на сервер
            </button>
        </div>
    )
}