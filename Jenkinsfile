pipeline{
    agent any
    environment{
        IMAGE = "praveendevopsnexus/app"
    }
    stages{
        stage("Git Clone"){
            steps{
                git branch: 'master', credentialsId: 'github', url: 'https://github.com/pravi1991/my_first_web.git'
            }
        }
        stage("Docker Build"){
            steps{
                withDockerRegistry(credentialsId: 'dockerHub', url: 'https://registry.hub.docker.com') {
                    sh "docker build -t ${IMAGE} ."
                }
            }
        }
        stage("Docker Push"){
            steps{
                withCredentials([string(credentialsId: 'dockerhub_password', variable: 'dockerhub_password')]) {
                    sh "docker login -u praveendevopsnexus -p ${dockerhub_password}"
                    sh "docker push ${IMAGE}"
                }
            }
        }
        stage("Deploy to Kubernetes"){
            steps{
                kubernetesDeploy(
                    configs: "manifest/",
                    kubeconfigId: "kube_config_gcp"
                )
            }
        }
    }
}
