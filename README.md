# Narad 📒

## Description

Narad is a product importer service.

### Commands 📦

#### Docker

```make docker-compose-run```

Use this command to bootstrap all dependent services like Nginx, Webapp(Django)
and Postgresql. This command internally performs related `docker-compose`
commands.

#### Local Build

``` make build```

This command will install all Python dependencies. You are not re-quired to
perform this command if your goal is to make a build using Docker.

```make migrations```

This command will create a database migrations.

```make migrate```

This command will migrate pending migrations to local data base.
