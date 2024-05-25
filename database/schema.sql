CREATE TABLE IF NOT EXISTS `ww_config` (
  `user_id` varchar(20) NOT NULL,
  `card_pool_id` varchar(40) NOT NULL,
  `player_id` varchar(20) NOT NULL,
  `record_id` varchar(40) NOT NULL,
  `server_id` varchar(40) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);