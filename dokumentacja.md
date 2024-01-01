# Dokumentacja projektu "Koło Fortuny"

## Dane autora
- Autor: Kacper Górski
- Numer indeksu: 331379
- E-mail uczelniany: 01187228@pw.edu.pl
- E-mail prywatny: kerciuuu@gmail.com

## Cel i opis projektu
Projekt "Koło Fortuny" ma na celu umożliwienie graczom gry w znaną z telewizji 'dwójkę' (TVP2). Użytkownik może grać w trzyosobowym trybie, zachowując większość reguł z oryginalnego teleturnieju. Program prowadzi interakcję z graczami przez całą rozgrywkę.
Program składa się z trzech rund i jednej rundy finałowej.
Po uruchomieniu programu witany jest użytkownik i zapraszany do gry, proszony jest o podanie imion graczy. Program pobiera hasła i kategorie z pliku, losuje hasło i koduje je znakami '-'. Gracze mają trzy możliwości: kręcenie kołem fortuny, kupno samogłoski lub odgadnięcie całego hasła. Opcja kręcenia kołem losuje nagrody z listy obecnej w teleturnieju i prosi gracza o odgadnięcie spółgłoski (pod warunkiem, że nie wylosował 'BANKRUT' lub 'STOP' - wtedy kolejka przechodzi automatycznie na kolejnego gracza). Wynik losowania wpływa na dalszy przebieg gry. Na przykład, gdy gracz wylosuje 200 punktów i odgadnie spółgłoskę, punkty są dodawane do jego konta, a ukryte hasło jest odkrywane. W przeciwnym razie kolejka przechodzi na następnego gracza.
Oprócz pól pieniężnych i wyżej wymienionych pól utraty kolejki, istnieje pole 'NIESPODZIANKA', które przypisuje graczowi losową niespodziankę.
Opcja odgadnięcia samogłoski wykonywana jest tylko wtedy, gdy gracz ma 200 punktów w rundzie, ponieważ kosztuje ona właśnie tyle punktów. Jeśli gracz odgadnie samogłoskę, 200 punktów zostaje odjętych z jego konta (tak samo, gdy nie odgadnie samogłoski), a hasło jest odkrywane.
Odgadnięte spółgłoski i samogłoski są zapisywane.
Opcja odgadnięcia całego hasła prosi gracza o wpisanie pełnego hasła. Zalecane jest próbowanie odgadnięcia hasła, gdy jest ono częściowo odkryte i gracz jest pewny poprawności. Nieodgadnięcie hasła przenosi kolejkę na następnego gracza. Odgadnięcie hasła kończy rundę, przypisuje zwycięzcy punkty za rundę i zeruje punkty każdego gracza.
Po zakończeniu trzech rund wybierany jest zwycięzca z największą liczbą punktów. Pozostali gracze zostają pożegnani, a rozdawane są ewentualne niespodzianki. Wybierane jest hasło finałowe, które jest zakodowane. Program wyświetla litery R, S, T, L, N, E, a jeśli są one w haśle, są one odkrywane. Następnie losuje 5 liter (niewidocznych dla gracza) i odkrywa je, jeśli są w haśle. Po odkryciu, program zaczyna odliczanie, a po 10 sekundach prosi gracza o wpisanie odpowiedzi. Jeśli gracz nie zgadnie hasła, wychodzi z gry z nagrodą pieniężną równą liczbie zdobytych punktów. W przeciwnym przypadku zdobywa nagrodę pieniężną oraz Poloneza Caro.

## Podział programu na klasy i opis klas
### Klasa Player
- Opis: Klasa obsługująca graczy uczestniczących w grze. Zbiera dane graczy takie jak ich imiona i liczba punktów. Zbiera również liczbę permamentnych punktów oraz pozwala na dodawanie i odejmowanie obu rodzajów punktów. Zbiera również niespodzianki, które gracz zdobył podczas gry.

### Klasa WordAndCategory
- Opis: Klasa obsługująca hasła i ich kategorię. Jest to kluczowa klasa dla działania programu, ponieważ przechowuje dane pobrane z pliku 'hasla.json'.

## Instrukcja użytkownika
Projekt można uruchomić, wykonując wiersz poleceń nazwę modułu 'game.py'.

## Część refleksyjna
Podczas realizacji projektu napotkałem trudności związane z optymalizacją kodu. Podzielenie programu na mniejsze funkcje, zwłaszcza w funkcji play_round(), prowadziło do problemów z działaniem programu. Ponadto próbowałem korzystać z wątków zaimplementowanych w Pythonie (Threads), aby symulować odliczanie countdown() oraz odkrywanie losowych liter reveal_letters() w rundzie finałowej, lecz wątki nakładały się na siebie w jednej linii, nie mogłem znaleźć rozwiązania dla mojego problemu w Internecie, dlatego zrezygnowałem z tej części programu. Rozważałem również wykorzystanie klas w szerszym zakresie, ale nie przyszły mi do głowy żadne pomysły, jak mógłbym to zaimplementować. Ponadto jako, że gra sama w sobie jest wzorowana na polskiej wersji, to mimo to i tak programowałem po angielsku. Wnioski z realizacji projektu są takie, że muszę jeszcze pracować nad optymalizacją kodu. Chciałbym w tej części podziękować prowadzącym przedmiot oraz projektowi za możliwość przetestowania moich umiejętności w ten sposób.
