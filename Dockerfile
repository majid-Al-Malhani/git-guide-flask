# * إصدار Python مطابق لما يحدده runtime.txt
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# * تثبيت المكتبات أولًا للاستفادة من التخزين المؤقت للطبقات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# * أمر التشغيل نفسه المستخدم على Render
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} app:app"]
