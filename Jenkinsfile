pipeline {
    agent any

    environment {
        APP_NAME = "sleepsense"
        DOCKER_IMAGE = "sleepsense-app:latest"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running basic Flask test..."
                sh 'python -m py_compile app.py' // simple syntax check
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Run Container') {
            steps {
                echo "Running container..."
                sh 'docker run -d -p 5000:5000 --name ${APP_NAME} ${DOCKER_IMAGE}'
            }
        }

        stage('Post-Build Cleanup') {
            steps {
                echo "Cleaning up old containers..."
                sh 'docker stop ${APP_NAME} || true'
                sh 'docker rm ${APP_NAME} || true'
            }
        }
    }

    post {
        success {
            echo "✅ Build & deployment completed successfully!"
        }
        failure {
            echo "❌ Build failed. Check logs for details."
        }
    }
}
