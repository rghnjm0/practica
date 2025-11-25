from reservation_system_v2 import ReservationSystem
import threading
import time
import random


class StressTester:
    def __init__(self):
        self.system = ReservationSystem()

    def simulate_user(self, user_id, num_operations):
        """Имитация одного пользователя"""
        success = 0
        for i in range(num_operations):
            date = "2024-02-15"
            time_slot = f"{random.randint(18, 21)}:{random.choice(['00', '30'])}"
            guests = random.randint(1, 4)

            tables = self.system.get_available_tables(date, time_slot, guests)
            if tables:
                table = random.choice(tables)
                if self.system.make_reservation(
                        table.id,
                        f"TestUser{user_id}",
                        f"79{user_id:08d}",
                        date,
                        time_slot,
                        guests
                ):
                    success += 1
        return success

    def run_low_stress_test(self):
        """Запуск нагрузочного тестирования с низкой нагрузкой"""
        print(f"\n🚀 НАГРУЗОЧНОЕ ТЕСТИРОВАНИЕ: НИЗКАЯ НАГРУЗКА (5 пользователей)")
        print("=" * 50)

        return self._run_stress_test(num_users=5, operations_per_user=15)

    def run_high_stress_test(self):
        """Запуск нагрузочного тестирования с высокой нагрузкой"""
        print(f"\n🚀 НАГРУЗОЧНОЕ ТЕСТИРОВАНИЕ: ВЫСОКАЯ НАГРУЗКА (10 пользователей)")
        print("=" * 50)

        return self._run_stress_test(num_users=10, operations_per_user=15)

    def _run_stress_test(self, num_users=5, operations_per_user=15):
        """Общий метод для запуска нагрузочного тестирования"""
        print(f"Пользователей: {num_users}")
        print(f"Операций на пользователя: {operations_per_user}")
        print(f"Всего операций: {num_users * operations_per_user}")

        self.system.clear_test_data()
        threads = []
        results = []

        start_time = time.time()

        for user_id in range(num_users):
            thread = threading.Thread(
                target=lambda uid=user_id: results.append(self.simulate_user(uid, operations_per_user))
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        total_time = time.time() - start_time
        total_success = sum(results)
        total_operations = num_users * operations_per_user

        print(f"\n📊 РЕЗУЛЬТАТЫ:")
        print(f"Общее время: {total_time:.2f} сек")
        print(f"Успешных бронирований: {total_success}/{total_operations}")
        print(f"Процент успеха: {(total_success / total_operations) * 100:.1f}%")
        print(f"Операций в секунду: {total_operations / total_time:.2f}")

        return total_success, total_time

    def run_comparative_test(self):
        """Сравнительный тест низкой и высокой нагрузки"""
        print("\n" + "=" * 50)
        print("🔬 СРАВНИТЕЛЬНЫЙ ТЕСТ НАГРУЗКИ")
        print("=" * 50)

        # Низкая нагрузка
        print("\n🧪 НИЗКАЯ НАГРУЗКА (5 пользователей)")
        success1, time1 = self.run_low_stress_test()

        # Высокая нагрузка
        print("\n🧪 ВЫСОКАЯ НАГРУЗКА (10 пользователей)")
        success2, time2 = self.run_high_stress_test()

        # Сравнительная таблица
        print("\n" + "=" * 50)
        print("📋 СРАВНЕНИЕ РЕЗУЛЬТАТОВ")
        print("=" * 50)
        print(f"{'Нагрузка':<15} {'Время (с)':<12} {'Успешно':<12} {'ОПС':<12}")
        print("-" * 50)
        print(f"{'Низкая (5)':<15} {time1:<12.2f} {success1:<12} {(75 / time1):<12.2f}")
        print(f"{'Высокая (10)':<15} {time2:<12.2f} {success2:<12} {(150 / time2):<12.2f}")

        # Анализ производительности
        if time2 > 0:
            speedup = time1 / time2
            efficiency = (success2 / success1) / (10 / 5) * 100  # Эффективность в %
            print(f"\n⚡ Анализ производительности:")
            print(f"Ускорение при высокой нагрузке: {speedup:.2f}x")
            print(f"Эффективность использования ресурсов: {efficiency:.1f}%")

    def clear_all_test_data(self):
        """Очистка всех тестовых данных"""
        print("\n🧹 ОЧИСТКА ТЕСТОВЫХ ДАННЫХ")
        print("=" * 30)

        conn = self.system.db.get_connection()
        cursor = conn.cursor()

        # Подсчет количества записей перед очисткой
        cursor.execute("SELECT COUNT(*) FROM reservations WHERE customer_name LIKE 'TestUser%'")
        count_before = cursor.fetchone()[0]

        # Очистка данных
        cursor.execute("DELETE FROM reservations WHERE customer_name LIKE 'TestUser%'")

        # Подсчет количества записей после очистки
        cursor.execute("SELECT COUNT(*) FROM reservations WHERE customer_name LIKE 'TestUser%'")
        count_after = cursor.fetchone()[0]

        conn.commit()
        conn.close()

        print(f"Удалено тестовых записей: {count_before - count_after}")
        print("✅ Все тестовые данные очищены!")


class OccupancyAnalyzer:
    def __init__(self):
        self.system = ReservationSystem()

    def analyze_occupancy(self, date="2024-02-15"):
        """Анализ заполняемости столиков"""
        print(f"\n📈 АНАЛИЗ ЗАПОЛНЯЕМОСТИ НА {date}")
        print("=" * 50)

        conn = self.system.db.get_connection()
        cursor = conn.cursor()

        # Получаем статистику по времени
        cursor.execute('''
            SELECT reservation_time, COUNT(*) as occupied,
                   (SELECT COUNT(*) FROM tables) as total_tables
            FROM reservations 
            WHERE reservation_date = ? AND status = 'active'
            GROUP BY reservation_time
            ORDER BY reservation_time
        ''', (date,))

        stats = cursor.fetchall()

        # Подсчет общего количества бронирований
        cursor.execute('''
            SELECT COUNT(*) FROM reservations 
            WHERE reservation_date = ? AND status = 'active'
        ''', (date,))
        total_reservations = cursor.fetchone()[0]

        conn.close()

        if not stats:
            print("Нет данных о бронированиях")
            return

        total_tables = stats[0][2] if stats else 0
        overall_occupancy = (total_reservations / total_tables) * 100 if total_tables > 0 else 0

        peak_time = max(stats, key=lambda x: x[1])
        peak_occupancy = (peak_time[1] / peak_time[2]) * 100

        print(f"Общее количество бронирований: {total_reservations}")
        print(f"Общая заполняемость: {total_reservations}/{total_tables} столиков ({overall_occupancy:.1f}%)")
        print("\n📊 Детали по времени:")
        print("-" * 40)

        for time_slot, occupied, total in stats:
            occupancy_rate = (occupied / total) * 100
            print(f"{time_slot}: {occupied}/{total} столиков ({occupancy_rate:.1f}%)")

        print(f"\n🏆 ПИК НАГРУЗКИ: {peak_time[0]} - {peak_occupancy:.1f}%")

# Глобальные экземпляры для использования в main
stress_tester = StressTester()
occupancy_analyzer = OccupancyAnalyzer()


def run_occupancy_analysis():
    """Запуск анализа заполняемости"""
    occupancy_analyzer.analyze_occupancy()


def run_low_stress_test():
    """Запуск низкого нагрузочного тестирования"""
    stress_tester.run_low_stress_test()


def run_high_stress_test():
    """Запуск высокого нагрузочного тестирования"""
    stress_tester.run_high_stress_test()


def run_comparative_test():
    """Запуск сравнительного теста"""
    stress_tester.run_comparative_test()


def clear_test_data():
    """Очистка тестовых данных"""
    stress_tester.clear_all_test_data()