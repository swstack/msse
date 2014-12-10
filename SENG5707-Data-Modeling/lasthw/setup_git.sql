DROP TABLE git_object;
DROP TABLE commit_object;
DROP TABLE tree_object;
DROP TABLE blob_object;
DROP TABLE commit_commit_chain;
DROP TABLE content_graph_node;
DROP TABLE author;

create table git_object
(
  sha_hash varchar2(20),
  constraint
    pk_sha primary key (sha_hash)
);

create table commit_object
(
  go_sha_hash varchar2(20),
  commit_message varchar(200),
  tree_object_sha_hash varchar2(20),
  ccc_parent_sha varchar2(20),
  ccc_child_sha varchar2(20),
  constraint fk_sha
    foreign key (go_sha_hash)
    references git_object(sha_hash)
);

create table tree_object
(
  go_sha_hash varchar2(20),
  content_graph_id numeric(10),
  constraint fk_sha_tree
    foreign key (go_sha_hash)
    references git_object(sha_hash)
);

create table blob_object
(
  go_sha_hash varchar2(20),
  file_content varchar(200),
  content_graph_id numeric(10),
  constraint fk_sha_blob
    foreign key (go_sha_hash)
    references git_object(sha_hash)
);

create table commit_commit_chain
(
  parent_go_sha_hash varchar2(20),
  child_go_sha_hash varchar2(20),
  constraint fk_parent_sha
    foreign key (parent_go_sha_hash)
    references commit_object(go_sha_hash),
  constraint fk_child_sha
    foreign key (child_go_sha_hash)
    references commit_object(go_sha_hash)
);
