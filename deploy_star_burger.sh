#!/bin/bash
set -e
cd /opt/StarBurgerFastFood  # замените на путь до вашего проекта
if git pull | grep -q 'Already up to date.'
then
echo 'Already up to date.'
else
source ./venv/bin/activate
pip install -r requirements.txt
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
python3 manage.py collectstatic --noinput
python3 manage.py migrate --noinput
systemctl restart star_burger.service
curl --request POST \
     --url https://api.rollbar.com/api/1/deploy \
     --header "X-Rollbar-Access-Token: $ROLLBAR_TOKEN" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     --data '
{
  "environment": "production",
  "revision": "$(git rev-parse HEAD)"
}
'
echo "deployment completed successfully"
fi