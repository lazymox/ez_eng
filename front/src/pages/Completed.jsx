import Table from "../Table.jsx";

export default function Completed() {

    return (<>
        <div className="flex flex-col ">
            <h3 className="text-gray-800 text-xl font-bold sm:text-2xl">
                Завершившие
            </h3>
            <p className="text-gray-600 mt-2">
                Здесь отображаются те кто прошли курс.
            </p>
            <Table endPoint='completed' tableTypes={[{'id':'text'},{'Фио':'text'},{'Номер телефона':'text'},{'Позвонили':'bool'},{'ответ':'edit'}]}/>
        </div>
    </>)
}
