from src.recommender import recommend, recommend_hybrid

print("Normal Recommendation:")
print(recommend("Avatar"))

print()

print("Hybrid Recommendation:")
print(recommend_hybrid("Avatar", "Excited"))