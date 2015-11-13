-- not supported:
--  * link to other formats
--  * link to other languages 
--  * <author> (hardcoded)
--  * <updated>: I will use newest from service_feed_entry

CREATE TABLE service_feed 
(
  pkuid integer NOT NULL,
  title varchar NOT NULL,
  subtitle varchar, 
  self_link varchar NOT NULL, -- not used at the moment (hardcoded)
  describedby_link varchar NOT NULL,
  search_link varchar NOT NULL, -- not used at the moment (hardcoded)
  rights varchar,
  PRIMARY KEY ("pkuid")  
);

CREATE TABLE service_feed_entry
(
  pkuid integer NOT NULL,
  sf_id integer NOT NULL,
  identifier_code varchar NOT NULL,  
  identifier_namespace varchar,
  title varchar NOT NULL,
  subtitle varchar, 
  summary varchar,
  describedby_link varchar,
  rights varchar,
  updated datetime, 
  x_min float,
  y_min float,
  x_max float,
  y_max float, 
  PRIMARY KEY ("pkuid")
);

-- not supported:
--  * link to other languages
--  * <author> (hardcoded)
--  * <updated>: I will use newest from dataset_feed_entry
-- describedby 1-n relation

CREATE TABLE dataset_feed
(
  pkuid integer NOT NULL,
  sfe_id integer NOT NULL,
  title varchar NOT NULL,
  subtitle varchar, 
  rights varchar,
  PRIMARY KEY ("pkuid")  
);

CREATE TABLE dataset_feed_models 
(
  pkuid integer NOT NULL,
  df_id varchar NOT NULL,
  describedby_link varchar NOT NULL,
  PRIMARY KEY ("pkuid")  
);

CREATE TABLE dataset_feed_entry
(
  pkuid integer NOT NULL,
  df_id varchar NOT NULL,
  title varchar, -- do not use, instead use: dataset_feed.title + " " + srs_auth + ":" srs_code + "("+ format_txt + ")"  
  alternate_link varchar NOT NULL,
  summary varchar, 
  format_mime varchar NOT NULL,
  format_txt varchar NOT NULL,
  srs_auth integer NOT NULL,
  srs_code varchar NOT NULL,
  srs_txt varchar,
  updated datetime NOT NULL,  
  PRIMARY KEY ("pkuid")
);

