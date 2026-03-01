pipeline {
    agent any

    stages {
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
            // Публикация результатов тестов в веб-интерфейсе Jenkins
            junit 'test-results.xml'
            
            // Сохранение артефактов (отчёт можно скачать)
            archiveArtifacts artifacts: 'test-results.xml', 
                           fingerprint: true, 
                           allowEmptyArchive: true
            
            echo '📊 Отчёты сохранены и опубликованы в веб-интерфейсе Jenkins'
        }
        success {
            echo '🎉 Сборка и все тесты прошли успешно!'
        }
        failure {
            echo '❌ Ошибка в сборке или тестах. Смотрите логи и Test Result.'
        }
    }
}
