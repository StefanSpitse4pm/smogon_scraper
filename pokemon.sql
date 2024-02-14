SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


CREATE TABLE `pokemon` (
  `id` int NOT NULL,
  `pokemon_name` varchar(30) DEFAULT NULL,
  `pokemon_set` text,
  `format` varchar(100) DEFAULT NULL,
  `gen` varchar(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `pokemon`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `pokemon`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;
COMMIT;
