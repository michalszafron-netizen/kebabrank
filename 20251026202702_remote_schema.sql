

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


COMMENT ON SCHEMA "public" IS 'standard public schema';



CREATE EXTENSION IF NOT EXISTS "pg_graphql" WITH SCHEMA "graphql";






CREATE EXTENSION IF NOT EXISTS "pg_stat_statements" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "pgcrypto" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "supabase_vault" WITH SCHEMA "vault";






CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA "extensions";






CREATE OR REPLACE FUNCTION "public"."create_index_if_not_exists"("table_name" "text", "column_name" "text", "index_name" "text") RETURNS "void"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_indexes 
        WHERE schemaname = 'public' 
        AND tablename = table_name 
        AND indexname = index_name
    ) THEN
        EXECUTE format('CREATE INDEX %I ON %I (%I)', index_name, table_name, column_name);
    END IF;
END;
$$;


ALTER FUNCTION "public"."create_index_if_not_exists"("table_name" "text", "column_name" "text", "index_name" "text") OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."get_city_rankings_with_latest_ratings"("p_city_id" integer, "p_limit" integer, "p_offset" integer) RETURNS TABLE("id" integer, "name" "text", "address" "text", "google_place_id" "text", "rating" numeric, "total_reviews" integer, "positive_percentage" numeric, "rank_score" numeric, "city_rank" integer, "data_fetched_at" timestamp with time zone)
    LANGUAGE "plpgsql"
    AS $$
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
        FROM kebab_places kp
        JOIN ratings_history rh ON kp.id = rh.kebab_place_id
        WHERE kp.city_id = p_city_id
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
    FROM latest_ratings lr
    WHERE lr.rn = 1
    ORDER BY lr.rank_score DESC, lr.total_reviews DESC
    LIMIT p_limit OFFSET p_offset;
END;
$$;


ALTER FUNCTION "public"."get_city_rankings_with_latest_ratings"("p_city_id" integer, "p_limit" integer, "p_offset" integer) OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."get_city_rankings_with_latest_ratings_v2"("p_city_id" integer, "p_limit" integer, "p_offset" integer) RETURNS TABLE("id" integer, "name" character varying, "address" character varying, "google_place_id" character varying, "rating" numeric, "total_reviews" integer, "positive_percentage" numeric, "rank_score" numeric, "city_rank" integer, "data_fetched_at" timestamp with time zone)
    LANGUAGE "plpgsql"
    AS $$
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
        FROM kebab_places kp
        JOIN ratings_history rh ON kp.id = rh.kebab_place_id
        WHERE kp.city_id = p_city_id
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
    FROM latest_ratings lr
    WHERE lr.rn = 1
    ORDER BY lr.rank_score DESC, lr.total_reviews DESC
    LIMIT p_limit OFFSET p_offset;
END;
$$;


ALTER FUNCTION "public"."get_city_rankings_with_latest_ratings_v2"("p_city_id" integer, "p_limit" integer, "p_offset" integer) OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."get_city_rankings_with_latest_ratings_v3"("p_city_id" integer, "p_limit" integer, "p_offset" integer) RETURNS TABLE("id" integer, "name" character varying, "address" "text", "google_place_id" "text", "rating" numeric, "total_reviews" integer, "positive_percentage" numeric, "rank_score" numeric, "city_rank" integer, "data_fetched_at" timestamp with time zone)
    LANGUAGE "plpgsql"
    AS $$
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
$$;


ALTER FUNCTION "public"."get_city_rankings_with_latest_ratings_v3"("p_city_id" integer, "p_limit" integer, "p_offset" integer) OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."get_city_rankings_with_latest_ratings_v4"("p_city_id" integer, "p_limit" integer, "p_offset" integer) RETURNS TABLE("id" integer, "name" character varying, "address" "text", "google_place_id" character varying, "rating" numeric, "total_reviews" integer, "positive_percentage" numeric, "rank_score" numeric, "city_rank" integer, "data_fetched_at" timestamp without time zone)
    LANGUAGE "plpgsql"
    AS $$
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
$$;


