-- Add indexes to improve query performance
CREATE INDEX IF NOT EXISTS idx_kebab_places_city_id ON kebab_places(city_id);
CREATE INDEX IF NOT EXISTS idx_ratings_history_kebab_place_id ON ratings_history(kebab_place_id);
CREATE INDEX IF NOT EXISTS idx_ratings_history_data_fetched_at ON ratings_history(data_fetched_at);
CREATE INDEX IF NOT EXISTS idx_ratings_history_city_rank ON ratings_history(city_rank);
CREATE INDEX IF NOT EXISTS idx_cities_name ON cities(name);
