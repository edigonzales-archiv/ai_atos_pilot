SELECT sfe.identifier_code, sfe.identifier_namespace, df.title, dfe.format_mime, dfe.format_txt, dfe.srs_auth, dfe.srs_code, dfe.srs_txt, dfe.alternate_link
FROM service_feed_entry as sfe, dataset_feed as df, dataset_feed_entry as dfe
WHERE sfe.pkuid = df.sfe_id
AND df.pkuid = dfe.df_id
AND sfe.identifier_code = '788f4376-a625-4c0a-8704-458aa59bff79'
AND sfe.identifier_namespace = 'http://www.geodienste.ch'
AND dfe.format_mime = 'application/gml+xml;version=3.2'
AND srs_code = 21781
