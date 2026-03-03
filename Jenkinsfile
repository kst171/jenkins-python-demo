pipeline {
    agent { label 'python' }

    environment {
        EMAIL_TO = "tymanovich17@gmail.com"
        VENV_DIR = "${WORKSPACE}/venv"
    }

    stages {
        stage('Информация об окружении') {
            steps {
                sh 'whoami'
                sh 'pwd'
                sh 'git --version'
                sh 'python3 --version'
                sh 'java -version'
            }
        }

        stage('Клонирование репозитория из Git') {
            steps {
                checkout scm
                echo '✅ Репозиторий успешно клонирован'
            }
        }

        stage('Сборка приложения (pip)') {
            steps {
                sh '''
                    rm -rf venv || true
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
                echo '✅ Сборка завершена: зависимости установлены'
            }
        }

        stage('Запуск автоматических тестов') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest --junitxml=test-results.xml --tb=short -q
                '''
                echo '✅ Тесты выполнены'
            }
        }
    }

    post {
        always {
            junit 'test-results.xml'
            archiveArtifacts artifacts: 'test-results.xml',
                             fingerprint: true,
                             allowEmptyArchive: true
            echo '📊 Отчёты сохранены и опубликованы в веб-интерфейсе Jenkins'
        }

        success {
            echo '🎉 Сборка и все тесты прошли успешно!'
            emailext(
                to: "${EMAIL_TO}",
                subject: "✅ ${JOB_NAME} #${BUILD_NUMBER} — SUCCESS",
                mimeType: 'text/html',
                body: """
                    <h2>✅ Сборка прошла успешно</h2>
                    <table>
                        <tr><td><b>Проект:</b></td><td>${JOB_NAME}</td></tr>
                        <tr><td><b>Сборка:</b></td><td>#${BUILD_NUMBER}</td></tr>
                        <tr><td><b>Ветка:</b></td><td>${GIT_BRANCH}</td></tr>
                        <tr><td><b>Коммит:</b></td><td>${GIT_COMMIT}</td></tr>
                        <tr><td><b>Длительность:</b></td><td>${currentBuild.durationString}</td></tr>
                    </table>
                    <br>
                    <a href="${BUILD_URL}">Открыть сборку</a> |
                    <a href="${BUILD_URL}testReport">Результаты тестов</a>
                """
            )
        }

        failure {
            echo '❌ Ошибка в сборке или тестах. Смотрите логи и Test Result.'
            emailext(
                to: "${EMAIL_TO}",
                subject: "❌ ${JOB_NAME} #${BUILD_NUMBER} — FAILED",
                mimeType: 'text/html',
                attachLog: true,
                body: """
                    <h2>❌ Сборка упала!</h2>
                    <table>
                        <tr><td><b>Проект:</b></td><td>${JOB_NAME}</td></tr>
                        <tr><td><b>Сборка:</b></td><td>#${BUILD_NUMBER}</td></tr>
                        <tr><td><b>Ветка:</b></td><td>${GIT_BRANCH}</td></tr>
                        <tr><td><b>Коммит:</b></td><td>${GIT_COMMIT}</td></tr>
                        <tr><td><b>Длительность:</b></td><td>${currentBuild.durationString}</td></tr>
                    </table>
                    <br>
                    <a href="${BUILD_URL}console">Посмотреть логи</a> |
                    <a href="${BUILD_URL}testReport">Результаты тестов</a>
                    <br><br>
                    <i>Лог сборки во вложении</i>
                """
            )
        }

        unstable {
            echo '⚠️ Сборка нестабильна — часть тестов упала'
            emailext(
                to: "${EMAIL_TO}",
                subject: "⚠️ ${JOB_NAME} #${BUILD_NUMBER} — UNSTABLE",
                mimeType: 'text/html',
                body: """
                    <h2>⚠️ Сборка нестабильна</h2>
                    <table>
                        <tr><td><b>Проект:</b></td><td>${JOB_NAME}</td></tr>
                        <tr><td><b>Сборка:</b></td><td>#${BUILD_NUMBER}</td></tr>
                        <tr><td><b>Ветка:</b></td><td>${GIT_BRANCH}</td></tr>
                    </table>
                    <br>
                    <a href="${BUILD_URL}testReport">Посмотреть упавшие тесты</a>
                """
            )
        }
    }
}