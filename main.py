# main.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

# ===============================
# 1. Load Dataset
# ===============================
file_path = "Dataset .csv"  # Update if path differs
df = pd.read_csv(file_path)

print("Dataset Shape:", df.shape)
print(df.head())

# ===============================
# 2. Restaurant Distribution Map
# ===============================
m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=2)

# Add restaurant markers
for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=1,
        color="blue",
        fill=True,
        fill_opacity=0.4
    ).add_to(m)

# Save map
m.save("restaurant_distribution_map.html")
print("✅ Restaurant distribution map saved as restaurant_distribution_map.html")

# ===============================
# 3. Heatmap of Restaurant Density
# ===============================
heatmap_map = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=2)
HeatMap(df[["Latitude", "Longitude"]].dropna().values.tolist(), radius=5).add_to(heatmap_map)
heatmap_map.save("restaurant_heatmap.html")
print("✅ Heatmap saved as restaurant_heatmap.html")

# ===============================
# 4. Restaurants per City
# ===============================
city_counts = df["City"].value_counts().head(20)
plt.figure(figsize=(12,6))
sns.barplot(x=city_counts.values, y=city_counts.index, palette="viridis")
plt.title("Top 20 Cities by Number of Restaurants")
plt.xlabel("Number of Restaurants")
plt.ylabel("City")
plt.tight_layout()
plt.savefig("restaurants_per_city.png")
plt.show()

# ===============================
# 5. Average Rating per City
# ===============================
city_ratings = df.groupby("City")["Aggregate rating"].mean().sort_values(ascending=False).head(20)
plt.figure(figsize=(12,6))
sns.barplot(x=city_ratings.values, y=city_ratings.index, palette="coolwarm")
plt.title("Top 20 Cities by Average Rating")
plt.xlabel("Average Rating")
plt.ylabel("City")
plt.tight_layout()
plt.savefig("average_rating_per_city.png")
plt.show()

# ===============================
# 6. Price Range Analysis
# ===============================
plt.figure(figsize=(8,5))
sns.countplot(x="Price range", data=df, palette="Set2")
plt.title("Distribution of Price Ranges")
plt.xlabel("Price Range")
plt.ylabel("Count")
plt.savefig("price_range_distribution.png")
plt.show()

# ===============================
# 7. Top Cuisines by City
# ===============================
def top_cuisines(city, n=10):
    city_data = df[df["City"] == city]
    cuisines_series = city_data["Cuisines"].dropna().str.split(",").explode().str.strip()
    return cuisines_series.value_counts().head(n)

example_city = df["City"].value_counts().idxmax()  # City with most restaurants
print(f"\n🍴 Top cuisines in {example_city}:\n", top_cuisines(example_city))

# ===============================
# 8. Insights
# ===============================
print("\n📊 Key Insights:")
print(f"- {df['City'].nunique()} cities are covered.")
print(f"- City with most restaurants: {df['City'].value_counts().idxmax()} ({df['City'].value_counts().max()} restaurants).")
print(f"- Average global restaurant rating: {df['Aggregate rating'].mean():.2f}")
print(f"- Most common price range: {df['Price range'].mode()[0]}")
