CREATE TABLE `country_summary` (
  `country` text,
  `total_titles` int DEFAULT NULL,
  `avg_imdb` double DEFAULT NULL,
  `top_platform` text,
  `top_genre` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `genre_summary` (
  `primary_genre` text,
  `total_titles` int DEFAULT NULL,
  `avg_imdb` double DEFAULT NULL,
  `avg_rt` double DEFAULT NULL,
  `total_hours_watched_million` int DEFAULT NULL,
  `avg_budget` text,
  `total_awards` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `platform_summary` (
  `platform` text,
  `total_titles` int DEFAULT NULL,
  `movies` int DEFAULT NULL,
  `tv_shows` int DEFAULT NULL,
  `avg_imdb` double DEFAULT NULL,
  `avg_rt` double DEFAULT NULL,
  `avg_votes` double DEFAULT NULL,
  `total_hours_watched_million` int DEFAULT NULL,
  `total_awards` int DEFAULT NULL,
  `top_genre` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `streaming_catalog` (
  `show_id` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `platform` varchar(255) DEFAULT NULL,
  `primary_genre` varchar(255) DEFAULT NULL,
  `genres` varchar(255) DEFAULT NULL,
  `director` varchar(255) DEFAULT NULL,
  `cast` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `language` varchar(255) DEFAULT NULL,
  `release_year` varchar(255) DEFAULT NULL,
  `date_added` date DEFAULT NULL,
  `rating` varchar(255) DEFAULT NULL,
  `duration` varchar(255) DEFAULT NULL,
  `duration_minutes` varchar(255) DEFAULT NULL,
  `num_seasons` varchar(255) DEFAULT NULL,
  `num_episodes` varchar(255) DEFAULT NULL,
  `imdb_rating` varchar(255) DEFAULT NULL,
  `rotten_tomatoes_score` varchar(255) DEFAULT NULL,
  `imdb_votes` varchar(255) DEFAULT NULL,
  `budget_million_usd` varchar(255) DEFAULT NULL,
  `production_company` varchar(255) DEFAULT NULL,
  `awards_won` varchar(255) DEFAULT NULL,
  `hours_watched_million` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `yearly_release_trends` (
  `release_year` int DEFAULT NULL,
  `total_titles` int DEFAULT NULL,
  `movies` int DEFAULT NULL,
  `tv_shows` int DEFAULT NULL,
  `avg_imdb` double DEFAULT NULL,
  `avg_budget` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
