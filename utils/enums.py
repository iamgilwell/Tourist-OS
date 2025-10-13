from django.db import models


class UserType(models.TextChoices):
    TOURIST = "tourist", "Tourist"
    OPERATOR = "operator", "Service Operator"
    DMO = "dmo", "Destination Manager"
    ADMIN = "admin", "System Admin"


class ServiceType(models.TextChoices):
    TOUR = "tour", "Guided Tour"
    ACTIVITY = "activity", "Activity"
    TRANSPORT = "transport", "Transport"
    ACCOMMODATION = "accommodation", "Accommodation"
    DINING = "dining", "Dining"


class BookingStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    CANCELLED = "cancelled", "Cancelled"
    COMPLETED = "completed", "Completed"


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"


class PaymentMethod(models.TextChoices):
    CREDIT_CARD = "credit_card", "Credit Card"
    DEBIT_CARD = "debit_card", "Debit Card"
    PAYPAL = "paypal", "PayPal"
    STRIPE = "stripe", "Stripe"
    CASH = "cash", "Cash"
    BANK_TRANSFER = "bank_transfer", "Bank Transfer"


class Rating(models.IntegerChoices):
    POOR = 1, "1 - Poor"
    FAIR = 2, "2 - Fair"
    GOOD = 3, "3 - Good"
    VERY_GOOD = 4, "4 - Very Good"
    EXCELLENT = 5, "5 - Excellent"


class PromotionType(models.TextChoices):
    FEATURED = "featured", "Featured Listing"
    BANNER = "banner", "Banner Ad"
    PUSH = "push", "Push Notification"
    PACKAGE = "package", "Package Promotion"
    EMAIL = "email", "Email Campaign"


class MetricType(models.TextChoices):
    BOOKINGS = "bookings", "Total Bookings"
    REVENUE = "revenue", "Total Revenue"
    USERS = "users", "New Users"
    PAGE_VIEWS = "page_views", "Page Views"
    CONVERSION_RATE = "conversion_rate", "Conversion Rate"


class Currency(models.TextChoices):
    USD = "USD", "US Dollar"
    EUR = "EUR", "Euro"
    GBP = "GBP", "British Pound"
    KES = "KES", "Kenyan Shilling"
    TZS = "TZS", "Tanzanian Shilling"
    ZAR = "ZAR", "South African Rand"


class SubscriptionPlan(models.TextChoices):
    FREE = "free", "Free Plan"
    BASIC = "basic", "Basic Plan"
    PROFESSIONAL = "professional", "Professional Plan"
    ENTERPRISE = "enterprise", "Enterprise Plan"


class SubscriptionStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    EXPIRED = "expired", "Expired"
    CANCELLED = "cancelled", "Cancelled"
    SUSPENDED = "suspended", "Suspended"
