from reservation_system import ReservationSystem
import sys


class RestaurantApp:
    def __init__(self):
        self.system = ReservationSystem()

    def display_menu(self):
        """Отображение главного меню"""
        print("\n" + "=" * 50)
        print("       СИСТЕМА БРОНИРОВАНИЯ РЕСТОРАНА")
        print("=" * 50)
        print("1. Найти свободные столики")
        print("2. Забронировать столик")
        print("3. Отменить бронирование")
        print("4. Найти мои бронирования")
        print("5. Выйти")
        print("-" * 50)

    def find_available_tables(self):
        """Поиск свободных столиков"""
        print("\n--- Поиск свободных столиков ---")

        date = input("Введите дату (ГГГГ-ММ-ДД): ")
        time = input("Введите время (ЧЧ:ММ): ")
        guests = int(input("Количество гостей: "))

        tables = self.system.get_available_tables(date, time, guests)

        if not tables:
            print("К сожалению, нет свободных столиков на указанное время.")
            return

        print(f"\nНайдено {len(tables)} свободных столиков:")
        for table in tables:
            print(f"Столик №{table.table_number} (вместимость: {table.capacity} чел.)")

    def make_reservation(self):
        """Создание бронирования"""
        print("\n--- Бронирование столика ---")

        date = input("Дата (ГГГГ-ММ-ДД): ")
        time = input("Время (ЧЧ:ММ): ")
        guests = int(input("Количество гостей: "))

        # Показываем доступные столики
        tables = self.system.get_available_tables(date, time, guests)
        if not tables:
            print("Нет свободных столиков на указанное время.")
            return

        print("\nДоступные столики:")
        for table in tables:
            print(f"{table.id}. Столик №{table.table_number} (до {table.capacity} чел.)")

        table_id = int(input("\nВыберите номер столика: "))
        name = input("Ваше имя: ")
        phone = input("Ваш телефон: ")

        if self.system.make_reservation(table_id, name, phone, date, time, guests):
            print("Бронирование успешно создано!")
        else:
            print("Ошибка при создании бронирования.")

    def cancel_reservation(self):
        """Отмена бронирования"""
        print("\n--- Отмена бронирования ---")
        phone = input("Введите ваш телефон: ")

        reservations = self.system.get_reservations_by_phone(phone)
        if not reservations:
            print("Активных бронирований не найдено.")
            return

        print("\nВаши бронирования:")
        for res in reservations:
            print(f"{res.id}. {res.reservation_date} {res.reservation_time} - {res.customer_name}")

        res_id = int(input("\nВведите номер бронирования для отмены: "))

        if self.system.cancel_reservation(res_id):
            print("Бронирование отменено!")
        else:
            print("Ошибка при отмене бронирования.")

    def find_my_reservations(self):
        """Поиск бронирований по телефону"""
        print("\n--- Мои бронирования ---")
        phone = input("Введите ваш телефон: ")

        reservations = self.system.get_reservations_by_phone(phone)
        if not reservations:
            print("Активных бронирований не найдено.")
            return

        print("\nВаши активные бронирования:")
        for res in reservations:
            print(f"Дата: {res.reservation_date} Время: {res.reservation_time}")
            print(f"Имя: {res.customer_name}")
            print(f"Телефон: {res.customer_phone}")
            print(f"Гостей: {res.guests_count}")
            print()

    def run(self):
        """Запуск приложения"""
        print("Добро пожаловать в систему бронирования ресторана!")
        while True:
            self.display_menu()
            choice = input("Выберите действие (1-5): ")

            if choice == '1':
                self.find_available_tables()
            elif choice == '2':
                self.make_reservation()
            elif choice == '3':
                self.cancel_reservation()
            elif choice == '4':
                self.find_my_reservations()
            elif choice == '5':
                print("До свидания!")
                sys.exit()
            else:
                print("Неверный выбор. Попробуйте снова.")

        # Этот код должен быть ВНЕ класса, в самом конце файла
if __name__ == "__main__":
    app = RestaurantApp()
    app.run()