ALTER FUNCTION "public"."get_city_rankings_with_latest_ratings_v4"("p_city_id" integer, "p_limit" integer, "p_offset" integer) OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."get_previous_city_rankings"("p_city_id" integer, "p_target_date" timestamp with time zone) RETURNS TABLE("google_place_id" character varying, "city_rank" integer, "data_fetched_at" timestamp without time zone, "is_approximate" boolean)
    LANGUAGE "plpgsql"
    AS $$
BEGIN
    RETURN QUERY
    WITH ranked_history AS (
        SELECT 
            kp.google_place_id,
            rh.city_rank,
            rh.data_fetched_at,
            ROW_NUMBER() OVER (
                PARTITION BY kp.id 
                ORDER BY ABS(EXTRACT(EPOCH FROM (rh.data_fetched_at - p_target_date)))
            ) as proximity_rank
        FROM kebab_places kp
        JOIN ratings_history rh ON rh.kebab_place_id = kp.id
        WHERE kp.city_id = p_city_id
        AND rh.data_fetched_at <= p_target_date
    )
    SELECT 
        rh.google_place_id,
        rh.city_rank,
        rh.data_fetched_at,
        CASE 
            WHEN ABS(EXTRACT(EPOCH FROM (rh.data_fetched_at - p_target_date))) > 86400 
            THEN true 
            ELSE false 
        END as is_approximate
    FROM ranked_history rh
    WHERE rh.proximity_rank = 1;
END;
$$;


ALTER FUNCTION "public"."get_previous_city_rankings"("p_city_id" integer, "p_target_date" timestamp with time zone) OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."get_previous_rankings"("p_kebab_place_id" integer, "p_days_ago" integer DEFAULT 7) RETURNS TABLE("previous_rank" integer, "rank_change" integer, "data_fetched_at" timestamp without time zone)
    LANGUAGE "plpgsql"
    AS $$
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
$$;


ALTER FUNCTION "public"."get_previous_rankings"("p_kebab_place_id" integer, "p_days_ago" integer) OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."get_rank_change_indicator"("p_kebab_place_id" integer, "p_days_ago" integer DEFAULT 7) RETURNS "text"
    LANGUAGE "plpgsql"
    AS $$
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
$$;


ALTER FUNCTION "public"."get_rank_change_indicator"("p_kebab_place_id" integer, "p_days_ago" integer) OWNER TO "postgres";

SET default_tablespace = '';

SET default_table_access_method = "heap";


CREATE TABLE IF NOT EXISTS "public"."ai_analysis" (
    "id" integer NOT NULL,
    "kebab_place_id" integer,
    "analysis_type" character varying(50) NOT NULL,
    "analysis_data" "jsonb" NOT NULL,
    "ai_score" double precision DEFAULT 0,
    "ai_summary" "text",
    "confidence_score" double precision DEFAULT 0,
    "review_count" integer DEFAULT 0,
    "created_at" timestamp with time zone DEFAULT "now"(),
    "updated_at" timestamp with time zone DEFAULT "now"()
);


ALTER TABLE "public"."ai_analysis" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."ai_analysis_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "public"."ai_analysis_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."ai_analysis_id_seq" OWNED BY "public"."ai_analysis"."id";



