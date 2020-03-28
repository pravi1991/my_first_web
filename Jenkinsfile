pipeline{
    agent any
    environment{
        APP='flask-app'
        BLUE='flask-app-blue'
        GREEN='flask-app-green'
        MANIFEST_PATH='manifest'
        DEPLOYMENT_FILE='deployment.yaml'
        SERVICE_FILE='service.yaml'
        IMAGE='praveendevopsnexus/app'
        GIT_URL='https://github.com/pravi1991/my_first_web.git'
        DOCKER_USER='praveendevopsnexus'
        DOCKER_REGISTRY='https://registry.hub.docker.com'
        LAST_DEPLOY=''
    }   
    stages{
        stage("Git Clone"){
            steps{
                git branch: 'master', credentialsId: 'github', url: env.GIT_URL
            }
        }
        stage("Docker Build"){
            steps{
                withDockerRegistry(credentialsId: 'dockerHub', url: env.DOCKER_REGISTRY ) {
                    sh "docker build -t ${IMAGE} ."
                }
            }
        }
        stage("Docker Push"){
            steps{
                withCredentials([string(credentialsId: 'dockerhub_password', variable: 'dockerhub_password')]) {
                    sh "docker login -u ${DOCKER_USER} -p ${dockerhub_password}"
                    sh "docker push ${IMAGE}"
                }
            }
        }
        stage("Deploy to Kubernetes"){
            steps{
                script{
                    echo "GET THE LAST DEPLOYMENT"
                    env.DEPLOYMENT=sh( 
                     script: 
                     '''
                        set +e
                        DEPLOY=`kubectl get deploy -o jsonpath="{.items[*].metadata.name}" | egrep "^\${APP}"`
                        [ -z $DEPLOY ] && echo -n 'none'|| echo $DEPLOY
                        set -e
                     ''',
                     returnStdout: true
                    ).trim()
                    echo "GET SERVICE"
                    sh(script: 
                     '''
                        set +e
                        kubectl get service ${SERVICE}
                        [ $? != 0 ] && sed "s|DEPLOYMENT|${DEPLOYMENT}|g" ${MANIFEST_PATH}/${SERVICE_FILE}
                        kubectl apply -f ${MANIFEST_PATH}/${SERVICE_FILE}
                        echo ${DEPLOYMENT}
                        set -e
                     ''')
                }
                script{
                    withEnv(["LAST_DEPLOY=${DEPLOYMENT}"]){
                        if (DEPLOYMENT == 'none') { env.DEPLOYMENT=env.BLUE }
                        else{
                            if ( DEPLOYMENT == env.BLUE ) { 
                                echo 'inside else if'
                                env.DEPLOYMENT=env.GREEN 
                                echo env.DEPLOYMENT
                            }
                            else { 
                                echo 'inside else else'
                                env.DEPLOYMENT=env.BLUE }
                                echo env.DEPLOYMENT
                        }
                        sh 'sed -i "s|DEPLOYMENT|\${DEPLOYMENT}|g" ${MANIFEST_PATH}/${DEPLOYMENT_FILE}'
                        sh 'sed -i "s|APP|${APP}|g" ${MANIFEST_PATH}/${DEPLOYMENT_FILE}'
                        sh 'sed -i "s|IMAGE|${IMAGE}|g" ${MANIFEST_PATH}/${DEPLOYMENT_FILE}'
                        sh 'sed -i "s|DEPLOYMENT|\${DEPLOYMENT}|g" ${MANIFEST_PATH}/${SERVICE_FILE}'
                        kubernetesDeploy(
                            configs: "${MANIFEST_PATH}/${DEPLOYMENT_FILE}",
                            kubeconfigId: "kube_config_gcp"
                        )
                        sh '''
                        READY=$(kubectl get deploy $DEPLOYMENT -o json | jq '.status.conditions[] | select(.reason == "MinimumReplicasAvailable") | .status' | tr -d '"')
                        while [[ "$READY" != "True" ]]; do
                            READY=$(kubectl get deploy $DEPLOYMENT -o json | jq '.status.conditions[] | select(.reason == "MinimumReplicasAvailable") | .status' | tr -d '"')
                        done
                        '''
                        kubernetesDeploy(
                            configs: "${MANIFEST_PATH}/${SERVICE_FILE}",
                            kubeconfigId: "kube_config_gcp"
                        )
                        if (env.LAST_DEPLOY != 'none'){
                            sh 'kubectl delete deploy ${LAST_DEPLOY}'
                        }
                    }
                }
                        
        }
    
    }
}
