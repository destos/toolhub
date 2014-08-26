base:
  '*':
    - requirements.essential
    - ssh
  'vagrant.toolhub.co':
    - toolhub.requirements
    - toolhub.nginx
    - toolhub.share
    - toolhub.venv
    - toolhub.uwsgi
    - toolhub.postgresql

