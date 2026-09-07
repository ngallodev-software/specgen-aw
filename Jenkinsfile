pipeline {
    agent any

    environment {
        SPECGEN_AGENT_WORKFLOW_ROOT = "${WORKSPACE}/.agent-workflow"
        AGENT_WORKFLOW_SOURCE_ROOT = "${WORKSPACE}/.agent-workflow"
        SPECGEN_VENV = "${WORKSPACE}/.venv"
    }

    options {
        disableConcurrentBuilds()
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
    }

    stages {
        stage('Prepare Agent-Workflow') {
            steps {
                sh '''
                    set -eu
                    config=dev/agent-workflow.example.toml
                    if [ -f dev/agent-workflow.toml ]; then config=dev/agent-workflow.toml; fi
                    ref=$(sed -n '/^expected_snapshot = /p' "$config" | sed 's/.*-//; s/"//g')
                    test -n "$ref"
                    rm -rf "$WORKSPACE/.agent-workflow"
                    git clone --quiet /lump/apps/agent-workflow "$WORKSPACE/.agent-workflow"
                    git -C "$WORKSPACE/.agent-workflow" checkout --quiet --detach "$ref"
                '''
            }
        }
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
