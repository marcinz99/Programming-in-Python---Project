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
