INSERT INTO service_feed (pkuid, title, subtitle, self_link, describedby_link, search_link, rights) 
VALUES (1, "eCH-0056 Downloaddienst der Kantone", "Vordefinierter Downloaddienst der Kantone auf Basis von Atom Feed und OpenSearch.", "", "http://www.geocat.ch/geonetwork/srv/ger/xml_iso19139?id=123456", "", "Es gelten die Nutzungsbedingungen geodienste.ch.");


-- bbox of canton Solothurn
INSERT INTO service_feed_entry (pkuid, sf_id, identifier_code, identifier_namespace, title, subtitle, summary, describedby_link, rights, updated, x_min, y_min, x_max, y_max)
VALUES (1, 1, "788f4376-a625-4c0a-8704-458aa59bff79", "http://www.geodienste.ch", "Gefahrenkartierung", "Gefahrenkarte / Gefahrenkartierung", "<xhtml:div xmlns:xhtml='http://www.w3.org/1999/xhtml'>
  <xhtml:p>
    Die aggregierte Gefahrenkartierung der Schweiz im minimalen <xhtml:a href='http://models.geo.admin.ch/BAFU/Hazard_Mapping_V1_1.ili'>Geodatenmodell</xhtml:a>.
  </xhtml:p>
  <xhtml:p>
    Hier könnten bereits Downloadlinks stehen. Darauf verzichte ich, da eine sinnvolle Meta-DB Implentierung dafür nötig wäre und das out-of-scope ist.
  </xhtml:p>	
</xhtml:div>", "http://www.geocat.ch/geonetwork/srv/ger/xml_iso19139?id=243086", "Es gelten die Nutzungsbedingungen geodienste.ch.", "2015-11-13 06:00:00", 7.34041, 47.0743, 8.03137, 47.5027);


INSERT INTO dataset_feed (pkuid, sfe_id, title, subtitle, rights)
VALUES (1, 1, "Gefahrenkartierung", "Gefahrenkarte / Gefahrenkartierung", "Es gelten die Nutzungsbedingungen geodienste.ch.");


INSERT INTO dataset_feed_models (pkuid, df_id, describedby_link)
VALUES (1, 1, "http://models.geo.admin.ch/BAFU/Hazard_Mapping_V1_1.ili");


INSERT INTO dataset_feed_entry (pkuid, df_id, title, alternate_link, summary, format_mime, format_txt, srs_auth, srs_code, srs_txt, updated)
VALUES (1, 1, "", "http://catais.org/geodaten/ch/gl/efs/supplysecurity/xtf/lv03/supplysecurity.xtf", "<xhtml:div xmlns:xhtml='http://www.w3.org/1999/xhtml'>
  <xhtml:p>
    Die aggregierte Gefahrenkartierung der Schweiz im minimalen <xhtml:a href='http://models.geo.admin.ch/BAFU/Hazard_Mapping_V1_1.ili'>Geodatenmodell</xhtml:a> / {{item['srs_txt']}} / {{item['format_txt']}}.
  </xhtml:p>
  <xhtml:p>
    Hier könnten bereits Downloadlinks stehen. Darauf verzichte ich, da eine sinnvolle Meta-DB Implentierung dafür nötig wäre und das out-of-scope ist.
  </xhtml:p>	
</xhtml:div>", "application/gml+xml;version=3.2", "GML", "EPSG", "21781", "LV03", "2015-11-13 06:00:00");


