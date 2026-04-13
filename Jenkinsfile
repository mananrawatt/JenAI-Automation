pipeline {
    agent any

    parameters {
        choice(name: 'BRANCH', choices: ['test', 'prod'], description: 'Select branch to deploy')
    }

    environment {
        IMAGE_NAME = "jenai-app"
        VERSION = "${BUILD_NUMBER}"
        KIND_CLUSTER = "jenai-cluster"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: "${params.BRANCH}", url: 'https://github.com/mananrawatt/JenAI-Automation.git'
            }
        }

        stage('Check Docker') {
        steps {
            sh 'docker version'
        }
    }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t $IMAGE_NAME:v$VERSION .
                """
            }
        }

        stage('Load Image into Kind') {
            steps {
                sh """
                kind load docker-image $IMAGE_NAME:v$VERSION --name $KIND_CLUSTER
                """
            }
        }

        stage('Update Kubernetes Deployment') {
            steps {
                sh """
                kubectl set image deployment/jenai-app jenai-app=$IMAGE_NAME:v$VERSION
                """
            }
        }

        stage('Verify Deployment') {
            steps {
                sh """
                kubectl rollout status deployment jenai-app
                """
            }
        }
    }
}
