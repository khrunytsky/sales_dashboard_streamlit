👟 Adidas USA – Sales Performance Dashboard

Interaktywny dashboard sprzedażowy zbudowany w Streamlit, analizujący dane sprzedażowe Adidas na rynku USA. Aplikacja pozwala na eksplorację przychodów, zysku operacyjnego i wolumenu sprzedaży w podziale na metody sprzedaży, regiony, typy produktów i miasta.

Live: https://brand-sales-dashboard.streamlit.app

 Funkcjonalność


Karty KPI – całkowity przychód, zysk operacyjny, sprzedane sztuki, średnia marża
Filtry interaktywne – po metodzie sprzedaży/roku/retailerze (w panelu bocznym)
Dynamika przychodu i zysku w czasie – wykres liniowy z agregacją miesięczną
Udział metod sprzedaży – wykres donut
Mapa bąbelkowa USA – przychód w podziale na miasta (wielkość i kolor bąbelka = przychód)
Przychody wg kategorii produktów – poziomy wykres słupkowy
Przychody wg regionów – wykres słupkowy z kolorową skalą

Requirements:
Python 
Streamlit – framework do budowy aplikacji webowych
Pandas – przetwarzanie i agregacja danych
Plotly Express / Graph Objects – wizualizacje interaktywne
OpenPyXL – wczytywanie danych z pliku Excel



Struktura projektu

sales_dashboard_streamlit/
├── .streamlit/                       # konfiguracja Streamlit
├── Adidas US Sales Datasets.xlsx     # dane źródłowe
├── city_coords.py                    # słownik współrzędnych miast (lat/lon)
├── main.py                           # główna aplikacja Streamlit
├── requirements.txt                  # zależności projektu
└── README.md



📈 Źródło danych

Dane pochodzą z publicznie dostępnego zbioru Adidas Sales Dataset (https://www.kaggle.com/datasets/heemalichaudhari/adidas-sales-dataset), zawierającego informacje o sprzedaży w USA.


👤 AndrzejK

Projekt stworzony jako część portfolio.

[LinkedIn](https://www.linkedin.com/in/andrii-khrunytskyi-012438366?utm_source=share_via&utm_content=profile&utm_medium=member_ios) • [Github](https://github.com/khrunytsky)