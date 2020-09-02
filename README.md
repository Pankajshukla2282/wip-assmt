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
3. Do the coding part, develop components for stack
4. Deployment the stack
	cdk deploy announce
5. CloudFormation Template
	Get it in cdk.out/announce.template.json
6. Destroy the stack
	cdk destroy	announce
