-- Create function to get city rankings with latest ratings in one query
CREATE OR REPLACE FUNCTION get_city_rankings_with_latest_ratings_v3(
    p_city_id integer,
    p_limit integer,
    p_offset integer
)
RETURNS TABLE (
    id integer,
    name text,
    address text,
    google_place_id text,
    rating numeric,
    total_reviews integer,
    positive_percentage numeric,
    rank_score numeric,
    city_rank integer,
    data_fetched_at timestamp with time zone
) AS $$
BEGIN
    RETURN QUERY
    WITH latest_ratings AS (
        SELECT 
            kp.id,
            kp.name,
            kp.address,
            kp.google_place_id,
            rh.rating,
            rh.total_reviews,
            rh.positive_percentage,
            rh.rank_score,
            rh.city_rank,
            rh.data_fetched_at,
            ROW_NUMBER() OVER (PARTITION BY kp.id ORDER BY rh.data_fetched_at DESC) as rn
        FROM 
            kebab_places kp
        JOIN 
            ratings_history rh ON kp.id = rh.kebab_place_id
        WHERE 
            kp.city_id = p_city_id
    )
    SELECT 
        lr.id,
        lr.name,
        lr.address,
        lr.google_place_id,
        lr.rating,
        lr.total_reviews,
        lr.positive_percentage,
        lr.rank_score,
        lr.city_rank,
        lr.data_fetched_at
    FROM 
        latest_ratings lr
    WHERE 
        lr.rn = 1
    ORDER BY
        lr.rank_score DESC,
        lr.total_reviews DESC
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
