#!groovy

pipeline {

  agent {
    label 'node'
  }

  stages {

    // --- BUILD ---
    stage('Test') {
      agent {
        label "node"
      }
      steps {
        deleteDir()
        checkout scm
        sh 'make'
        sh 'make test'
        sh 'tar cfz stash.tgz bin develop-eggs include lib parts var webpack/node_modules *.cfg requirements.txt'
        stash includes: 'stash.tgz', name: 'stash.tgz'
      }
    }
  }

  post {
    success {
      slackSend (
        color: 'good',
        message: "SUCCESS: #${env.BUILD_NUMBER} ${env.JOB_NAME} (${env.BUILD_URL})"
      )
    }
    failure {
      slackSend (
        color: 'danger',
        message: "FAILURE: #${env.BUILD_NUMBER} ${env.JOB_NAME} (${env.BUILD_URL})"
      )
    }
    unstable {
      slackSend (
        color: 'warning',
        message: "UNSTABLE: #${env.BUILD_NUMBER} ${env.JOB_NAME} (${env.BUILD_URL})"
      )
    }
    aborted {
      slackSend (
        color: 'danger',
        message: "ABORTED: #${env.BUILD_NUMBER} ${env.JOB_NAME} (${env.BUILD_URL})"
      )
    }
  }
}