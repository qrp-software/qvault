# Teknopark PDKS API Dokümantasyonu

## Genel Bilgiler

Bu dokümantasyon, Teknopark PDKS (Personel Devam Kontrol Sistemi) API'sinin kullanımını açıklar. API, RESTful prensiplere uygun olarak tasarlanmıştır ve JWT (JSON Web Token) tabanlı kimlik doğrulama kullanır.

### Base URL

```
http://localhost:8000  (Development)
https://yourdomain.com  (Production)
```

### Kimlik Doğrulama

API, JWT Bearer token tabanlı kimlik doğrulama kullanır. Tüm isteklerde (login hariç) `Authorization` header'ında token gönderilmelidir.

**Format:**
```
Authorization: Bearer <access_token>
```

---

## 1. Kimlik Doğrulama Endpoint'leri

### 1.1. Giriş Yap (Login)

Kullanıcı girişi yaparak JWT token alınır.

**Endpoint:** `POST /users/api/login/`

**Kimlik Doğrulama:** Gerekli değil

**Request Body:**
```json
{
  "username": "kullanici_adi",
  "password": "sifre"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "kullanici_adi",
    "email": "user@example.com",
    "first_name": "Ad",
    "last_name": "Soyad"
  }
}
```

**Hata Durumları:**
- `400 Bad Request`: Kullanıcı adı veya şifre hatalı
- `400 Bad Request`: Kullanıcı hesabı aktif değil

**Örnek cURL:**
```bash
curl -X POST http://localhost:8000/users/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "kullanici_adi",
    "password": "sifre"
  }'
```

---

## 2. PDKS Log Endpoint'leri

### 2.1. Tüm Logları Listele

Kullanıcının tüm giriş/çıkış loglarını listeler.

**Endpoint:** `GET /teknopark/api/pdks/logs/`

**Kimlik Doğrulama:** Gerekli (Bearer Token)

**Query Parametreleri:**
- `log_type` (string, optional): Log tipi (`entry` veya `exit`)
- `date_from` (date, optional): Başlangıç tarihi (format: `YYYY-MM-DD`)
- `date_to` (date, optional): Bitiş tarihi (format: `YYYY-MM-DD`)
- `page` (integer, optional): Sayfa numarası (varsayılan: 1)
- `ordering` (string, optional): Sıralama (`-timestamp`, `timestamp`)

**Response (200 OK):**
```json
{
  "count": 100,
  "next": "http://localhost:8000/teknopark/api/pdks/logs/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 1,
        "username": "kullanici_adi",
        "email": "user@example.com",
        "first_name": "Ad",
        "last_name": "Soyad"
      },
      "log_type": "entry",
      "log_type_display": "Giriş",
      "timestamp": "2025-01-15 09:00:00",
      "created_date": "2025-01-15 09:00:00",
      "modified_date": "2025-01-15 09:00:00"
    }
  ]
}
```

**Örnek cURL:**
```bash
curl -X GET "http://localhost:8000/teknopark/api/pdks/logs/?log_type=entry&date_from=2025-01-01" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 2.2. Yeni Log Oluştur

Yeni bir giriş veya çıkış logu oluşturur.

**Endpoint:** `POST /teknopark/api/pdks/logs/`

**Kimlik Doğrulama:** Gerekli (Bearer Token)

**Request Body:**
```json
{
  "log_type": "entry",
  "timestamp": "2025-01-15T09:00:00Z"
}
```

**Parametreler:**
- `log_type` (string, required): Log tipi - `entry` (Giriş) veya `exit` (Çıkış)
- `timestamp` (datetime, optional): Log zamanı (ISO 8601 formatı). Belirtilmezse şu anki zaman kullanılır.

**Response (201 Created):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "kullanici_adi",
    "email": "user@example.com",
    "first_name": "Ad",
    "last_name": "Soyad"
  },
  "log_type": "entry",
  "log_type_display": "Giriş",
  "timestamp": "2025-01-15 09:00:00",
  "created_date": "2025-01-15 09:00:00",
  "modified_date": "2025-01-15 09:00:00"
}
```

