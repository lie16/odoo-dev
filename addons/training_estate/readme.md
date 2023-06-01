1. Create python package
2. add init and manifest .py
3. define manifest.py as is
4. restart server
5. update app list
6. install app
7. bikin models dengan field utama _name dan nama tabel untunk bisa bikin tabel
8. jangan lupa tambahkan base security pada ir.model.access.csv convention lihat di : https://www.odoo.com/documentation/16.0/developer/tutorials/getting_started/05_securityintro.html
9. import each file
10. restart server
11. update module with these syntax python odoo-bin -r dbuser -w dbpassword --addons-path=addons -d mydb -u training_estate --dev xml
12. create access right at folder security with file name ir.model.access.csv
13. create view
14. create menu
15. create tree view
16. create form
17. create search