CREATE TABLE IF NOT EXISTS "public"."cities" (
    "id" integer NOT NULL,
    "name" character varying(100) NOT NULL,
    "google_place_id" character varying(255),
    "created_at" timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE "public"."cities" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."kebab_places" (
    "id" integer NOT NULL,
    "google_place_id" character varying(255) NOT NULL,
    "name" character varying(255) NOT NULL,
    "address" "text",
    "city_id" integer,
    "latitude" numeric(10,8),
    "longitude" numeric(11,8),
    "created_at" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE "public"."kebab_places" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."ratings_history" (
    "id" integer NOT NULL,
    "kebab_place_id" integer,
    "rating" numeric(2,1),
    "total_reviews" integer,
    "positive_percentage" numeric(5,2),
    "rank_score" numeric(10,2),
    "city_rank" integer,
    "global_rank" integer,
    "data_fetched_at" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    "ai_score" double precision,
    "ai_confidence" double precision,
    "sentiment_score" double precision,
    "authenticity_score" double precision,
    "trend_momentum" double precision,
    "update_batch_timestamp" timestamp with time zone
);


ALTER TABLE "public"."ratings_history" OWNER TO "postgres";


CREATE OR REPLACE VIEW "public"."ai_rankings" AS
 SELECT "kp"."id",
    "kp"."name",
    "kp"."address",
    "kp"."google_place_id",
    "c"."name" AS "city_name",
    "rh"."rating",
    "rh"."total_reviews",
    "rh"."rank_score",
    "rh"."city_rank",
    COALESCE("rh"."ai_score", ("rh"."rank_score")::double precision) AS "combined_score",
    ("aa"."analysis_data" ->> 'sentiment_analysis'::"text") AS "sentiment_data",
    ("aa"."analysis_data" ->> 'trend_analysis'::"text") AS "trend_data",
    "aa"."ai_summary",
    "aa"."confidence_score" AS "ai_confidence",
    "aa"."updated_at" AS "ai_last_updated"
   FROM ((("public"."kebab_places" "kp"
     JOIN "public"."cities" "c" ON (("kp"."city_id" = "c"."id")))
     JOIN "public"."ratings_history" "rh" ON (("kp"."id" = "rh"."kebab_place_id")))
     LEFT JOIN "public"."ai_analysis" "aa" ON (("kp"."id" = "aa"."kebab_place_id")))
  WHERE ("rh"."data_fetched_at" = ( SELECT "max"("ratings_history"."data_fetched_at") AS "max"
           FROM "public"."ratings_history"
          WHERE ("ratings_history"."kebab_place_id" = "kp"."id")))
  ORDER BY COALESCE("rh"."ai_score", ("rh"."rank_score")::double precision) DESC;


ALTER VIEW "public"."ai_rankings" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."cached_reviews" (
    "id" integer NOT NULL,
    "kebab_place_id" integer,
    "google_place_id" character varying(255) NOT NULL,
    "author_name" character varying(255),
    "author_id" character varying(255),
    "rating" integer,
    "review_text" "text",
    "review_time" timestamp with time zone,
    "language" character varying(10),
    "is_suspicious" boolean DEFAULT false,
    "fetched_at" timestamp with time zone DEFAULT "now"(),
    CONSTRAINT "cached_reviews_rating_check" CHECK ((("rating" >= 1) AND ("rating" <= 5)))
);


ALTER TABLE "public"."cached_reviews" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."cached_reviews_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "public"."cached_reviews_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."cached_reviews_id_seq" OWNED BY "public"."cached_reviews"."id";



CREATE SEQUENCE IF NOT EXISTS "public"."cities_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "public"."cities_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."cities_id_seq" OWNED BY "public"."cities"."id";



CREATE SEQUENCE IF NOT EXISTS "public"."kebab_places_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "public"."kebab_places_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."kebab_places_id_seq" OWNED BY "public"."kebab_places"."id";



CREATE SEQUENCE IF NOT EXISTS "public"."ratings_history_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "public"."ratings_history_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."ratings_history_id_seq" OWNED BY "public"."ratings_history"."id";



ALTER TABLE ONLY "public"."ai_analysis" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."ai_analysis_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."cached_reviews" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."cached_reviews_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."cities" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."cities_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."kebab_places" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."kebab_places_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."ratings_history" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."ratings_history_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."ai_analysis"
    ADD CONSTRAINT "ai_analysis_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."cached_reviews"
    ADD CONSTRAINT "cached_reviews_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."cities"
    ADD CONSTRAINT "cities_name_key" UNIQUE ("name");



ALTER TABLE ONLY "public"."cities"
    ADD CONSTRAINT "cities_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."kebab_places"
    ADD CONSTRAINT "kebab_places_google_place_id_key" UNIQUE ("google_place_id");



ALTER TABLE ONLY "public"."kebab_places"
    ADD CONSTRAINT "kebab_places_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."ratings_history"
    ADD CONSTRAINT "ratings_history_pkey" PRIMARY KEY ("id");



CREATE INDEX "idx_ai_analysis_created" ON "public"."ai_analysis" USING "btree" ("created_at" DESC);



CREATE INDEX "idx_ai_analysis_place" ON "public"."ai_analysis" USING "btree" ("kebab_place_id");



CREATE INDEX "idx_cached_reviews_place" ON "public"."cached_reviews" USING "btree" ("kebab_place_id");



CREATE INDEX "idx_cached_reviews_time" ON "public"."cached_reviews" USING "btree" ("review_time" DESC);



CREATE INDEX "idx_kebab_places_city" ON "public"."kebab_places" USING "btree" ("city_id");



CREATE INDEX "idx_kebab_places_city_id" ON "public"."kebab_places" USING "btree" ("city_id");



CREATE INDEX "idx_kebab_places_google_place_id" ON "public"."kebab_places" USING "btree" ("google_place_id");



CREATE INDEX "idx_ratings_history_composite" ON "public"."ratings_history" USING "btree" ("kebab_place_id", "data_fetched_at" DESC);



CREATE INDEX "idx_ratings_history_data_fetched_at" ON "public"."ratings_history" USING "btree" ("data_fetched_at");



CREATE INDEX "idx_ratings_history_fetched" ON "public"."ratings_history" USING "btree" ("data_fetched_at");



CREATE INDEX "idx_ratings_history_kebab_place_id" ON "public"."ratings_history" USING "btree" ("kebab_place_id");



CREATE INDEX "idx_ratings_history_place" ON "public"."ratings_history" USING "btree" ("kebab_place_id");



ALTER TABLE ONLY "public"."ai_analysis"
    ADD CONSTRAINT "ai_analysis_kebab_place_id_fkey" FOREIGN KEY ("kebab_place_id") REFERENCES "public"."kebab_places"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."cached_reviews"
    ADD CONSTRAINT "cached_reviews_kebab_place_id_fkey" FOREIGN KEY ("kebab_place_id") REFERENCES "public"."kebab_places"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."kebab_places"
    ADD CONSTRAINT "kebab_places_city_id_fkey" FOREIGN KEY ("city_id") REFERENCES "public"."cities"("id");



ALTER TABLE ONLY "public"."ratings_history"
    ADD CONSTRAINT "ratings_history_kebab_place_id_fkey" FOREIGN KEY ("kebab_place_id") REFERENCES "public"."kebab_places"("id");





ALTER PUBLICATION "supabase_realtime" OWNER TO "postgres";


GRANT USAGE ON SCHEMA "public" TO "postgres";
GRANT USAGE ON SCHEMA "public" TO "anon";
GRANT USAGE ON SCHEMA "public" TO "authenticated";
GRANT USAGE ON SCHEMA "public" TO "service_role";

























































































































































GRANT ALL ON FUNCTION "public"."create_index_if_not_exists"("table_name" "text", "column_name" "text", "index_name" "text") TO "anon";
GRANT ALL ON FUNCTION "public"."create_index_if_not_exists"("table_name" "text", "column_name" "text", "index_name" "text") TO "authenticated";
GRANT ALL ON FUNCTION "public"."create_index_if_not_exists"("table_name" "text", "column_name" "text", "index_name" "text") TO "service_role";



GRANT ALL ON FUNCTION "public"."get_city_rankings_with_latest_ratings"("p_city_id" integer, "p_limit" integer, "p_offset" integer) TO "anon";
GRANT ALL ON FUNCTION "public"."get_city_rankings_with_latest_ratings"("p_city_id" integer, "p_limit" integer, "p_offset" integer) TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_city_rankings_with_latest_ratings"("p_city_id" integer, "p_limit" integer, "p_offset" integer) TO "service_role";



GRANT ALL ON FUNCTION "public"."get_city_rankings_with_latest_ratings_v2"("p_city_id" integer, "p_limit" integer, "p_offset" integer) TO "anon";
GRANT ALL ON FUNCTION "public"."get_city_rankings_with_latest_ratings_v2"("p_city_id" integer, "p_limit" integer, "p_offset" integer) TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_city_rankings_with_latest_ratings_v2"("p_city_id" integer, "p_limit" integer, "p_offset" integer) TO "service_role";



GRANT ALL ON FUNCTION "public"."get_city_rankings_with_latest_ratings_v3"("p_city_id" integer, "p_limit" integer, "p_offset" integer) TO "anon";
GRANT ALL ON FUNCTION "public"."get_city_rankings_with_latest_ratings_v3"("p_city_id" integer, "p_limit" integer, "p_offset" integer) TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_city_rankings_with_latest_ratings_v3"("p_city_id" integer, "p_limit" integer, "p_offset" integer) TO "service_role";



GRANT ALL ON FUNCTION "public"."get_city_rankings_with_latest_ratings_v4"("p_city_id" integer, "p_limit" integer, "p_offset" integer) TO "anon";
GRANT ALL ON FUNCTION "public"."get_city_rankings_with_latest_ratings_v4"("p_city_id" integer, "p_limit" integer, "p_offset" integer) TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_city_rankings_with_latest_ratings_v4"("p_city_id" integer, "p_limit" integer, "p_offset" integer) TO "service_role";



GRANT ALL ON FUNCTION "public"."get_previous_city_rankings"("p_city_id" integer, "p_target_date" timestamp with time zone) TO "anon";
GRANT ALL ON FUNCTION "public"."get_previous_city_rankings"("p_city_id" integer, "p_target_date" timestamp with time zone) TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_previous_city_rankings"("p_city_id" integer, "p_target_date" timestamp with time zone) TO "service_role";



GRANT ALL ON FUNCTION "public"."get_previous_rankings"("p_kebab_place_id" integer, "p_days_ago" integer) TO "anon";
GRANT ALL ON FUNCTION "public"."get_previous_rankings"("p_kebab_place_id" integer, "p_days_ago" integer) TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_previous_rankings"("p_kebab_place_id" integer, "p_days_ago" integer) TO "service_role";



GRANT ALL ON FUNCTION "public"."get_rank_change_indicator"("p_kebab_place_id" integer, "p_days_ago" integer) TO "anon";
GRANT ALL ON FUNCTION "public"."get_rank_change_indicator"("p_kebab_place_id" integer, "p_days_ago" integer) TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_rank_change_indicator"("p_kebab_place_id" integer, "p_days_ago" integer) TO "service_role";


















GRANT ALL ON TABLE "public"."ai_analysis" TO "anon";
GRANT ALL ON TABLE "public"."ai_analysis" TO "authenticated";
GRANT ALL ON TABLE "public"."ai_analysis" TO "service_role";



GRANT ALL ON SEQUENCE "public"."ai_analysis_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."ai_analysis_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."ai_analysis_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."cities" TO "anon";
GRANT ALL ON TABLE "public"."cities" TO "authenticated";
GRANT ALL ON TABLE "public"."cities" TO "service_role";



GRANT ALL ON TABLE "public"."kebab_places" TO "anon";
GRANT ALL ON TABLE "public"."kebab_places" TO "authenticated";
GRANT ALL ON TABLE "public"."kebab_places" TO "service_role";



GRANT ALL ON TABLE "public"."ratings_history" TO "anon";
GRANT ALL ON TABLE "public"."ratings_history" TO "authenticated";
GRANT ALL ON TABLE "public"."ratings_history" TO "service_role";



GRANT ALL ON TABLE "public"."ai_rankings" TO "anon";
GRANT ALL ON TABLE "public"."ai_rankings" TO "authenticated";
GRANT ALL ON TABLE "public"."ai_rankings" TO "service_role";



GRANT ALL ON TABLE "public"."cached_reviews" TO "anon";
GRANT ALL ON TABLE "public"."cached_reviews" TO "authenticated";
GRANT ALL ON TABLE "public"."cached_reviews" TO "service_role";



GRANT ALL ON SEQUENCE "public"."cached_reviews_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."cached_reviews_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."cached_reviews_id_seq" TO "service_role";



GRANT ALL ON SEQUENCE "public"."cities_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."cities_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."cities_id_seq" TO "service_role";



GRANT ALL ON SEQUENCE "public"."kebab_places_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."kebab_places_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."kebab_places_id_seq" TO "service_role";



GRANT ALL ON SEQUENCE "public"."ratings_history_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."ratings_history_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."ratings_history_id_seq" TO "service_role";









ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "service_role";






























RESET ALL;

