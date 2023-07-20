
import Table from "../Table.jsx";
export default function Payments() {


    return (
        <div className="flex flex-col ">
            <h3 className="text-gray-800 text-xl font-bold sm:text-2xl">
                Платежи
            </h3>
            <p className="text-gray-600 mt-2">
                Здесь отображаются платежи за все время.
            </p>
            <Table endPoint='payments' tableTypes={[{'№':'text'},{'id':'text'},{'Фио':'text'},{'Дата платежа':'text'}]}/>
        </div>
    )
}
