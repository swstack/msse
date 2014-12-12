DROP TABLE commit_commit_chain;
DROP TABLE tree_entry;
DROP TABLE commit_object;
DROP TABLE tree_object;
DROP TABLE blob_object;
DROP TABLE content_graph_node;
DROP TABLE git_object;

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
  constraint fk_sha
    foreign key (go_sha_hash)
    references git_object(sha_hash),
  constraint pk_co_sha primary key (go_sha_hash)
);

create table tree_object
(
  go_sha_hash varchar2(20),
  content_graph_id numeric(10),
  constraint fk_sha_tree
    foreign key (go_sha_hash)
    references git_object(sha_hash),
  constraint pk_to_sha primary key (go_sha_hash)
);

create table blob_object
(
  go_sha_hash varchar2(20),
  file_content varchar2(200),
  content_graph_id numeric(10),
  constraint fk_sha_blob
    foreign key (go_sha_hash)
    references git_object(sha_hash),
  constraint pk_bo_sha primary key (go_sha_hash)
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
    references commit_object(go_sha_hash),
  constraint pk_ccc primary key (parent_go_sha_hash, child_go_sha_hash)
);

create table content_graph_node
(
  content_graph_id number(10),
  constraint pk_cgn_id primary key (content_graph_id)
);

create table tree_entry
(
  child_id number(10),
  parent_id number(10),
  child_mode varchar2(10),
  constraint fk_child_id
    foreign key (child_id)
    references content_graph_node(content_graph_id),
  constraint fk_parent_id
    foreign key (parent_id)
    references content_graph_node(content_graph_id),
  constraint pk_parent_id primary key (parent_id, child_id)
);
