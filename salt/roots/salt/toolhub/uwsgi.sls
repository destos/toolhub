include:
  - uwsgi

toolhub-uwsgi:
  file.managed:
    - name: /etc/uwsgi/apps-available/toolhub.ini
    - source: salt://toolhub/uwsgi.ini
    - template: jinja
    - user: www-data
    - group: www-data
    - mode: 755
    - require:
      - pip: uwsgi

enable-uwsgi-app:
  file.symlink:
    - name: /etc/uwsgi/apps-enabled/toolhub.ini
    - target: /etc/uwsgi/apps-available/toolhub.ini
    - force: false
    - require:
      - file: toolhub-uwsgi
      - file: /etc/uwsgi/apps-enabled
