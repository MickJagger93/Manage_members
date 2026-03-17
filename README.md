## Aplicación web de gestión de miembros / suscriptores construida con Flask que incluye:

## Autenticación y autorización

-Registro, login y logout (Flask‑Login)
-Recuperación / cambio de contraseña
-Protección CSRF en formularios (Flask‑WTF)
-Modelo de datos

-Member: usuario con email y hash de contraseña
-Profile: datos personales (nombre, apellido, email, teléfono, dirección) vinculados a un miembro
-PlanDetails: planes de suscripción (nombre, precio, descripción, duración)
-Payments: historial de pagos (plan, monto, fecha, estado, método, expiración)
-Gestión de suscripciones y pagos

-Selección de planes y registro de pagos
-Uso de métodos de pago simulados: tarjeta (formulario de CC) y transferencia bancaria (subida de comprobante)
-Historial de pagos, estado y duración/expiración del servicio

## Tecnologias utilizadas

-Backend: Python 3.11, Flask 3.1.3
-Base de Datos: SQLAlchemy 2.0.48 con Flask-Migrate para migraciones
-Autenticación: Flask-Login 0.6.3
-Formularios: Flask-WTF 1.2.2 con WTForms 3.2.1
-Frontend: HTML, CSS (estilos personalizados), JavaScript
-Otros: Jinja2 para templates, Werkzeug para utilidades web
