pipeline {
    agent any

    stages {
        stage('Hello') {
            steps {
                echo '🎉 Jenkins Pipeline is working!'
            }
        }

        stage('Wait a Bit') {
            steps {
                echo '⏳ Sleeping for 5 seconds...'
                sleep time: 5, unit: 'SECONDS'
            }
        }

        stage('Goodbye') {
            steps {
                echo '✅ Test pipeline completed!'
            }
        }
    }

    post {
        always {
            echo '📦 Pipeline run finished (success or fail).'
        }
    }
}
