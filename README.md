<img alt="Logo" src="http://coderslab.pl/svg/logo-coderslab.svg" width="400">

# ScrumLab Python

## Jak skonfigurować aplikację?

### Co skonfigurowaliśmy za Ciebie?

- szablony
  - umieszczaj je w aplikacji **jedzonko** w katalogu **templates**,
- pliki statyczne
  - pliki statyczne (czyli wszystkie pliki, które są serwowane przez aplikację: obrazki, pliki CSS, JS itp.)
  umieszczaj w katalogu **static**, który znajduje się w głównym katalogu projektu.

### Czego nie skonfigurowaliśmy?

- bazy danych (ze względów bezpieczeństwa)

**Pamiętaj:** nie należy trzymać danych wrażliwych pod kontrolą Gita! Takimi danymi wrażliwymi
są m. in. dane do połączenia z bazą danych. Te dane trzymamy w pliku **local_settings.py**,
którego nie znajdziesz w tym repozytorium (plik jest dodany do **.gitignore**)!

Zajrzyj do pliku **settings.py**, znajdziesz w nim następującą sekcję:

```python
try:
    from scrumlab.local_settings import DATABASES
except ModuleNotFoundError:
    print("Brak konfiguracji bazy danych w pliku local_settings.py!")
    print("Uzupełnij dane i spróbuj ponownie!")
    exit(0)
```

Oznacza to, że Django podczas każdego uruchomienia będzie próbowało zaimportować
stałą `DATABASES` z pliku **local_settings.py**. Tam trzymaj dane do połączenia.
Nie umieszczaj tego pliku pod kontrolą Gita. Aby ułatwić Ci pracę, przygotowaliśmy 
plik **local_settings.py.example**, w którym znajdziesz przygotowane odpowiednie dane.
Wystarczy tylko, że zmienisz plikowi **local_settings.py.example** nazwę na  **local_settings.py** 
i uzupełnisz go.

--- 

Jeśli wszystko skonfigurowałeś poprawnie, to pod adresem http://localhost:8000/index zobaczysz przykładową stronę.