CREATE TABLE responses(
  case_id INTEGER,
  user_id TEXT,
  response TEXT,
  FOREIGN KEY(case_id) REFERENCES cases(id)
);
CREATE UNIQUE INDEX response_index ON responses(case_id, user_id);
CREATE TABLE "cases"(
  `id`	INTEGER,
  `title`	TEXT,
  `body`	TEXT,
  `details`	TEXT,
  PRIMARY KEY(`id`)
);
