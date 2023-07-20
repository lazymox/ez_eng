import Table from "../Table.jsx";

export default function Users() {


    return (
        <div className="flex flex-col  ">
            <h3 className="text-gray-800 text-xl font-bold sm:text-2xl">
                Пользователи бота
            </h3>
            <p className="text-gray-600 mt-2">
                Здесь все текущие пользователи бота. Здесь можно управлять подпиской.
            </p>
            <Table  endPoint={'users'} tableTypes={[{'id':'text'},{'Фио':'edit'},{'Подписан':'bool'},{'Дата подписки':'date'},{'Дата окончания подписки':'date'}]}/>
        </div>
    )
}
