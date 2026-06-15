pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t log-analyzer .'
            }
        }

        stage('Test') {
            steps {
                sh 'docker run --rm log-analyzer'
            }
        }
    }

    post {
        success {
            echo 'Tous les tests sont passes'
        }
        failure {
            echo 'Des tests ont echoue'
        }
    }
}
