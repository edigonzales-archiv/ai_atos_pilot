** Geocat **

Noch keine Einträg in geocat.ch für Dienst und Datensatz.


**GeoRSS: <georss:box> oder <georss:polygon>?**

Falls wir sowieso nur die Boundingbox verlangen, reicht <georss:box>. Besteht auch aus weniger Koordinatenpaaren (2 versus 5).


**GeoRSS: <georss:where>?**

Wollen wir das? Ist nicht mehr GeoRSS Simple, sondern "normales" GML. Konsequenterweise müssten wir dann hier auch wieder die gleiche Kodierung wie in INTERLIS/GML verwenden.

[http://www.georss.org/](http://www.georss.org/)
[https://en.wikipedia.org/wiki/GeoRSS](https://en.wikipedia.org/wiki/GeoRSS)


** <updated> **

Was sagt das jetzt genau aus? Was sagt es aus wenn die Feeds dynamisch erzeugt werden? Soll da *definitiv nicht* das Nachführungsdatum des Datensatz reingeschrieben werden? Btw: Was heisst Nachführungsdatum? 

Beispiel aus amtlicher Vermessung: Die letzte Änderung im Datensatz (z.B. Mutation an Grundstück) ist vom 23. November 2014. Was soll jetzt bei <updated> stehen? Der Zeitpunkt wo die INTERLIS/GML-Datei erzeugt wurde? Wenn sie z.B. täglich aus der DB erzeugt wird, ändert das Datum täglich? 

Ich glaube, ich möchte ein anderes Datum stehen haben, wenn es die Dateien ändern. Ändern muss nicht bloss inhaltlich gemeint sein, sondern wenn sie eben auch einfach neu exportiert werden. Alles andere geht mir irgendwie nicht auf und ist nicht wirklich handlebar.


** Anzahl Service Feeds? **

Wie viele Service Feeds wird es geben? Pro MGDM (siehe Diskussion Datensatz vs MGDM) einen? Oder ein (1) Service Feed für alles?

Abhängigkeit: Eintrag in Geocat.


** Mehrere physische Dateien **

Wer gibt das vor? a) Ob es welche gibt und b) wie sie partioniert sind? 

Egal ob AtOS oder WFS (stored queries).


** Was steht bei <author>?**

Was steht da?