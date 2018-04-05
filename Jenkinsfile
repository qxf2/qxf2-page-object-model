pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        bat(script: 'python tests/test_example_form.py', returnStatus: true, returnStdout: true)
      }
    }
  }
}