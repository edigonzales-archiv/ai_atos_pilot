INSERT INTO service_feed (pkuid, title, subtitle, self_link, describedby_link, search_link, rights) 
VALUES (1, "eCH-0056 Downloaddienst der Kantone", "Vordefinierter Downloaddienst der Kantone auf Basis von Atom Feed und OpenSearch.", "", "http://www.geocat.ch/geonetwork/srv/ger/xml_iso19139?id=123456", "", "Es gelten die Nutzungsbedingungen geodienste.ch.");


-- bbox of canton Solothurn
INSERT INTO service_feed_entry (pkuid, sf_id, identifier_code, identifier_namespace, title, subtitle, summary, describedby_link, rights, updated, x_min, y_min, x_max, y_max)
VALUES (1, 1, "788f4376-a625-4c0a-8704-458aa59bff79", "http://www.geodienste.ch", "Gefahrenkartierung", "Gefahrenkarte / Gefahrenkartierung", "<div>
  <p>
    Die aggregierte Gefahrenkartierung der Schweiz im minimalen <a href='http://models.geo.admin.ch/BAFU/Hazard_Mapping_V1_1.ili'>Geodatenmodell</a>.
  </p>
  <p>
    Hier könnten bereits Downloadlinks oder ein schönes Bildli stehen. Oder auch Link zu <a href='https://s.geo.admin.ch/6831e869fd'>Darstellungsdienst</a> inkl. nettem Vorschaubild.
  </p>
</div>", "http://www.geocat.ch/geonetwork/srv/ger/xml_iso19139?id=243086", "Es gelten die Nutzungsbedingungen geodienste.ch.", "2015-11-13 06:00:00", 7.34041, 47.0743, 8.03137, 47.5027);



INSERT INTO dataset_feed (pkuid, sfe_id, title, subtitle, rights)
VALUES (1, 1, "Gefahrenkartierung", "Gefahrenkarte / Gefahrenkartierung", "Es gelten die Nutzungsbedingungen geodienste.ch.");


INSERT INTO dataset_feed_models (pkuid, df_id, describedby_link)
VALUES (1, 1, "http://models.geo.admin.ch/BAFU/Hazard_Mapping_V1_1.ili");


INSERT INTO dataset_feed_entry (pkuid, df_id, title, alternate_link, summary, format_mime, format_txt, srs_auth, srs_code, srs_txt, updated)
VALUES (1, 1, "", "http://catais.org/geodaten/ch/gl/efs/supplysecurity/xtf/lv03/supplysecurity.xtf", "<div>
  <p>
    Die aggregierte Gefahrenkartierung der Schweiz im minimalen <a href='http://models.geo.admin.ch/BAFU/Hazard_Mapping_V1_1.ili'>Geodatenmodell</a> / {{item['srs_txt']}} / {{item['format_txt']}}.
  </p>
  <p>
    Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam.
  </p>
</div>", "application/gml+xml;version=3.2", "GML", "EPSG", "21781", "LV03", "2015-11-13 06:00:00");

INSERT INTO dataset_feed_entry (pkuid, df_id, title, alternate_link, summary, format_mime, format_txt, srs_auth, srs_code, srs_txt, updated)
VALUES (2, 1, "", "http://catais.org/geodaten/ch/gl/efs/supplysecurity/xtf/lv03/supplysecurity.xtf", "<div>
  <p>
    Die aggregierte Gefahrenkartierung der Schweiz im minimalen <a href='http://models.geo.admin.ch/BAFU/Hazard_Mapping_V1_1.ili'>Geodatenmodell</a> / {{item['srs_txt']}} / {{item['format_txt']}}.
  </p>
  <p>
    LV95-Dummy: Ich brauche weitere Dataset Feed Einträge, um die Erstellung der Feeds testen zu können. Dieser hier hat auch ein anderes Datum.
  </p>
</div>", "application/gml+xml;version=3.2", "GML", "EPSG", "2056", "LV95", "2015-11-12 06:00:00");

INSERT INTO dataset_feed_entry (pkuid, df_id, title, alternate_link, summary, format_mime, format_txt, srs_auth, srs_code, srs_txt, updated)
VALUES (3, 1, "", "http://catais.org/geodaten/ch/gl/efs/supplysecurity/xtf/lv03/supplysecurity.xtf", "<div>
  <p>
    Die aggregierte Gefahrenkartierung der Schweiz im minimalen <a href='http://models.geo.admin.ch/BAFU/Hazard_Mapping_V1_1.ili'>Geodatenmodell</a> / {{item['srs_txt']}} / {{item['format_txt']}}.
  </p>
  <p>
    XTF-Dummy: Ich brauche weitere Dataset Feed Einträge, um die Erstellung der Feeds testen zu können.
  </p>
</div>", "application/interlis+xml;version=2.3", "XTF", "EPSG", "21781", "LV03", "2015-11-12 06:00:00");
