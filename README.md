# Django-DDD

Apply Domain-driven Design to Django without Django Rest Framework. 
This could be an overkill for using Django, but it's going to be an interesting experiment.

Most project hierarchies are similar to [python-ddd project](https://github.com/qu3vipon/python-ddd).

## Points to Note
- The whole project is not dependent on the database using the imperative mapping and repository pattern.
  - [Imperative Mapping](src/shared/infra/repository/mapper.py)
  - [Repository Pattern](src/shared/infra/repository/rdb.py)
- The built-in features(Admin, ORM, etc.) of Django can be used as they are.
- Without using DRF, routing was implemented manually and Pydantic is used for serialization & deserialization. 

## Project Structure
```
src
├── todo
│   ├── application
│   │   └── use_case
│   │       ├── query
│   │       └── command
│   ├── domain
│   │   ├── entity
│   │   └── exception
│   ├── infra
│   │   └── database
│   │       ├── migrations
│   │       ├── models
│   │       └── database
│   │           └── repository
│   │              ├── mapper
│   │              └── rdb
│   └── presentation
│       └── rest
│            ├── request
│            ├── response
│            ├── urls
│            └── views
├── user
├── tests
└── shared
    ├── domain
    └── infra
        ├── django
        └── repository
            ├── mapper
            └── rdb
```


## Opinion
DRF has the advantage of being able to create the web applications quickly, but it is inherently too dependent on the database. I want to take advantage of Django's built-in Admin and ORM, but I have sometimes suffered from DRF because of its inflexible design.

I'm planning to create a new framework on top of Django to replace DRF someday.
This repo is a proof of concept project before that.

But I still think DRF is a very good framework, and I highly value DRF's contribution to the Python web community.
