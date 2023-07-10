insert into users(user_id, name, chosen_album_id)
values
(1, 'user_1', 3),
(2, 'user_2', 1),
(3, 'user_3', NULL),
(4, 'user_4', NULL),
(5, 'user_5', NULL);

insert into albums
values
(1, 'album_1', 'description_1', 'index_1.pkl', 'mapping_1.pkl'),
(2, 'album_2', 'description_2', 'index_2.pkl', 'mapping_2.pkl'),
(3, 'album_3', 'description_3', 'index_3.pkl', 'mapping_3.pkl'),
(4, 'album_4', 'description_4', 'index_4.pkl', 'mapping_4.pkl');

insert into album_permissions
values
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(2, 1),
(2, 2),
(2, 3),
(3, 2),
(3, 4);