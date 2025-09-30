# financial-toolkit
A tool for myself to use for my personal financial needs.

To run:
`docker-compose up -d`

To stop
`docker-compose down`

To rebuild
`docker-compose up -d --build`

Ensure you have Docker installed.


To access postgresql DB
1. Launch the DB with `docker-compose up postgres`
2. `docker-compose exec postgres bash`
3. `psql -U username -d db_name`
4. `\dt` to see tables