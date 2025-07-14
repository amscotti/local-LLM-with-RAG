import asyncio
import aiohttp
import time
import json
from datetime import datetime
import random

# Конфигурация
BASE_URL = "http://localhost:8081/api"  # Замените на ваш URL
CONCURRENT_USERS = 100
DEPARTMENT_ID = "5"  # Или другой инициализированный отдел

# Тестовые вопросы
TEST_QUESTIONS = [
    "Что такое машинное обучение?",
    "Объясните принципы работы нейронных сетей",
    "Какие есть типы алгоритмов машинного обучения?",
    "Что такое глубокое обучение?",
    "Расскажите про обработку естественного языка",
    "Что такое компьютерное зрение?",
    "Объясните разницу между ИИ и машинным обучением",
    "Что такое reinforcement learning?",
    "Расскажите про этику в ИИ",
    "Какие есть применения ИИ в медицине?"
]

class LoadTester:
    def __init__(self):
        self.results = []
        self.errors = []
        
    async def send_query(self, session, user_id, question):
        """Отправляет запрос и возвращает task_id"""
        try:
            start_time = time.time()
            
            async with session.post(
                f"{BASE_URL}/llm/query",
                json={
                    "question": question,
                    "department_id": DEPARTMENT_ID
                },
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    task_id = data.get("task_id")
                    
                    # Записываем время отправки запроса
                    query_time = time.time() - start_time
                    
                    return {
                        "user_id": user_id,
                        "task_id": task_id,
                        "question": question,
                        "query_sent_at": time.time(),
                        "query_time": query_time,
                        "status": "sent"
                    }
                else:
                    error_text = await response.text()
                    return {
                        "user_id": user_id,
                        "error": f"HTTP {response.status}: {error_text}",
                        "query_time": time.time() - start_time,
                        "status": "failed"
                    }
                    
        except Exception as e:
            return {
                "user_id": user_id,
                "error": str(e),
                "query_time": time.time() - start_time,
                "status": "failed"
            }

    async def get_result(self, session, task_id, user_id, max_attempts=60):
        """Получает результат по task_id с опросом"""
        for attempt in range(max_attempts):
            try:
                async with session.get(
                    f"{BASE_URL}/llm/query/{task_id}",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data["status"] == "completed":
                            return {
                                "user_id": user_id,
                                "task_id": task_id,
                                "status": "completed",
                                "answer_length": len(data.get("answer", "")),
                                "chunks_count": len(data.get("chunks", [])),
                                "attempt": attempt + 1
                            }
                        elif data["status"] == "failed":
                            return {
                                "user_id": user_id,
                                "task_id": task_id,
                                "status": "failed",
                                "error": data.get("error", "Unknown error"),
                                "attempt": attempt + 1
                            }
                        # Если статус "pending" или "processing", продолжаем опрос
                        
                # Ждем перед следующим опросом
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"Ошибка при получении результата для task {task_id}: {e}")
                await asyncio.sleep(2)
                
        # Превышено максимальное количество попыток
        return {
            "user_id": user_id,
            "task_id": task_id,
            "status": "timeout",
            "error": f"Timeout after {max_attempts} attempts",
            "attempt": max_attempts
        }

    async def simulate_user(self, session, user_id):
        """Симулирует одного пользователя"""
        print(f"👤 Пользователь {user_id} начинает тест")
        
        # Выбираем случайный вопрос
        question = random.choice(TEST_QUESTIONS)
        
        start_time = time.time()
        
        # 1. Отправляем запрос
        query_result = await self.send_query(session, user_id, question)
        
        if query_result["status"] == "failed":
            query_result["total_time"] = time.time() - start_time
            self.errors.append(query_result)
            print(f"❌ Пользователь {user_id} - ошибка при отправке запроса")
            return query_result
        
        task_id = query_result["task_id"]
        print(f"📤 Пользователь {user_id} отправил запрос, task_id: {task_id}")
        
        # 2. Получаем результат
        result = await self.get_result(session, task_id, user_id)
        
        # Объединяем результаты
        final_result = {**query_result, **result}
        final_result["total_time"] = time.time() - start_time
        
        if result["status"] == "completed":
            print(f"✅ Пользователь {user_id} получил ответ за {final_result['total_time']:.2f}с")
            self.results.append(final_result)
        else:
            print(f"❌ Пользователь {user_id} - {result['status']}: {result.get('error', 'Unknown')}")
            self.errors.append(final_result)
            
        return final_result

    async def run_load_test(self):
        """Запускает нагрузочный тест"""
        print(f"🚀 Запуск нагрузочного теста: {CONCURRENT_USERS} пользователей")
        print(f"🎯 URL: {BASE_URL}")
        print(f"🏢 Отдел: {DEPARTMENT_ID}")
        print("-" * 50)
        
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            # Создаем задачи для всех пользователей
            tasks = [
                self.simulate_user(session, user_id) 
                for user_id in range(1, CONCURRENT_USERS + 1)
            ]
            
            # Запускаем все задачи одновременно
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = time.time() - start_time
        
        # Анализируем результаты
        self.analyze_results(total_time)
        
        return results

    def analyze_results(self, total_time):
        """Анализирует и выводит результаты теста"""
        print("\n" + "="*60)
        print("📊 РЕЗУЛЬТАТЫ НАГРУЗОЧНОГО ТЕСТА")
        print("="*60)
        
        successful = len(self.results)
        failed = len(self.errors)
        total = successful + failed
        
        print(f"👥 Всего пользователей: {total}")
        print(f"✅ Успешных запросов: {successful} ({successful/total*100:.1f}%)")
        print(f"❌ Неудачных запросов: {failed} ({failed/total*100:.1f}%)")
        print(f"⏱️  Общее время теста: {total_time:.2f} секунд")
        
        if self.results:
            times = [r["total_time"] for r in self.results]
            query_times = [r["query_time"] for r in self.results]
            
            print(f"\n⏱️  ВРЕМЯ ОТВЕТА:")
            print(f"   Среднее: {sum(times)/len(times):.2f}с")
            print(f"   Минимальное: {min(times):.2f}с")
            print(f"   Максимальное: {max(times):.2f}с")
            print(f"   Медиана: {sorted(times)[len(times)//2]:.2f}с")
            
            print(f"\n📤 ВРЕМЯ ОТПРАВКИ ЗАПРОСА:")
            print(f"   Среднее: {sum(query_times)/len(query_times):.3f}с")
            print(f"   Максимальное: {max(query_times):.3f}с")
            
            # Пропускная способность
            rps = successful / total_time
            print(f"\n🚀 ПРОИЗВОДИТЕЛЬНОСТЬ:")
            print(f"   Запросов в секунду: {rps:.2f}")
            print(f"   Среднее время на запрос: {total_time/total:.2f}с")
        
        if self.errors:
            print(f"\n❌ ОШИБКИ:")
            error_types = {}
            for error in self.errors:
                error_type = error.get("error", "Unknown")[:50]
                error_types[error_type] = error_types.get(error_type, 0) + 1
            
            for error_type, count in error_types.items():
                print(f"   {error_type}: {count}")
        
        print("="*60)

async def main():
    tester = LoadTester()
    await tester.run_load_test()

if __name__ == "__main__":
    asyncio.run(main())