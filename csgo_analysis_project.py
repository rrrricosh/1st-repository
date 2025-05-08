import pandas as pd
import matplotlib.pyplot as plt

# 1. Завантаження даних з правильним роздільником
try:
    df = pd.read_csv("players_stats.csv", sep=';', encoding='utf-8')
    if df.shape[1] == 1:
        df = pd.read_csv("players_stats.csv", sep=',', encoding='utf-8')
except Exception as e:
    print("Помилка при завантаженні CSV:", e)
    exit()

# 2. Огляд даних
print("Перші 5 рядків:")
print(df.head())
print("\nІнформація про дані:")
print(df.info())
print("\nОписова статистика:")
print(df.describe())

# 3. Очищення даних
df = df.drop_duplicates()
df = df.dropna()

# 4. Фільтрація: гравці, які зіграли більше ніж 10 матчів
df_filtered = df[df['maps'] > 10]

# 5. Групування: середній рейтинг за командою
if 'team' in df.columns and 'rating' in df.columns:
    team_ratings = df.groupby('team')['rating'].mean().sort_values(ascending=False)
    print("\nСередній рейтинг по командах:")
    print(team_ratings.head(10))

# 6. Візуалізація: Топ-10 гравців за рейтингом
top_players = df.sort_values(by='rating', ascending=False).head(10)
plt.figure(figsize=(10, 6))
plt.bar(top_players['name'], top_players['rating'], color='skyblue')
plt.title('Топ-10 гравців за рейтингом')
plt.xlabel('Гравець')
plt.ylabel('Рейтинг')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top10_players.png")
plt.show()

# 7. Статистичні показники
print("\nСередній рейтинг:", df['rating'].mean())
print("Медіана рейтингу:", df['rating'].median())
print("Мода рейтингу:", df['rating'].mode()[0])

# 8. Висновки
print("\nВисновок: Найкращі гравці мають рейтинг понад", round(top_players['rating'].min(), 2))
print("Середній рівень тримається на рівні", round(df['rating'].mean(), 2))