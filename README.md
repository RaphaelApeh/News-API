**🌐 News API 📰 with django and django rest framework 😍**

- **clone** <br>

```bash
git clone https://github.com/RaphaelApeh/News-API.git
```
- __Setting a vitual environment__
```bash
python -m venv venv
```
- <b>Activate</b>
* Windows
```bash
.\venv\scritps\activate
```
* MacOS or Linux
```bash
source bin/scritps/activate
```
- **Installing requirements**
```bash
pip install -r requiremets.txt
```
- Working dir
```bash
cd src/
```
- **.env**
```python
DJANGO_DEBUG=True
DJANGO_SECRET_KEY="secret-key"
```
- Generate `SECRET_KEY`
```bash
python manage.py shell --command="from django.core.management.utils import get_random_secret_key;print(get_random_secret_key())"
```
- **Run the development server**
```bash
python manage.py runserver
```