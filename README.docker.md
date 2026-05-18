# Docker Kurulum ve Kullanım Kılavuzu

Bu proje Docker ve Docker Compose ile çalıştırılabilir.

## Gereksinimler

- Docker
- Docker Compose

## Hızlı Başlangıç

### 1. Environment Dosyası Oluşturma

`.env` dosyası oluşturun ve gerekli environment değişkenlerini ayarlayın:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=qvault
DB_USER=qvault_user
DB_PASSWORD=qvault_password
DB_HOST=db
DB_PORT=5432
TIME_ZONE=Europe/Istanbul
```

### 2. Production Modunda Çalıştırma

```bash
# Docker image'ı build et
docker-compose build

# Servisleri başlat
docker-compose up -d

# Logları görüntüle
docker-compose logs -f

# Servisleri durdur
docker-compose down
```

### 3. Development Modunda Çalıştırma

```bash
# Development compose dosyası ile çalıştır
docker-compose -f docker-compose.dev.yml up -d

# Logları görüntüle
docker-compose -f docker-compose.dev.yml logs -f
```

## Yönetim Komutları

### Migration Çalıştırma

```bash
docker-compose exec web python manage.py migrate
```

### Superuser Oluşturma

```bash
docker-compose exec web python manage.py createsuperuser
```

### Django Shell

```bash
docker-compose exec web python manage.py shell
```

### Static Dosyaları Toplama

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Veritabanı Yedekleme

```bash
docker-compose exec db pg_dump -U qvault_user qvault > backup.sql
```

### Veritabanı Geri Yükleme

```bash
docker-compose exec -T db psql -U qvault_user qvault < backup.sql
```

## Volume'ler

- `postgres_data`: PostgreSQL veritabanı verileri
- `static_volume`: Static dosyalar
- `media_volume`: Media dosyalar (yüklenen dosyalar)

## Portlar

- Web uygulaması: `8000` (varsayılan)
- PostgreSQL: `5432` (varsayılan)

Portları değiştirmek için `.env` dosyasında `PORT` ve `DB_PORT` değişkenlerini ayarlayın.

## Sorun Giderme

### Veritabanı Bağlantı Hatası

Veritabanının hazır olmasını bekleyin. `docker-entrypoint.sh` scripti otomatik olarak veritabanının hazır olmasını bekler.

### Static Dosyalar Görünmüyor

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Permission Hataları

```bash
docker-compose exec web chmod -R 755 /app/public/static
docker-compose exec web chmod -R 755 /app/public/media
```

## Production Deployment

Production için:

1. `.env` dosyasında `DEBUG=False` ayarlayın
2. Güçlü bir `SECRET_KEY` kullanın
3. `ALLOWED_HOSTS` değişkenini domain adresinizle güncelleyin
4. SSL sertifikası için reverse proxy (nginx) kullanın
5. `docker-compose.yml` dosyasını kullanın (gunicorn ile)

