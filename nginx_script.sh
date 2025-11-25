cp ark2020.nginx /etc/nginx/sites-available/
rm /etc/nginx/sites-enabled/ark2020.nginx
ln -s /etc/nginx/sites-available/ark2020.nginx /etc/nginx/sites-enabled/
service nginx restart