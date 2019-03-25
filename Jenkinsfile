pipeline {
	agent {
		dockerfile {
			label "docker && linux"
			args "-u 1001:1001"
		}
	}
	stages {
		stage("Build") {
			steps {
				sh "python3 -m py_compile textle/__init__.py"
			}
		}
		stage("Archive") {
			steps {
				sh "python3 setup.py bdist_wheel sdist"
				archiveArtifacts artifacts: 'dist/*', onlyIfSuccessful: true
			}
		}
	}
}
