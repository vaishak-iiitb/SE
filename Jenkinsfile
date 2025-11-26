pipeline {
    agent any

    environment {
        IMAGE = "vaishak2005/ci-cd-demo2:jenkins"
        VENV = ".venv"
        PYTHON = "/usr/bin/python3" 
    }

    stages {

        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM',
                  branches: [[name: '*/main']],
                  userRemoteConfigs: [[
                    url: 'https://github.com/vaishak-iiitb/SE',
                    credentialsId: 'github_jenkins'
                  ]]
                ])
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh '$PYTHON -m venv $VENV'
                sh '$VENV/bin/pip install --upgrade pip'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '$VENV/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '$VENV/bin/pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                  usernameVariable: 'USER',
                                                  passwordVariable: 'PASS')]) {
                    sh '''
                      echo $PASS | docker login -u $USER --password-stdin
                      docker push $IMAGE
                    '''
                }
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                  docker pull $IMAGE
                  docker stop ci-cd-demo || true
                  docker rm ci-cd-demo || true
                  docker run -d -p 5000:5000 --name ci-cd-demo $IMAGE
                '''
            }
        }
    }
}
