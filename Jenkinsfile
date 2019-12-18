pipeline {
  agent {
    docker {
      image 'ubuntu'
    }

  }
  stages {
    stage('Build') {
      steps {
        sh '''uname -a 
ping -c 3 google.com'''
        git 'https://github.com/pravi1991/my_first_web.git'
      }
    }

  }
}