**Örnek cURL:**
```bash
curl -X POST http://localhost:8000/teknopark/api/pdks/logs/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "log_type": "entry",
    "timestamp": "2025-01-15T09:00:00Z"
  }'
```

### 2.3. Bugünkü Logları Getir

Kullanıcının bugünkü tüm loglarını getirir.

**Endpoint:** `GET /teknopark/api/pdks/logs/today/`

**Kimlik Doğrulama:** Gerekli (Bearer Token)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "user": {
      "id": 1,
      "username": "kullanici_adi",
      "email": "user@example.com",
      "first_name": "Ad",
      "last_name": "Soyad"
    },
    "log_type": "entry",
    "log_type_display": "Giriş",
    "timestamp": "2025-01-15 09:00:00",
    "created_date": "2025-01-15 09:00:00",
    "modified_date": "2025-01-15 09:00:00"
  },
  {
    "id": 2,
    "user": {
      "id": 1,
      "username": "kullanici_adi",
      "email": "user@example.com",
      "first_name": "Ad",
      "last_name": "Soyad"
    },
    "log_type": "exit",
    "log_type_display": "Çıkış",
    "timestamp": "2025-01-15 18:00:00",
    "created_date": "2025-01-15 18:00:00",
    "modified_date": "2025-01-15 18:00:00"
  }
]
```

### 2.4. Tekil Log Getir

Belirli bir log kaydının detaylarını getirir.

**Endpoint:** `GET /teknopark/api/pdks/logs/{id}/`

**Kimlik Doğrulama:** Gerekli (Bearer Token)

**Response (200 OK):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "kullanici_adi",
    "email": "user@example.com",
    "first_name": "Ad",
    "last_name": "Soyad"
  },
  "log_type": "entry",
  "log_type_display": "Giriş",
  "timestamp": "2025-01-15 09:00:00",
  "created_date": "2025-01-15 09:00:00",
  "modified_date": "2025-01-15 09:00:00"
}
```

### 2.5. Log Güncelle

Mevcut bir log kaydını günceller.

**Endpoint:** `PUT /teknopark/api/pdks/logs/{id}/` veya `PATCH /teknopark/api/pdks/logs/{id}/`

**Kimlik Doğrulama:** Gerekli (Bearer Token)

**Request Body (PUT - tüm alanlar):**
```json
{
  "log_type": "exit",
  "timestamp": "2025-01-15T18:00:00Z"
}
```

**Request Body (PATCH - kısmi güncelleme):**
```json
{
  "timestamp": "2025-01-15T18:30:00Z"
}
```

### 2.6. Log Sil

Bir log kaydını siler.

**Endpoint:** `DELETE /teknopark/api/pdks/logs/{id}/`

**Kimlik Doğrulama:** Gerekli (Bearer Token)

**Response (204 No Content):** Başarılı silme işlemi

---

## 3. Günlük Yoklama Endpoint'leri

### 3.1. Tüm Günlük Yoklamaları Listele

Kullanıcının tüm günlük yoklama kayıtlarını listeler.

**Endpoint:** `GET /teknopark/api/pdks/daily/`

**Kimlik Doğrulama:** Gerekli (Bearer Token)

**Query Parametreleri:**
- `date_from` (date, optional): Başlangıç tarihi (format: `YYYY-MM-DD`)
- `date_to` (date, optional): Bitiş tarihi (format: `YYYY-MM-DD`)
- `page` (integer, optional): Sayfa numarası
- `ordering` (string, optional): Sıralama (`-date`, `date`)

**Response (200 OK):**
```json
{
  "count": 30,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 1,
        "username": "kullanici_adi",
        "email": "user@example.com",
        "first_name": "Ad",
        "last_name": "Soyad"
      },
      "date": "2025-01-15",
      "total_hours": "8.50",
      "entry_count": 2,
      "first_entry": "2025-01-15 09:00:00",
      "last_exit": "2025-01-15 18:00:00",
      "created_date": "2025-01-15 09:00:00",
      "modified_date": "2025-01-15 18:00:00"
    }
  ]
}
```

### 3.2. Bugünkü Yoklamayı Getir

Kullanıcının bugünkü yoklama kaydını getirir. Eğer bugün için kayıt yoksa otomatik olarak oluşturulur ve hesaplanır.

