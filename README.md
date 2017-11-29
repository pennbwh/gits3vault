# GitS3Vault

Extract all branches of all projects in a Gitlab.com hosted Group and store backups of them in an AWS S3 bucket.
This toy/proof of concept exists largely as a peace-of-mind exercise in response to Gitlab.com outages and an excuse
use-case to mess around with AWS APIs and to experiment with AWS CodeCommit and CodeBuild.

This is not the easiest way to solve this problem.  If you're looking for an actual solution, just clone your repos 
to another remote on another platform with a webhook.  If you're looking to play with boto3 or the Gitlab APIs and my 
fumblings are useful to you, that's what OSS is for!  This will extract each branch of each repo from git, and if its 
more recent than the copy currently backed up in the S3 bucket, it will add it as an object to the bucket.

I was motivated to open the kimono and air my bad code by an 
excellent FOSSCON 2017 lightning talk by https://twitter.com/ShillaSaebi Enjoy.  :)

Developed on Python 2.7 because its ubiquitous but would've been easier on 3.6.

Before you start, make sure you have a credentials file set up for your AWS account in ~/.aws/credentials.  
Boto3 depends on it.

To install/build:
```
virtualenv env
. env/bin/activate (or '. env/Scripts/activate for windows')
pip install -r requirements.txt
```

Run the logic locally with 
```
python repoextract.py
```

Setup on AWS is to create a CodeBuild process that will execute the buildspec.yml to generate a deployment file and put 
it in another S3 bucket, and then configure a lambda function to be sourced from that bucket and run on a cloudwatch 
hook.  That's all done manually (bad!) through the console right now but captured as TODOs in lambda_deploy.py. 
In my free time I'll cloudformation it like a good person.
