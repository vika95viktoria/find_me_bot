create table users(
   user_id bigint,
   name text,
   chosen_album_id bigint
);


create table albums(
  album_id bigint,
  full_name text,
  folder_name text,
  index_file_name text,
  mapping_file_name text
);


create table album_permissions(
  user_id  bigint,
  album_id bigint
);