**Endpoint:** `GET /teknopark/api/pdks/daily/today/`

**Kimlik Doğrulama:** Gerekli (Bearer Token)

**Response (200 OK):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "kullanici_adi",
    "email": "user@example.com",
    "first_name": "Ad",
    "last_name": "Soyad"
  },
  "date": "2025-01-15",
  "total_hours": "8.50",
  "entry_count": 2,
  "first_entry": "2025-01-15 09:00:00",
  "last_exit": "2025-01-15 18:00:00",
  "created_date": "2025-01-15 09:00:00",
  "modified_date": "2025-01-15 18:00:00"
}
```

### 3.3. Yoklama Özeti

Kullanıcının tüm yoklama kayıtlarının özet istatistiklerini getirir.

**Endpoint:** `GET /teknopark/api/pdks/daily/summary/`

**Kimlik Doğrulama:** Gerekli (Bearer Token)

**Response (200 OK):**
```json
{
  "total_hours": 240.50,
  "total_days": 30,
  "average_hours_per_day": 8.02
}
```

### 3.4. Tekil Günlük Yoklama Getir

Belirli bir günlük yoklama kaydının detaylarını getirir.

**Endpoint:** `GET /teknopark/api/pdks/daily/{id}/`

**Kimlik Doğrulama:** Gerekli (Bearer Token)

**Response (200 OK):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "kullanici_adi",
    "email": "user@example.com",
    "first_name": "Ad",
    "last_name": "Soyad"
  },
  "date": "2025-01-15",
  "total_hours": "8.50",
  "entry_count": 2,
  "first_entry": "2025-01-15 09:00:00",
  "last_exit": "2025-01-15 18:00:00",
  "created_date": "2025-01-15 09:00:00",
  "modified_date": "2025-01-15 18:00:00"
}
```

---

## 4. Aylık Rapor Endpoint'leri

### 4.1. Tüm Aylık Raporları Listele

Kullanıcının tüm aylık raporlarını listeler.

**Endpoint:** `GET /teknopark/api/pdks/monthly/`

**Kimlik Doğrulama:** Gerekli (Bearer Token)

**Query Parametreleri:**
- `year` (integer, optional): Yıl (örn: `2025`)
- `month` (integer, optional): Ay (1-12 arası)
- `page` (integer, optional): Sayfa numarası
- `ordering` (string, optional): Sıralama (`-year`, `-month`)

**Response (200 OK):**
```json
{
  "count": 12,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 1,
        "username": "kullanici_adi",
        "email": "user@example.com",
        "first_name": "Ad",
        "last_name": "Soyad"
      },
      "year": 2025,
      "month": 1,
      "month_display": "Ocak",
      "total_hours": "176.00",
      "total_days": 22,
      "average_hours_per_day": "8.00",
      "last_calculated": "2025-01-31 23:59:59"
    }
  ]
}
```

### 4.2. Bu Ayın Raporunu Getir

Kullanıcının bu ayın raporunu getirir. Eğer bu ay için rapor yoksa otomatik olarak oluşturulur ve hesaplanır.

**Endpoint:** `GET /teknopark/api/pdks/monthly/current_month/`

**Kimlik Doğrulama:** Gerekli (Bearer Token)

**Response (200 OK):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "kullanici_adi",
    "email": "user@example.com",
    "first_name": "Ad",
    "last_name": "Soyad"
  },
  "year": 2025,
  "month": 1,
  "month_display": "Ocak",
  "total_hours": "176.00",
  "total_days": 22,
  "average_hours_per_day": "8.00",
  "last_calculated": "2025-01-31 23:59:59"
}
```

### 4.3. Tekil Aylık Rapor Getir

Belirli bir aylık raporun detaylarını getirir.

**Endpoint:** `GET /teknopark/api/pdks/monthly/{id}/`

**Kimlik Doğrulama:** Gerekli (Bearer Token)

**Response (200 OK):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "kullanici_adi",
    "email": "user@example.com",
    "first_name": "Ad",
    "last_name": "Soyad"
  },
  "year": 2025,
  "month": 1,
  "month_display": "Ocak",
  "total_hours": "176.00",
  "total_days": 22,
  "average_hours_per_day": "8.00",
  "last_calculated": "2025-01-31 23:59:59"
}
```

