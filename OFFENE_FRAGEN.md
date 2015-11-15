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


** MIME-Type für INTERLIS/XTF?**

application/interlis+xml;version=2.3 oder text/x-interlis23 ?


** <summary> xhtml vs html**

Ich bring xhtml nicht zum laufen (wo wie wir das in eCH-0056 geschrieben haben). html im Firefox auch nur wenn man `<![CDATA[<div>...</div>]]>` wegglässt. Wie sieht es in IE aus?


** Redundanz**

Bei der Implementierung gut überlegen, welcher Inhalt von welchen Tags gleich sein soll (z.b. <title> etc.). Soll/muss es so sein oder soll die Implementierung beides zulassen (Auswirkung auf DB-Struktur).

** Meta-DB für AtOS**
Ich glaube am liebsten wäre mir die Abbildung von des Atom Feeds XSD in der DB und dann werden diese Tabelle aus einer Meta-DB abgefüllt. Wäre wohl am profimässigsten. Anschliessend sauber als XML exportieren (JAXB o.ä.).


** OpenSearch **

"The example given in Annex A uses content negotiation to identify which operation to perform. This
means that even though the operation endpoint is only one, i.e. http://xyz.org/search.php, the client
has to set the HTTP-Accept-Header to the correct value in order to receive the expected result."

Dieser Accept-Header approach ist also absichtlich und bewusst gewählt worden. Was machen wir in eCH-0056? Ich finde es immer noch bisschen "abgehoben".

Ist bei DescribeSpatialDataset CRS und MediaType notwendig? Nein, oder?

Gedankestütze: Abfrage von Klient in mehreren Stufen (wenn ich id von Datensatz kenne):

1) OpenSearch
2) Klient such nach describedby Url und ruft diese URL auf. Response ist Dataset feed. Dort drin stehen alle vorhandenen Kombination von CRS und Mimetypes.
3) Klient sucht nach results Url in OpenSearch und ruft mit den gewünschten Parameter diese URL auf, um den Datensatz herunterzuladen.

(Warum lädt er dann nicht mit einem GET den Datensatz runter wenn er beim Schritt 2 den Datasetfeed liest?)


** OpenSearch Language **
Was sagt <Language>de</Language> aus? Ah: Available languages of download service.


** OpenSearch Query **
Nur ein example oder alle Varianten? Dann müsste aber nicht nur CRS, sondern auch z.B. mime type dazugehören.
