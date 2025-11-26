// Jenkins Pipeline defined using the declarative syntax
pipeline {
    agent any 

    environment {
        // --- Placeholders defined ---
        DOCKERHUB_USERNAME = 'vaishak2005'
        ROLL_NUMBER = 'imt2023085'
        // FIX: Removed trailing whitespace from credential ID
        DOCKER_CREDS_ID = 'dockerhub-creds' 
        
        IMAGE_NAME = "${DOCKERHUB_USERNAME}/${ROLL_NUMBER}-cli-todo"
        // Define the full path for the Docker executable once
        DOCKER_CLI = '/usr/local/bin/docker'
    }

    stages {
        // 1. Checkout Stage: Pulls the code from GitHub
        stage('Pull Code (Checkout)') {
            steps {
                git branch: 'main', url: 'https://github.com/vaishak-iiitb/todo-cli-app'
            }
        }

        // 2. Build Stage: Creates and configures the Python environment
        stage('Create Virtual Environment & Install Deps') {
            steps {
                echo 'Creating Python Virtual Environment...'
                sh '/usr/bin/python3 -m venv .venv'
                
                echo 'Installing Pytest and other dependencies from requirements.txt...'
                sh '.venv/bin/pip install --upgrade pip'
                sh '.venv/bin/pip install -r requirements.txt'
            }
        }

        // 3. Test Stage: Runs the automated tests using Pytest
        stage('Run Tests (Pytest)') {
            steps {
                script {
                    echo 'Running Pytest tests...'
                    withEnv(['PYTHONPATH=src/main/python']) {
                        def testResult = sh(returnStatus: true, script: '.venv/bin/pytest -v')
                        if (testResult != 0) {
                            error 'Pytest failed. Aborting pipeline.'
                        }
                    }
                }
            }
        }

        // 4. Docker Build Stage: FIXES rate limit by logging in BEFORE build
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}:latest"
                
                script {
                    // Login to DockerHub using the stored Jenkins credential to use authenticated pull quota
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDS_ID}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        
                        echo 'Logging into DockerHub to bypass pull rate limits...'
                        sh "echo \$DOCKER_PASSWORD | ${DOCKER_CLI} login -u \$DOCKER_USERNAME --password-stdin"

                        // Apply DOCKER_BUILDKIT=0 fix and run build
                        withEnv(["DOCKER_BUILDKIT=0"]) {
                            sh "${DOCKER_CLI} build -t ${IMAGE_NAME}:latest ."
                        }
                        
                        // Logout immediately to not carry session state into the next stage
                        sh "${DOCKER_CLI} logout"
                    }
                }
                
                // Check the image was created
                sh "${DOCKER_CLI} images | grep ${IMAGE_NAME}"
            }
        }
        
        // 5. Docker Push Stage: Pushes the image to DockerHub (requires re-login)
        stage('Push Docker Image to Hub') {
            steps {
                script {
                    // Relog in just for the push
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDS_ID}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        
                        echo 'Re-logging into DockerHub for push...'
                        sh "echo \$DOCKER_PASSWORD | ${DOCKER_CLI} login -u \$DOCKER_USERNAME --password-stdin"
                        
                        echo "Pushing Docker image ${IMAGE_NAME}:latest..."
                        sh "${DOCKER_CLI} push ${IMAGE_NAME}:latest"
                        
                        // Final logout
                        sh "${DOCKER_CLI} logout"
                    }
                }
            }
        }
    }
    
    // Post-build actions
    post {
        always {
            echo 'Pipeline execution finished.'
        }
        success {
            echo 'Pipeline succeeded! Docker image pushed to DockerHub.'
        }
        failure {
            echo 'Pipeline failed! Check logs for errors.'
        }
        cleanup {
            deleteDir() 
        }
    }
}
