# Use Python 2.7 as Django < 1.5 requires Python 2
FROM python:2.7-slim-buster

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Build essentials for Python packages
    build-essential \
    gcc \
    g++ \
    # PostgreSQL client and development files for psycopg2
    postgresql-client \
    libpq-dev \
    # XML processing libraries for lxml
    libxml2-dev \
    libxslt1-dev \
    # Image processing for Pillow
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libtiff5-dev \
    libwebp-dev \
    # Git for installing from repositories
    git \
    # YUI compressor dependencies
    default-jre \
    # ZeroMQ for zerorpc
    libzmq3-dev \
    # Cython compilation
    python-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

# Install pip and setuptools compatible with Python 2.7
RUN pip install --upgrade "pip<21.0" "setuptools<45"

# Create requirements file
COPY requirements.txt /app/

# Pre-install Cython as some packages need it during compilation
RUN pip install Cython==0.29.24

# Install Python dependencies
# Note: Installing in specific order to handle dependencies
RUN pip install numpy==1.16.6 && \
    pip install Django==1.4.22 && \
    pip install South==1.0.2 && \
    pip install psycopg2==2.4.1 && \
    pip install wsgiref==0.1.2 && \
    pip install ordereddict==1.1 && \
    pip install pillow==2.3.0 && \
    pip install django-widget-tweaks==1.1.1 && \
    pip install lxml==4.6.5 && \
    pip install pyyaml==5.4.1 && \
    pip install webassets==0.7.1 && \
    pip install yuicompressor && \
    pip install jsonfield && \
    pip install django-tastypie==0.9.16 && \
    pip install django-htmlmin==0.7.0 && \
    pip install celery==3.1.25 && \
    pip install django-celery==3.1.16 && \
    pip install defusedxml==0.4.1 && \
    pip install django-countries==3.3 && \
    pip install "elasticsearch>=1.0.0,<2.0.0" && \
    pip install zerorpc==0.4.4 && \
    pip install packtools==2.1.0 && \
    pip install scielo-django-extensions==0.4

# Install thriftpy and thriftpywrap
RUN pip install thriftpy==0.3.9 && \
    pip install git+https://github.com/scieloorg/thriftpy-wrap@0.1.1#egg=thriftpywrap

# Copy project files
COPY . /app/

# Create directories for static and media files
RUN mkdir -p /app/static /app/media

# Create a non-root user to run the application
RUN useradd -m -s /bin/bash django && \
    chown -R django:django /app

USER django

# Expose port
EXPOSE 8000

# Run Django development server (for production, use gunicorn or uwsgi)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]