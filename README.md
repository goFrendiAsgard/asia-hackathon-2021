# What is this

Demo for Asia hackathon. Emphasizing dependency injection

# How to

## Run the program

```sh
zaruba please start
```

## Create .env

```sh
zaruba please syncEnv
```

## Use Mysql instead of sqlite

Edit `.env`

```sh
# ASIA_APP_APP_SQLALCHEMY_DATABASE_URL="sqlite:///database.db"
ASIA_APP_APP_SQLALCHEMY_DATABASE_URL="mysql+pymysql://root:toor@localhost:3306/asia"
```

## Use Redis

Edit `.env`

```sh
ASIA_APP_APP_REDIS_URL="redis://root:toor@localhost:6379"
ASIA_APP_APP_BOOK_STORAGE_ENGINE=redis
```