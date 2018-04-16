pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        bat(script: 'C:\\Python27\\python.exe tests\\test_example_form.py -B Chrome', returnStatus: true)
      }
    }
  }
}