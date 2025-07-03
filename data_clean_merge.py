import pandas as pd

# Load the datasets
tmdb_credits = pd.read_csv('tmdb_5000_credits.csv')
imdb_data = pd.read_csv('Comprehensive IMDb Data.csv')

# Step 1: Clean IMDb dataset
# Keep essential columns and drop duplicates
imdb_clean = imdb_data[['title', 'year', 'genre', 'score', 'budget', 'gross', 'runtime', 'company']].copy()
imdb_clean = imdb_clean.drop_duplicates(subset=['title', 'year'])

# Convert budget and gross to numeric and remove rows with missing or zero values
imdb_clean['budget'] = pd.to_numeric(imdb_clean['budget'], errors='coerce')
imdb_clean['gross'] = pd.to_numeric(imdb_clean['gross'], errors='coerce')
imdb_clean = imdb_clean[(imdb_clean['budget'] > 0) & (imdb_clean['gross'] > 0)]

# Step 2: Prepare TMDB dataset for merging
tmdb_credits_clean = tmdb_credits[['title', 'cast', 'crew']].copy()
tmdb_credits_clean['title'] = tmdb_credits_clean['title'].str.strip()

# Step 3: Normalize titles for merging
imdb_clean['title_lower'] = imdb_clean['title'].str.lower().str.strip()
tmdb_credits_clean['title_lower'] = tmdb_credits_clean['title'].str.lower().str.strip()

# Step 4: Merge datasets on cleaned lowercase titles
merged_df = pd.merge(imdb_clean, tmdb_credits_clean, on='title_lower', how='inner')

# Final cleaning: remove redundant title column and rename
merged_df = merged_df.drop(columns=['title_y'])
merged_df = merged_df.rename(columns={'title_x': 'title'})

# Preview the result
print("Merged dataset shape:", merged_df.shape)
print(merged_df[['title', 'year', 'genre', 'score', 'budget', 'gross']].head())
merged_df.to_csv('merged_movie_dataset.csv', index=False)