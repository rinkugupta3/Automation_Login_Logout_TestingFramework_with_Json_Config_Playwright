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

        stage('Set up Virtual Environment') {
            steps {
                bat '''
                    if not exist venv (
                        C:\\Users\\dhira\\AppData\\Local\\Programs\\Python\\Python311\\python.exe -m venv venv
                    )
                '''
            }
        }

        stage('Set up Python environment') {
            steps {
                // Original: upgrade pip
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pip install --upgrade pip"
                // Original: install requirements
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pip install -r requirements.txt"
                // Original: install pytest-html (fixed typo: pytest.html -> pytest-html)
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pip install pytest-html"

                // New: install same dependencies inside venv
                bat 'venv\\Scripts\\pip.exe install --upgrade pip'
                bat 'venv\\Scripts\\pip.exe install -r requirements.txt'
                bat 'venv\\Scripts\\pip.exe install pytest-html'
            }
        }

        stage('Install Playwright Browsers') {
            steps {
                // Original: install all browsers
                bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m playwright install"
                // New: install chromium inside venv
                bat 'venv\\Scripts\\python.exe -m playwright install chromium'
            }
        }

        stage('Dev - Env Playwright Tests') {
            steps {
                // Original: run tests with global python (kept for reference)
                // bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pytest"
                // bat "C:/Users/dhira/AppData/Local/Programs/Python/Python311/python.exe -m pytest --html=report_playwright_bdd.html"

                // New: run tests using venv python (avoids langsmith conflict)
                bat 'venv\\Scripts\\python.exe -m pytest'
                bat 'venv\\Scripts\\python.exe -m pytest --html=report_playwright_bdd.html'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            archiveArtifacts artifacts: 'screenshots/**/*', allowEmptyArchive: true
            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'report_playwright_bdd.html',
                reportName: 'Playwright Test Report'
            ])
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}