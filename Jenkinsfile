pipeline {
  agent {
    docker {
      image 'ubuntu'
    }

  }
  stages {
    stage('test') {
      steps {
        echo 'test'
        sh 'mkdir /tmp/testing_from_blueocean'
      }
    }

  }
}