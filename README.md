# Django-DDD

Apply Domain-driven Design to Django without Django Rest Framework. 
This could be an overkill for using Django, but it's going to be an interesting experiment.

## Requirements
- django
- django-ninja

## Points to Note
- Most project hierarchies are similar to [python-ddd project](https://github.com/qu3vipon/python-ddd).
- The whole project is not dependent on the database using the imperative mapping and repository pattern.
  - [Imperative Mapping](src/shared/infra/repository/mapper.py)
  - [Repository Pattern](src/todo/infra/database/repository/rdb.py)
- The built-in features(Admin, ORM, etc.) of Django can be used as they are.

### Project Structure
```
src
├── shared
│   ├── domain
│   └── infra
│       ├── django
│       └── repository
│           ├── mapper
│           └── rdb
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
│   │       └── repository
│   │           ├── mapper
│   │           └── rdb
│   └── presentation
│       └── rest
│            ├── api
│            ├── containers
│            ├── request
│            └── response
├── user
└── tests
```

## Opinion
DRF has the advantage of being able to create the web applications quickly, but it is inherently too dependent on the database. I want to take advantage of Django's built-in features like Admin, ORM, etc. But I have sometimes suffered from DRF because of its inflexible design.

I found Django-Ninja instead, and it has everything I need.

But I still think DRF is a very good framework, and I highly value DRF's contribution to the Python web community.
