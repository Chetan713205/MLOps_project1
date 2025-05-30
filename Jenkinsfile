pipeline {
    agent any

    environment{
        VENV_DIR = 'venv'
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
    }
}
