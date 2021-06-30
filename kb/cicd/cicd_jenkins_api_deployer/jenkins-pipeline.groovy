pipeline {
    agent any
    environment {
        api_package_id = "${sh(returnStdout: true, script: 'echo "${API_SERVICE_ID}_v`date +%Y-%m-%d_%H-%M-%S`"').trim()}"
    }
    stages {
        stage('PREPARE'){
            steps {
                cleanWs()
                sh 'echo ${bundle_name}'
                git credentialsId: "git_hub_ssh", url: "git@github.com:fsergot/dss_api_pipeline.git"
                sh "cat requirements.txt"
                sh "printenv"
                withPythonEnv('python3') {
                    // sh "pip install -U pip"
                    sh "pip install -r requirements.txt"
                }
            }
        }
        stage('PACK_AND_PUB') {
            steps {
                withPythonEnv('python3') {
                    sh "python 1_package_and_publish/run_packaging.py '${DESIGN_URL}' '${DESIGN_API_KEY}' '${DSS_PROJECT}' '${API_SERVICE_ID}' '${api_package_id}' '${API_DEV_INFRA_ID}' '${API_PROD_INFRA_ID}'"
                }
            }
        }
        stage('DEV_TEST') {
            steps {
                withPythonEnv('python3') {
                    sh "python 2_deploy_dev/run_deploy_dev.py '${DESIGN_URL}' '${DESIGN_API_KEY}' '${DSS_PROJECT}' '${API_SERVICE_ID}' '${api_package_id}' '${API_DEV_INFRA_ID}'"
                    sh "pytest -s 2_deploy_dev/test_dev.py -o junit_family=xunit1 --host='${DESIGN_URL}' --api='${DESIGN_API_KEY}' --api_service_id='${API_SERVICE_ID}' --api_endpoint_id='${API_ENDPOINT_ID}' --api_dev_infra_id='${API_DEV_INFRA_ID}' --junitxml=reports/DEV_TEST.xml"
                    
                }                
            }
        }
        stage('DEPLOY_TO_PROD') {
            steps {
                script {
                try {
                    withPythonEnv('python3') {
                        sh "python 3_deploy_prod/run_deploy_prod.py '${DESIGN_URL}' '${DESIGN_API_KEY}' '${DSS_PROJECT}' '${API_SERVICE_ID}' '${api_package_id}' '${API_PROD_INFRA_ID}'"
                    }
                } catch (Exception err) {
                        echo 'Exception occurred: ' + err.getMessage()
                        if(err.getMessage().contains("code 2"))
                            currentBuild.result = 'UNSTABLE'
                        else
                            currentBuild.result = 'FAILURE'
                }
                }
            }
        }
    }
    post{
        always {
            junit 'reports/**/*.xml'
      }
    }
}
