pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
    }

    triggers {
        pollSCM('H/5 * * * *')
    }

    stages {
        stage('Install') {
            steps {
                sh './scripts/install.sh'
            }
        }
        stage('Release checks') {
            steps {
                sh 'timeout 60s .venv/bin/python tests/release/verify_versions.py'
                sh 'timeout 60s env PYTHONPATH=src .venv/bin/python tests/critical-seams/run.py'
            }
        }
    }
}
