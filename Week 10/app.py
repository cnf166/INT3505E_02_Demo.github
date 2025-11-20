from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pybreaker import CircuitBreaker
import logging
import redis
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


# Rate limiting 
redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=os.getenv("REDIS_URL", "memory://")
)

# Circuit Breaker (bảo vệ khi backend chậm hoặc lỗi)
breaker = CircuitBreaker(fail_max=5, reset_timeout=60)


# Prometheus metrics
metrics = PrometheusMetrics(app)
metrics.info("app_info", "Flask Security & Monitoring Demo", version="1.0.0")

# Custom metrics
counter = metrics.counter(
    'api_requests_total', 'Total API requests', labels={'endpoint': lambda: request.path}
)

# Logging có cấu trúc + audit log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)
audit_logger = logging.getLogger('audit')
audit_handler = logging.FileHandler('audit.log')
audit_logger.addHandler(audit_handler)

# Routes
@app.before_request
def before_request():
    counter.inc()

@app.route('/')
@limiter.limit("100 per minute")  # Rate limiting
def health():
    audit_logger.info(f"ACCESS HEALTH {request.remote_addr} {request.user_agent}")
    return jsonify({"status": "ok", "message": "Flask Production Demo Running!"})

@app.route('/heavy')
@limiter.limit("10/minute")
@breaker
def heavy_endpoint():
    # Giả lập gọi service bên ngoài có thể fail
    import time, random
    if random.random() < 0.3:  # 30% chance fail
        audit_logger.warning(f"HEAVY ENDPOINT FAILED {request.remote_addr}")
        raise Exception("External service down")
    time.sleep(2)
    return jsonify({"result": "heavy computation done"})

@app.route('/metrics')
def metrics_endpoint():
    # Prometheus sẽ tự expose ở đây
    return metrics()

# Error Handlers
@app.errorhandler(429)
def ratelimit_handler(e):
    audit_logger.warning(f"RATE LIMIT {request.remote_addr}")
    return jsonify(error="Rate limit exceeded", limit=e.description), 429

@breaker.on_circuit_open
def on_open():
    app.logger.warning("Circuit breaker OPENED")

@breaker.on_circuit_close
def on_close():
    app.logger.info("Circuit breaker CLOSED again")

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)