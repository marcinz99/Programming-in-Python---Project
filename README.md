# Programowanie w języku Python
## Projekt: System wizualizacji stanu „inteligentnego” domu

Wykonawca: **Marcin Zięba**

![app in use](https://github.com/marcinz99/Programming-in-Python---Project/blob/master/img/app.png "Aplikacja w akcji")

## Informacje ogólne

Założenia projetkowe:

> Celem systemu jest wizualizacja stanu inteligentnego domu, m.in. stany oświetlenia, otwarcia bądź zamknięcia drzwi i okien, parametrów środowiskowych w pomieszczeniach (temperatura, wilgotność, itp.) oraz ruchu wykrywanego w pomieszczeniach.<br>
> Potrzebne dane będą pobierane z brokera komunikatów MQTT i wyświetlane na planie domu/mieszkania. Plan domu (np. pochodzący z pliku jpg) oraz położenie czujników, lamp, itp. (np. opisane w pliku np. yaml, json) będą wczytywane do systemu, następnie system będzie odbierał komunikaty od brokera MQTT i wyświetlam zmiany na planie.

IDE: **PyCharm**

Uwaga: Projekt napisany został w środowisku PyCharm. Uruchamiając go z innego IDE lub z terminalu, może być konieczne wyspecyfikowanie źródeł kodu (`sys.path`).
* Jeśli korzystasz z innego IDE, oznacz folder `src/dependencies-api` jako źródło.
* Jeśli korzystasz z czystego edytora tekstu konieczne może być wyedytowanie `sys.path` w każdym pliku `*.py` spoza folderu `src/dependencies-api`. Rozwiązanie takie jest jednak stanowczo odradzane, gdyż mija się z celem i wymaga sporo niepotrzebnej ręcznej roboty (`import sys` oraz `sys.path.append("../dependencies-api")` przed pozostałymi importami).

Uwaga: Należy pamiętać o uprzednim zainstalowaniu brokera MQTT, np. Mosquito.

Wykorzystane moduły spoza biblioteki standardowej:
* Pillow (`pip install Pillow`)
* paho-mqtt (`pip install paho-mqtt`)

Projekt można podzielić na dwie części:
* aplikacja (uruchamianie poprzez `main.py`)
* dostarczyciel zadań (uruchamiane poprzez `event_provider.py`)

Uruchamianie aplikacji (zalecane):
* Otwórz projekt w środowisku PyCharm
* Zainstaluj w wirtualnym środowisku wymagane moduły (Pillow i paho-mqtt)
* Uruchom broker MQTT
* Uruchom aplikację plik `main/main.py` (Run 'main')
* (Opcjonalnie) Uruchom dostarczyciela wydarzeń `event_provider/event_provider.py` (Run 'event_provider')

Aplikacja w obecnej postaci rozróżnia urządzenia na dwa typy:
* switchable - wszelkie urządzenia, których stan przełącza się między włączonych (`ON`) oraz wyłączonym (`OFF`), jak na przykład żarówka czy telewizor;
* detector - jak sugeruje nazwa może to być wykrywacz ruchu, dymu, itp.; urządzenia tego typu przełączają się między stanami `IDLE` oraz `EXCITED`.

## Opis zawartości

Poniżej opisana jest zawartość poszczególnych podfolderów projektu (z `src/`).

#### Folder `config`

W folderze tym powinny się znaleźć następującego pliki:
* plan domu (`home_plan.bmp` o wymiarach 750x520 px)
* informacje o urządzeniach (`plan.json`)
Powyższe pliki można zmodyfikować, żeby dostosować aplikację pod konkretne pomieszczenie lub mieszkanie.

#### Folder `dependencies-api`

* `topic_tree.py` - API struktury drzewiastej obsługiwanych tematów
* `mqtt_api.py` - uproszczone API dla klientów MQTT

#### Folder `img`

Ikony urządzeń obu obsługiwanych typów wraz w możliwymi stanami.

#### Folder `main`

Główny folder aplikacji:
* `main.py` - główny kod aplikacji
* `window.py` - klasa definiująca GUI aplikacji w trybie okienkowym

#### Folder `event_privider`

Folder z dostarczycielem zdarzeń dla aplikacji. Uruchomienie jego pozwala zasymulować działanie w normalnych warunkach pracy.
* `event_provider.py` - kod dostarczyciela wydarzeń
* `events_schedule.txt` - zaplanowane wydarzenia w formacie "<opóźnienie> <temat> <wiadomość>" w kolejnych linijkach pliku tekstowego
