import Table from "../Table.jsx";

export default function Feedback() {

    return (<>
        <div className="flex flex-col ">
            <h3 className="text-gray-800 text-xl font-bold sm:text-2xl">
                Отзывы
            </h3>
            <p className="text-gray-600 mt-2">
                Здесь отображаются проблемы и предложения пользователей
            </p>
            <Table endPoint='feedback' tableTypes={[{'№':'text'},{'id':'text'},{'Сообщение':'text'}]}/>
        </div>
    </>)
}
