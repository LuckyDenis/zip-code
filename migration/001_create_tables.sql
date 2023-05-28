CREATE TABLE "user" (
  "chat_id" bigint PRIMARY KEY,
  "language" varchar
);

CREATE TABLE "language" (
  "code" varchar PRIMARY KEY NOT NULL
);

ALTER TABLE "user" ADD FOREIGN KEY ("language") REFERENCES "language" ("code");

