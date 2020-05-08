# Automat biletowy MPK

## 1. Opis zadania
  * Automat przechowuje informacje o monetach/banknotach znajdujących się w
nim (1, 2, 5, 10, 20, 50gr, 1, 2, 5, 10, 20, 50zł) [dziedziczenie: można napisać
uniwersalną klasę PrzechowywaczMonet po której dziedziczyć będzie automat]
  * Okno z listą biletów w różnych cenach (jako przyciski). Wymagane bilety:
20-minutowy, 40-minutowy, 60-minutowy w wariantach normalnym i ulgowym.
  * Możliwość wybrania więcej niż jednego rodzaju biletu. Możliwość
wprowadzenia liczby biletów.
  * Po wybraniu biletu pojawia się okno z listą monet (przyciski) oraz
możliwością dodania kolejnego biletu lub liczby biletów.
  * Interfejs ma dodatkowo zawierać pole na wybór liczby wrzucanych
monet (domyślnie jedna).
  * Po wrzuceniu monet, których wartość jest większa lub równa cenie
    wybranych biletów, automat sprawdza czy może wydać resztę.
  * Brak reszty/może wydać: wyskakuje okienko z informacją o zakupach, wydaje
    resztę (dolicza wrzucone monety, odlicza wydane jako reszta), wraca do
    wyboru biletów.
 1.8. Nie może wydać: wyskakuje okienko z napisem "Tylko odliczona kwota"
    oraz zwraca włożone monety.
## 2. Testy
 * Bilet kupiony za odliczoną kwotę - oczekiwany brak reszty.
 * Bilet kupiony płacąc więcej - oczekiwana reszta.
 * Bilet kupiony płacąc więcej, automat nie ma jak wydać reszty - oczekiwana
     informacja o błędzie oraz zwrócenie takiej samej liczby monet o tych
     samych nominałach, co wrzucone.
 * Zakup biletu płacąc po 1gr - suma stu monet 1gr ma być równa 1zł (dla floatów
     suma sto razy 0.01+0.01+...+0.01 nie będzie równa 1.0). Płatności można dokonać
     za pomocą pętli for w interpreterze.
 * Zakup dwóch różnych biletów naraz - cena powinna być sumą.
 * Dodanie biletu, wrzucenie kilku monet, dodanie drugiego biletu, wrzucenie  
     pozostałych monet, zakup za odliczoną kwotę - oczekiwany brak reszty
     (wrzucone monety nie zerują się po dodaniu biletu).
 * Próba wrzucenia ujemnej oraz niecałkowitej liczby monet (oczekiwany komunikat
     o błędzie).
