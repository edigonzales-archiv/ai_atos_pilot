SELECT sfe.identifier_code, sfe.identifier_namespace, df.title, dfe.format_mime, dfe.format_txt, dfe.srs_auth, dfe.srs_code, dfe.srs_txt
FROM service_feed_entry as sfe, dataset_feed as df, dataset_feed_entry as dfe
WHERE sfe.pkuid = df.sfe_id
AND df.pkuid = dfe.df_id;
