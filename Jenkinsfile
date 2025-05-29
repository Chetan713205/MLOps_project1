pipeline{
    agent any

    stage('Cloning GitHub repo to Jenkins'){
        steps{
            script{
                echo '.........Cloning GitHub repo to Jenkins.........'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Chetan713205/MLOps_project1.git']])
            }
        }
    }
}