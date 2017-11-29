"""
@author Bryan Hopkins pennbwh@gmail.com

This script, intended to be run by a lambda function, will spider all repositories in a gitlab.com team,
and for each branch, if it has been modified more recently than the copy in S3, upload a new zip backup of
that branch to S3, with the branch name appended to the repo name.

There are better ways to do this.  This exists largely as a peace of mind backup, and as a training exercise
and conceptual example.
"""
import gitlab
import manage_s3
import StringIO
import gc
from dateutil.parser import parse

gl = gitlab.Gitlab("https://gitlab.com", "GITLAB_ACCESS_KEY", api_version=4)
group = gl.groups.get("GITLAB_GROUP_NAME")


def main(event, context):
    print ("Group " + group.name + " has ID " + str(group.id))
    # Get all the groups in the project (https://docs.gitlab.com/ee/api/groups.html)
    # Have to set all=True: https://github.com/python-gitlab/python-gitlab/issues/93
    projects = group.projects.list(all=True)
    for project in projects:
        print(project.ssh_url_to_repo)

        # Get all the branches in the project (http://python-gitlab.readthedocs.io/en/stable/gl_objects/branches.html)
        if project.default_branch is None:
            # This signifies that the repo was never initialized and we'll get a 500 from gitlab
            continue
        branches = project.branches.list(all=True)
        for branch in branches:
            branch_last_modified = branch.commit['committed_date']
            print(branch.name + " branch of " + project.path + " was last modified " + str(branch_last_modified))
            # branch_last_modified = datetime.strptime(str(branch_last_modified), '%Y-%m-%dT%H:%M:%S.%f%z')
            # Python 2.7 barfs on %z
            branch_last_modified = parse(branch_last_modified)

            object_key = manage_s3.s3_object_name_from_repo(project.path, branch.name)
            object_last_modified = manage_s3.s3_object_last_modified(object_key)
            print(object_key + " was last modified " + str(object_last_modified))

            # It's worth downloading the zip and uploading
            if object_last_modified is None or branch_last_modified > object_last_modified:
                tgz = project.repository_archive(branch=branch.name)
                data = StringIO.StringIO(tgz)
                manage_s3.s3_store_repo(object_key, data)
                data.close()
                gc.collect()
                print(object_key + " updated")
            else :
                print(object_key + " skipped")


main(None, None)
