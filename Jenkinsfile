pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds') // Add in Jenkins credentials
        DOCKER_IMAGE = '<dockerhub-username>/sleepsense-app'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/<your-username>/SleepSense.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                sh 'docker push $DOCKER_IMAGE:latest'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f deployment.yaml'
                sh 'kubectl apply -f service.yaml'
            }
        }
    }

    post {
        success { echo "✅ Deployment completed successfully!" }
        failure { echo "❌ Deployment failed." }
    }
}
