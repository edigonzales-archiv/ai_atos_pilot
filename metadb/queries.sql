SELECT DISTINCT sfe.pkuid, df.pkuid, srs_auth, srs_code
FROM service_feed_entry as sfe, dataset_feed as df, dataset_feed_entry as dfe
WHERE sfe.pkuid = df.sfe_id
AND df.pkuid = dfe.df_id



