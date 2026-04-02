-- Create function to get previous rankings and calculate rank changes
CREATE OR REPLACE FUNCTION get_previous_rankings(
    p_kebab_place_id integer,
    p_days_ago integer DEFAULT 7
)
RETURNS TABLE (
    previous_rank integer,
    rank_change integer,
    data_fetched_at timestamp without time zone
) AS $$
BEGIN
    RETURN QUERY
    WITH current_rank AS (
        SELECT rh.city_rank
        FROM ratings_history rh
        WHERE rh.kebab_place_id = p_kebab_place_id
        ORDER BY rh.data_fetched_at DESC
        LIMIT 1
    ),
    previous_rank AS (
        SELECT 
            rh.city_rank,
            rh.data_fetched_at,
            (SELECT city_rank FROM current_rank) - rh.city_rank AS change
        FROM ratings_history rh
        WHERE rh.kebab_place_id = p_kebab_place_id
        AND rh.data_fetched_at <= (NOW() - (p_days_ago || ' days')::interval)
        ORDER BY rh.data_fetched_at DESC
        LIMIT 1
    )
    SELECT 
        pr.city_rank as previous_rank,
        pr.change as rank_change,
        pr.data_fetched_at
    FROM previous_rank pr;
END;
$$ LANGUAGE plpgsql;

-- Create function to get rank change indicators
CREATE OR REPLACE FUNCTION get_rank_change_indicator(
    p_kebab_place_id integer,
    p_days_ago integer DEFAULT 7
)
RETURNS text AS $$
DECLARE
    v_change integer;
    v_previous_exists boolean;
BEGIN
    SELECT (rank_change IS NOT NULL) INTO v_previous_exists
    FROM get_previous_rankings(p_kebab_place_id, p_days_ago);
    
    IF NOT v_previous_exists THEN
        RETURN 'new';
    END IF;
    
    SELECT rank_change INTO v_change
    FROM get_previous_rankings(p_kebab_place_id, p_days_ago);
    
    RETURN CASE 
        WHEN v_change > 2 THEN 'up'
        WHEN v_change < -2 THEN 'down' 
        ELSE 'neutral'
    END;
END;
$$ LANGUAGE plpgsql;
