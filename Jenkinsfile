pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                // Checkout from dev-env branch
                git branch: 'dev-env', url: 'https://github.com/rinkugupta3/Automation_Login_Logout_TestingFramework_with_Json_Config_Playwright'

                // To switch to main branch, comment out the above line and uncomment the line below:
                // git branch: 'main', url: 'https://github.com/rinkugupta3/Playwright_Automation_DesignSetup'
            }
        }
        stage('Set up Python environment') {
            steps {
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pip install --upgrade pip"
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pip install -r requirements.txt"
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pip install pytest.html"
            }
        }
        stage('Install Playwright Browsers') {
            steps {
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m playwright install"
            }
        }
        stage('Dev - Env Playwright Tests') {
            steps {
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pytest"
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pytest --html=report_playwright_bdd.html"            }
        }
    }
   post {
        always {
            echo 'Cleaning up...'
            archiveArtifacts artifacts: 'screenshots/**/*', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}