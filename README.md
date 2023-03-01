# Placement-Portal

### 1. Clone the repo
```base
git clone https://github.com/PLACEMENT-JKSHIM/Placement-Portal-Backend.git
```
> Note: make sure you after this step 
```cd Placement-Portal-Backend```

### 2. Create Python virtual environment
```base
python -m venv env
```

### 3. Enter virtual enviroment
```base
.\env\Scripts\activate
```

### 4. Install python modules
```base
pip install -r requirements.txt
```

### 5. Migrate Database
```base
python manage.py makemigrations
```
```base
python manage.py migrate
```

### 6.Create a super user. This is to access Admin panel and admin specific pages.
```base
python manage.py createsuperuser
```

### 7. Run Server
```base
python manage.py runserver
```

### 8. Tailwind Setup
```base
npm i
```
```base
npm run dev
```
> Note: this commands watches changes in tailwind output file (run it in another terminal in vscode and then run server)
