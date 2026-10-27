import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# SISTEM REKOMENDASI BUKU - COLLABORATIVE FILTERING
# MAT301 Kecerdasan Buatan | Topik: Recommendation Systems
# Raden Affan Harits Taufik (NIM 163241037)


#dataset
data = {
    'Buku A': [5,    4,    1,    5,    2,    np.nan],
    'Buku B': [4,    5,    2,    4,    1,    5     ],
    'Buku C': [np.nan, 3,  5,    4,    5,    4     ],
    'Buku D': [2,    1,    4,    np.nan, 5,  2     ],
    'Buku E': [1,    np.nan, 4,  2,    4,    1     ],
    'Buku F': [3,    2,    np.nan, 3,  np.nan, 3   ],
}

users = ['U1', 'U2', 'U3', 'U4', 'U5', 'U6']
df = pd.DataFrame(data, index=users)


print("SISTEM REKOMENDASI BUKU - COLLABORATIVE FILTERING")

print("\n Dataset Rating Pengguna:")
print("-" * 60)
print(df.to_string())
print("\n  (NaN = belum diberi rating)")

#Hitung Cosine Similarity antar pengguna berdasarkan rating mereka.
# Isi NaN dengan 0 untuk perhitungan similarity
df_filled = df.fillna(0)

sim_matrix = cosine_similarity(df_filled)
sim_df = pd.DataFrame(sim_matrix, index=users, columns=users)

print("\n" )
print("Matriks Cosine Similarity Antar Pengguna:")
print("-" * 60)
print(sim_df.round(4).to_string())

#Top 3 user paling mirip dengan User 1
print("\n" )
print("Top-3 Pengguna Paling Mirip dengan U1:")
print("-" * 60)

sim_u1 = sim_df['U1'].drop('U1').sort_values(ascending=False)
top3 = sim_u1.head(3)

for rank, (user, score) in enumerate(top3.items(), 1):
    print(f"  Peringkat {rank}: {user}  ->  Similarity = {score:.4f}")

#Prediksi rating untuk buku yang belum diratng U1
print("\n" )
print("Prediksi Rating Buku yang Belum Dirating U1:")
print("-" * 60)

unrated_books = df.columns[df.loc['U1'].isna()].tolist()
predictions = {}

for book in unrated_books:
    # Ambil user lain yang sudah merating buku ini
    rated_users = df[book].dropna().index.tolist()
    rated_users = [u for u in rated_users if u != 'U1']

    if not rated_users:
        continue

    numerator   = 0
    denominator = 0

    for user in rated_users:
        sim   = sim_df.loc['U1', user]
        rating = df.loc[user, book]
        numerator   += sim * rating
        denominator += abs(sim)

    predicted = numerator / denominator if denominator != 0 else 0
    predictions[book] = predicted
    print(f"  {book}: prediksi rating = {predicted:.4f}")

#rekomendasi buku untuk U1
print("\n" + "-" * 60)
print("Rekomendasi Buku untuk User 1:")
print("-" * 60)

if predictions:
    sorted_preds = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
    print(f"\n  Urutan rekomendasi berdasarkan prediksi rating:")
    for rank, (book, score) in enumerate(sorted_preds, 1):
        print(f"  {rank}. {book}  ->  Prediksi Rating = {score:.4f}")

    best_book = sorted_preds[0][0]
    best_score = sorted_preds[0][1]
    print(f"\n Rekomendasi utama: {best_book} (prediksi rating: {best_score:.4f})")
else:
    print("  Tidak ada buku yang bisa direkomendasikan.")

print("\n" )
print("  Program selesai.")
print("-" * 60)