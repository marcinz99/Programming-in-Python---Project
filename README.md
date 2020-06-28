# Programowanie w języku Python
## Projekt: System wizualizacji stanu „inteligentnego” domu

Wykonawca: Marcin Zięba

## Informacje ogólne

Założenia projetkowe:

> Celem systemu jest wizualizacja stanu inteligentnego domu, m.in. stany oświetlenia, otwarcia bądź zamknięcia drzwi i okien, parametrów środowiskowych w pomieszczeniach (temperatura, wilgotność, itp.) oraz ruchu wykrywanego w pomieszczeniach.<br>
> Potrzebne dane będą pobierane z brokera komunikatów MQTT i wyświetlane na planie domu/mieszkania. Plan domu (np. pochodzący z pliku jpg) oraz położenie czujników, lamp, itp. (np. opisane w pliku np. yaml, json) będą wczytywane do systemu, następnie system będzie odbierał komunikaty od brokera MQTT i wyświetlam zmiany na planie.

Sugerowane IDE: **PyCharm**

Uwaga: Projekt napisany został w środowisku PyCharm. Uruchamiając go z innego IDE lub z terminalu, może być konieczne wyspecyfikowanie źródeł kodu, korzystając z modułu `sys` przed innymi importami w każdym pliku `*.py`, korzystającym z tych źródeł. Rozwiązanie takie jest jednak odradzane. Lepszym rozwiązaniem będzie pozbycie się podziału na foldery i wrzucenia wszystkiego do jednego.
> `import sys`<br>
> `sys.path.append("../dependencies-api")`<br>
> `sys.path.append("../config")`<br>
> `sys.path.append("../img")`

Wykorzystane moduły spoza biblioteki standardowej:
* Pillow (`pip install Pillow`)
* paho-mqtt (`pip install paho-mqtt`)

Projekt można podzielić na dwie części:
* aplikacja (uruchamianie poprzez `main.py`)
* dostarczyciel zadań (uruchamiane poprzez `event_provider.py`)