### 4.4. Aylık Raporu Yeniden Hesapla

Belirli bir aylık raporu yeniden hesaplar.

**Endpoint:** `POST /teknopark/api/pdks/monthly/{id}/recalculate/`

**Kimlik Doğrulama:** Gerekli (Bearer Token)

**Response (200 OK):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "kullanici_adi",
    "email": "user@example.com",
    "first_name": "Ad",
    "last_name": "Soyad"
  },
  "year": 2025,
  "month": 1,
  "month_display": "Ocak",
  "total_hours": "176.00",
  "total_days": 22,
  "average_hours_per_day": "8.00",
  "last_calculated": "2025-01-31 23:59:59"
}
```

---

## Hata Kodları

API, standart HTTP durum kodlarını kullanır:

- `200 OK`: İstek başarılı
- `201 Created`: Kayıt başarıyla oluşturuldu
- `204 No Content`: İstek başarılı, içerik yok (silme işlemleri)
- `400 Bad Request`: Geçersiz istek (validasyon hatası)
- `401 Unauthorized`: Kimlik doğrulama gerekli veya token geçersiz
- `403 Forbidden`: İşlem için yetki yok
- `404 Not Found`: Kayıt bulunamadı
- `500 Internal Server Error`: Sunucu hatası

**Hata Response Formatı:**
```json
{
  "detail": "Hata mesajı burada yer alır"
}
```

veya validasyon hataları için:
```json
{
  "field_name": [
    "Bu alan için hata mesajı"
  ]
}
```

---

## Örnek Kullanım Senaryoları

### Senaryo 1: Günlük Kullanım Akışı

1. **Giriş yap:**
```bash
POST /users/api/login/
```

2. **Giriş logu oluştur:**
```bash
POST /teknopark/api/pdks/logs/
{
  "log_type": "entry"
}
```

3. **Çıkış logu oluştur:**
```bash
POST /teknopark/api/pdks/logs/
{
  "log_type": "exit"
}
```

4. **Bugünkü yoklamayı kontrol et:**
```bash
GET /teknopark/api/pdks/daily/today/
```

### Senaryo 2: Aylık Rapor Görüntüleme

1. **Bu ayın raporunu getir:**
```bash
GET /teknopark/api/pdks/monthly/current_month/
```

2. **Belirli bir ayın raporunu getir:**
```bash
GET /teknopark/api/pdks/monthly/?year=2025&month=1
```

### Senaryo 3: Geçmiş Verileri Filtreleme

1. **Belirli tarih aralığındaki logları getir:**
```bash
GET /teknopark/api/pdks/logs/?date_from=2025-01-01&date_to=2025-01-31
```

2. **Belirli tarih aralığındaki günlük yoklamaları getir:**
```bash
GET /teknopark/api/pdks/daily/?date_from=2025-01-01&date_to=2025-01-31
```

---

## Notlar

1. **Zaman Dilimi:** Tüm tarih ve saat değerleri UTC formatında saklanır ve döndürülür. İstemci tarafında yerel saat dilimine dönüştürülmelidir.

2. **Sayfalama:** Listeleme endpoint'leri sayfalama kullanır. Varsayılan sayfa boyutu 20 kayıttır.

3. **Sıralama:** Varsayılan sıralama:
   - Loglar: En yeni önce (`-timestamp`)
   - Günlük yoklamalar: En yeni önce (`-date`)
   - Aylık raporlar: En yeni önce (`-year`, `-month`)

4. **Otomatik Hesaplama:** Günlük yoklamalar ve aylık raporlar, log kayıtlarına göre otomatik olarak hesaplanır.

5. **Güvenlik:** Tüm endpoint'ler (login hariç) JWT token gerektirir. Token'lar 1 gün geçerlidir. Süresi dolduğunda refresh token kullanılarak yeni token alınabilir.

---

## Destek

Sorularınız veya sorunlarınız için lütfen sistem yöneticisi ile iletişime geçin.

