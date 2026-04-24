# WanderLust — Travel Platform

A full-featured travel booking platform built with Django REST Framework, PostgreSQL, Redis, and Docker.

## Features

- **Destinations** — Browse world destinations filtered by continent, country, and features
- **Tours** — Detailed tour packages with categories, difficulty levels, and availability dates
- **Bookings** — Authenticated booking system with spot management and cancellation
- **Reviews** — Verified user reviews with star ratings and automatic tour rating updates
- **JWT Auth** — Secure authentication with token refresh and blacklisting
- **API Docs** — Interactive Swagger UI at `/api/docs/`
- **Redis Caching** — Destination listings cached for performance
- **Admin Panel** — Full Django admin at `/admin/`

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2 + Django REST Framework |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| Auth | JWT (simplejwt) |
| Reverse Proxy | Nginx |
| Container | Docker + Docker Compose |

## Quick Start

```bash
# 1. Clone the repo
git clone <repo-url>
cd vibe

# 2. Create environment file
cp .env.example .env

# 3. Start all services
docker compose up --build

# 4. Visit the API docs
open http://localhost/api/docs/

# 5. Login to admin panel
open http://localhost/admin/
# Email: admin@travel.com  Password: admin123
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Create account |
| POST | `/api/auth/login/` | Get JWT tokens |
| POST | `/api/auth/logout/` | Blacklist refresh token |
| POST | `/api/auth/token/refresh/` | Refresh access token |
| GET/PATCH | `/api/auth/profile/` | View/update profile |

### Destinations
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/destinations/` | List all (filterable) |
| GET | `/api/destinations/{id}/` | Destination detail |
| GET | `/api/destinations/featured/` | Featured destinations |
| GET | `/api/destinations/continents/` | Continent choices |

### Tours
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tours/` | List tours (search, filter) |
| GET | `/api/tours/{id}/` | Tour detail with dates |
| GET | `/api/tours/featured/` | Featured tours |
| GET | `/api/tours/{id}/dates/` | Available dates |
| GET | `/api/tours/categories/` | Tour category choices |

### Bookings (Auth required)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/bookings/` | My bookings |
| POST | `/api/bookings/` | Create booking |
| POST | `/api/bookings/{id}/cancel/` | Cancel booking |

### Reviews
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/reviews/` | List reviews (filterable by tour) |
| POST | `/api/reviews/` | Submit review (auth required) |
| PATCH | `/api/reviews/{id}/` | Edit own review |

## Filtering & Search

```bash
# Filter tours by destination and category
GET /api/tours/?destination=1&category=adventure

# Search destinations
GET /api/destinations/?search=bali

# Filter reviews by tour and rating
GET /api/reviews/?tour=1&rating=5

# Order tours by price
GET /api/tours/?ordering=price_per_person
```

## Architecture

```
nginx (port 80)
    └── backend (Django/Gunicorn, port 8000)
            ├── PostgreSQL (db)
            └── Redis (cache)
```

## Development

```bash
# View logs
docker compose logs -f backend

# Run Django shell
docker compose exec backend python manage.py shell

# Create migrations after model changes
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate

# Run tests
docker compose exec backend python manage.py test
```

## Seed Data

On first startup the app automatically:
1. Runs all migrations
2. Creates the admin superuser
3. Loads 6 destinations (Bali, Santorini, Machu Picchu, Tokyo, Serengeti, NYC)
4. Loads 6 tours with available dates
