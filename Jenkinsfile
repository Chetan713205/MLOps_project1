pipeline {
    agent any

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
    }
}
