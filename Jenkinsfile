pipeline {
    agent any

    environment{
        VENV_DIR = 'venv'
        GCP_PROJECT = 'gen-lang-client-0389229415'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
    }

    stages {
        stage('Cloning GitHub repo to Jenkins') {
            steps {
                echo '.........Cloning GitHub repo to Jenkins.........'
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Chetan713205/MLOps_project1.git',
                        credentialsId: 'github-token'
                    ]],
                    extensions: []
                ])
            }
        }
        stage('Setting up Virtual Environment and Installing Dependencies') { 
            steps {
                script{
                    echo '.........Setting up Virtual Environment and Installing Dependencies.........'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
        stage('Building and pushing docker image to GCR') { 
            steps {
                withCredentials([file(credentialsId : 'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo '.........Building and pushing docker image to GCR.........'
                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}
                            gcloud auth configure-docker --quiet

                            docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                            docker push gcr.io/${GCP_PROJECT}/ml-project:latest 
                        '''
                    }
                }
            }
        }
    }
}
