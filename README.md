1. Installatins
	a. NodeJs 10.3.0 or later
	b. Install AWS CLI
	c. Install AWS CDK CLI (npm install -g aws-cdk)
2. Setup
	a. aws configure
	b. application
		cd wip-assmt
		source .env/bin/activate
			pip install -r requirements.txt
			cdk bootstrap
			cdk deploy announce
			
			Do the changes in files as per requirement
			cdk destroy	
