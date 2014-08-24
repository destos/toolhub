include:
  - nginx

toolhub-nginx-conf:
  file.managed:
    - name: /etc/nginx/sites-available/toolhub.conf
    - source: salt://toolhub/nginx.conf
    - template: jinja
    - user: www-data
    - group: www-data
    - mode: 755
    - require:
      - pkg: nginx

# Symlink and thus enable the virtual host
toolhub-enable-nginx:
  file.symlink:
    - name: /etc/nginx/sites-enabled/toolhub.conf
    - target: /etc/nginx/sites-available/toolhub.conf
    - force: false
    - require:
      - file: toolhub-nginx-conf
